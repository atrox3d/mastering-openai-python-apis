import pickle
import pandas as pd
from pathlib import Path
import logging

from .defaults import CACHE_PATH


logger = logging.getLogger(__name__)


def reset_cache(cache_path:str=CACHE_PATH):
    print(f'deleting {cache_path}')
    Path(cache_path).unlink(missing_ok=True)


def save_cache(cache:dict, cache_path:str=CACHE_PATH, reset:bool=False):
    if reset:
        reset_cache(cache_path)

    print(f'saving cache to {cache_path}')
    with open(cache_path, 'wb') as fp:
        pickle.dump(cache, fp)


def get_cache(cache_path:str=CACHE_PATH, reset:bool=False) -> dict:
    if reset:
        reset_cache(cache_path)
    try:
        print(f'loading {cache_path}...')
        cache = pd.read_pickle(cache_path)
    except FileNotFoundError:
        print('failed to load')
        cache = {}
        save_cache(cache)
    return cache

import sqlite3
import functools
import inspect
import pickle

def memoize_to_sqlite(sqlite_path):
    """
    Decorator that memoizes function results to an SQLite database.

    Args:
        sqlite_path (str): The path to the SQLite database file.

    Returns:
        callable: The decorated function.
    """

    def decorator(func):
        """
        The actual decorator that wraps the function.
        """

        func_name = func.__name__
        arg_names = inspect.getfullargspec(func).args
        logger.debug(f'{func_name} args: {arg_names}')

        def create_table():
            """Creates the table in the database if it doesn't exist."""
            conn = sqlite3.connect(sqlite_path)
            cursor = conn.cursor()

            # Determine argument types for database schema
            arg_types = []
            for arg in arg_names:
                arg_types.append("BLOB")  # Default to BLOB for flexibility
            arg_defs = ", ".join(f"{arg} BLOB" for arg in arg_names)
            logger.debug(f'{func_name} arg_defs: {arg_defs}')

            CREATE_QUERY = f"""
                CREATE TABLE IF NOT EXISTS {func_name} (
                    {arg_defs},
                    result BLOB,
                    UNIQUE ({', '.join(arg_names)})
                )
            """
            logger.debug(f'{func_name} CREATE_QUERY: {CREATE_QUERY}')
            cursor.execute(CREATE_QUERY)
            conn.commit()
            conn.close()

        create_table()  # Ensure the table exists at decorator time

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """
            The wrapper function that handles memoization logic.
            """
            # Handle both positional and keyword arguments consistently
            bound_args = inspect.signature(func).bind(*args, **kwargs)
            bound_args.apply_defaults()
            logger.debug(f'{func_name} bound_args: {bound_args}')

            arg_values = tuple(bound_args.arguments[arg] for arg in arg_names)

            # Serialize arguments to byte strings for SQLite storage
            serialized_args = tuple(pickle.dumps(arg) for arg in arg_values)

            # Check if result is already in the database
            conn = sqlite3.connect(sqlite_path)
            cursor = conn.cursor()

            placeholders = ", ".join(["?"] * len(arg_names))
            logger.debug(f'{func_name} placeholders: {placeholders}')

            SELECT_QUERY = f"""
                SELECT result FROM {func_name}
                -- WHERE {', '.join(arg_names)} = ({placeholders})
                WHERE {'AND '.join(f'{arg} = ?' for arg in arg_names)}
            """
            logger.debug(f'{func_name} SELECT_QUERY: {SELECT_QUERY}')
            logger.debug(f'{func_name} serialized_args: {serialized_args}')

            cursor.execute(SELECT_QUERY, serialized_args)
            result = cursor.fetchone()
            conn.close()

            if result:
                # Result found in the database
                deserialized_result = pickle.loads(result[0])
                logger.debug(f'{func_name} deserialized_result: {deserialized_result}')
                logger.info(f'found result returning cached value')
                return deserialized_result
            else:
                logger.info(f'no cached result found, executing')
                # Result not found, execute the function
                result = func(*args, **kwargs)
                serialized_result = pickle.dumps(result)

                # Store the result in the database
                conn = sqlite3.connect(sqlite_path)
                cursor = conn.cursor()
                placeholders = ", ".join(["?"] * (len(arg_names) + 1))  # Add placeholder for the result

                insert_query = f"""
                    INSERT OR REPLACE INTO {func_name} ({', '.join(arg_names)}, result)
                    VALUES ({placeholders})
                """

                values_to_insert = serialized_args + (serialized_result,)  # Combine args and serialized result

                try:
                    cursor.execute(insert_query, values_to_insert)
                    conn.commit()
                except sqlite3.IntegrityError:
                    # Handle potential race conditions (e.g., if another process
                    # inserts the same result concurrently).
                    # In this case, just try to retrieve the result again.
                    conn.close()
                    return wrapper(*args, **kwargs)

                finally:
                    conn.close()

                return result

        return wrapper

    return decorator


