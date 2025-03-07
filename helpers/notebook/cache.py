import pickle
import pandas as pd
from .defaults import CACHE_PATH


from pathlib import Path


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