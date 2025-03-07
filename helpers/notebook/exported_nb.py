from operator import ge
import os, json
import openai
from dotenv import dotenv_values, load_dotenv
from random import randint

from helpers.notebook.decorators import retry
from helpers.notebook.cache import get_cache
from helpers.notebook.embeddings import distances_from_embeddings, embedding_from_text, indices_of_nearest_neighbors_from_distances


from .defaults import (
    DATA_PATH,
    INPUT_FILE,
    OUTPUT_FILE,
    INPUT_PATH,
    EMBEDDING_MODEL,

)

@retry(wait=.5)
def test_retry(attempts:int=0, max_retries=5):
    if randint(0, 1):
        raise Exception


# CACHE = get_cache(reset=False)

        # print('embedding already cached')



# pd.options.display.width = 1000
# pd.options.display.max_colwidth = 1000


# embedding_from_title('phantom thread', movie_plots)
# embedding_from_title('stargate', movie_plots)

# try:
    # for k, v in CACHE.items():
        # print(v['title'])
# except KeyError:
    # print(f'ERROR')
    # print(k[0])
    # del CACHE[k]
    # save_cache(CACHE)


# [embedding_from_title(title, movie_plots)  for title in movie_plots['Title'].values]

# e1 = list(CACHE.values())[0]['embedding']
# e2 = list(CACHE.values())[1]['embedding']
# distances_from_embeddings(e1, [e1, e2])

# plots_embeddings = [value['embedding'] for value in CACHE.values()]
# titles = [value['title'] for value in CACHE.values()]
# plots = [plot for plot, model in CACHE.keys()]


def print_recommendations_from_strings(
        strings:list[str],
        index_of_source_strings,
        cache:dict=get_cache(),
        k_nearest_neighbors:int=3,
        model:str=EMBEDDING_MODEL
):
    embeddings = [embedding_from_text(text, model=model)['embedding'] for text in strings]
    query_embedding = embeddings[index_of_source_strings]
    distances = distances_from_embeddings(query_embedding, embeddings)
    # distances = [float(distance) for distance in distances]
    indexes = indices_of_nearest_neighbors_from_distances(distances)
    near_k_indexes = indexes[1:1+k_nearest_neighbors]
    return [list(cache.values())[x]['title'] for x in near_k_indexes]

# print_recommendations_from_strings(plots, 0)


def print_recommendations_from_plot(
        strings:list[str],
        plot:str,
        cache:dict=get_cache(),
        k_nearest_neighbors:int=3,
        model:str=EMBEDDING_MODEL
):
    embeddings = [embedding_from_text(text, model=model)['embedding'] for text in strings]
    # query_embedding = embeddings[index_of_source_strings]
    query_embedding = embedding_from_text(plot, model=model)['embedding'] 
    distances = distances_from_embeddings(query_embedding, embeddings)
    # distances = [float(distance) for distance in distances]
    indexes = indices_of_nearest_neighbors_from_distances(distances)
    near_k_indexes = indexes[1:1+k_nearest_neighbors]
    return [list(cache.values())[x]['title'] for x in near_k_indexes]

# print_recommendations_from_plot(plots, 'in a galaxy far far away', 20)


