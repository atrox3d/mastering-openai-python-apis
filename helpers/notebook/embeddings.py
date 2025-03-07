import numpy as np
from typing import List
import pandas as pd
from scipy import spatial
from helpers.notebook.cache import get_cache, save_cache
from helpers.notebook.decorators import retry
from helpers.notebook.defaults import EMBEDDING_MODEL


import ollama
from ollama import EmbedResponse


@retry(wait=2, max_retries=5)
def get_embedding(text:str, embed_client:ollama.Client,model:str=EMBEDDING_MODEL) -> EmbedResponse:
    text = text.replace('\n', ' ')
    embedding = embed_client.embed(input=text, model=model)
    return embedding.embeddings[0]


def embedding_from_text(
        text:str,
        model:str=EMBEDDING_MODEL,
        cache:dict=get_cache(),
        save:bool=False,
        **extras
) -> dict:
    key = (text, model)
    if cache.get(key) is None:
        print('getting embedding...')
        new_value = {}
        for k, v in extras.items():
            new_value[k] = v

        new_value['embedding'] = get_embedding(text, model)
        if save:
            cache[key] = new_value
            save_cache(cache)
        return new_value
    else:
        return cache[key]


def embedding_from_tÌitle(title:str, movies:pd.DataFrame, model=EMBEDDING_MODEL, cache:dict=get_cache()):
    try:
        # result = movies.loc[movies['Title'].str.lower() == title.lower(), 'Plot']
        movie = movies.loc[movies['Title'].str.lower() == title.lower()]
        # title = result['Title'].squeeze()
        title = movie['Title'].iloc[0]
        plot = movie['Plot'].iloc[0]
        return embedding_from_text(plot, title=title, save=True)
    except (IndexError, KeyError):  # Catch potential errors
        print(f'movie {title} not found')
        return None

# 
# https://github.com/openai/openai-python/blob/release-v0.28.1/openai/embeddings_utils.py
# https://github.com/openai/openai-cookbook/blob/main/examples/utils/embeddings_utils.py
# 

# https://github.com/openai/openai-python/blob/release-v0.28.1/openai/embeddings_utils.py
# https://github.com/openai/openai-cookbook/blob/main/examples/utils/embeddings_utils.py

def distances_from_embeddings(
    query_embedding: List[float],
    embeddings: List[List[float]],
    distance_metric="cosine",
) -> List[np.float64]:
    """Return the distances between a query embedding and a list of embeddings."""
    distance_metrics = {
        "cosine": spatial.distance.cosine,
        "L1": spatial.distance.cityblock,
        "L2": spatial.distance.euclidean,
        "Linf": spatial.distance.chebyshev,
    }
    distances = [
        distance_metrics[distance_metric](query_embedding, embedding)
        for embedding in embeddings
    ]
    return distances


def indices_of_nearest_neighbors_from_distances(distances) -> np.ndarray:
    """Return a list of indices of nearest neighbors from a list of distances."""
    return np.argsort(distances)