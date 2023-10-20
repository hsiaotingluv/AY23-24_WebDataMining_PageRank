import pickle
from glob import glob
import numpy as np

def get_id_to_title_dict():
    """
    Method to retrieve the mapping of all index to title

        Returns:
            id_to_title_dict dictionary: with key as index and value as title, i.e. {1: "title"}
    """
    id_to_title_dict = {}
    for filename in glob("block/id_to_title_block_*.pkl"):
        with open(filename, "rb") as file_title:
            id_to_title = pickle.load(file_title)
        id_to_title_dict.update(id_to_title)
    print("Get id_to_title_dict finished!")
    return id_to_title_dict


def get_id_to_outlinks_id_dict():
    """
    Method to retrieve the mapping of all title id to outlink ids

        Returns:
            id_to_outlinks_id_dict: dictionary with key as index and value as a list of index, i.e. {1: [2, 3, 4]}
    """
    id_to_outlinks_id_dict = {}
    for filename in glob("block/id_to_outlinks_id_block_*.pkl"):
        with open(filename, "rb") as file_outlinks_id:
            id_to_outlinks_id = pickle.load(file_outlinks_id)
        id_to_outlinks_id_dict.update(id_to_outlinks_id)
    print("Get id_to_outlinks_id_dict finished!")
    return id_to_outlinks_id_dict


def calculate_pagerank(id_to_title_dict, id_to_outlinks_id_dict):
    """
    Method to calculate the PageRank score of all pages

        Parameters:
                id_to_title_dict: a dictionary, e.g. {1: "title"}
                id_to_outlinks_id_dict: a dictionary, e.g. {1: [2, 3, 4]}

        Returns:
            title_to_score_dict: dictionary with key as title and value as score, i.e. {"title": 0.01}
    """
    d = 0.85
    teleport = (1 - d) / len(id_to_title_dict) # teleport probability
    eps = 1e-3
    length = len(id_to_outlinks_id_dict)
    # every page has the same teleport probability
    pagerank_curr = [teleport] * length
    # every page has the same initial probability 1/n
    pagerank_prev = [1/length] * length 

    # Calculate pagerank - iteratively
    while True:
        for i in range(length):
            pagerank_curr[i] = teleport
        for title_id in id_to_outlinks_id_dict:
            if title_id in id_to_title_dict:
                outlink_len = len(id_to_outlinks_id_dict[title_id])
                if outlink_len == 0:
                    continue
                contribution = d * pagerank_prev[title_id] / outlink_len
                for outlink_id in id_to_outlinks_id_dict[title_id]:
                    pagerank_curr[outlink_id] += contribution

        # Swap pagerank_curr and pagerank_last
        pagerank_curr, pagerank_prev = pagerank_prev, pagerank_curr

        delta = np.linalg.norm(np.array(pagerank_curr) - np.array(pagerank_prev), ord=2)
        if delta < eps:
            break

    # Get the pagerank results and sort
    title_to_score_dict = {}
    for id, score in enumerate(pagerank_prev):
        title_to_score_dict.update({id_to_title_dict[id]: score})
    title_to_score_dict = sorted(title_to_score_dict.items(), key=lambda x: x[1], reverse=True)

    return title_to_score_dict


def write(title_to_score_dict):
    """
    Method to write content into file
    
        Parameters:
            title_to_score_dict: a dictionary, e.g. {"title": 0.01}
    """
    # Write to the 'pagerank.txt' file
    with open('pagerank.txt', 'w') as file_pagerank:
        for t in title_to_score_dict:
            file_pagerank.write(t[0] + "\t" + str(t[1]) + "\n")


id_to_title_dict = get_id_to_title_dict()
id_to_outlinks_id_dict = get_id_to_outlinks_id_dict()
title_to_score_dict = calculate_pagerank(id_to_title_dict, id_to_outlinks_id_dict)
write(title_to_score_dict)
