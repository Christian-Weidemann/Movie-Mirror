import matplotlib.pyplot as plt
import pickle
import networkx as nx
import os

# Path variables
raw_data_path = "data/raw/"
figure_path = "data/figures/"
bipartite_path = "data/bipartite/"
projection_path = "data/projections/"

def save_projection(G, path, overwrite=False):
    if overwrite or not os.path.exists(projection_path+path):
        with open(projection_path+path, 'wb') as f:
            pickle.dump(G, f)
        print("Projection saved.")

def load_projection(path):
    if os.path.exists(projection_path+path):
        with open(projection_path+path, 'rb') as f:
            return pickle.load(f)
    else:
        raise ValueError(f"Projection at {projection_path+path} doesn't exist.")

def save_figure(path, overwrite=False):
    path = figure_path + path 
    if overwrite:
        plt.savefig(path, bbox_inches="tight")
    else:
        if not os.path.exists(path):
            plt.savefig(path, bbox_inches="tight")

def load_movie_titles():
    # Loading dicts of nodes:movie titles and movie titles:nodes
    with open(raw_data_path+"movie-titles.txt", 'r', encoding='latin') as f:
            title_dict =  dict()
            node_dict = dict()
            for line in f.readlines():
                movieid, title = line.strip().split('|')[:2]
                movieid = int(movieid)
                title_dict[movieid] = title
                node_dict[title] = movieid
    return title_dict, node_dict

def load_raw_bipartite(overwrite=False):
    if not overwrite and os.path.exists(bipartite_path+"full_bipartite.p"):
        with open(bipartite_path+"full_bipartite.p", 'rb') as f:
            G = pickle.load(f)
        print("Graph loaded.")
    else:
        G = nx.Graph()
        # Loading edges
        with open(raw_data_path+"rel.rating.csv", 'r', encoding='UTF-8') as f:
            for line in f.readlines():
                userid, movieid, rating, timestamp = tuple(map(int, line.strip().split(' ')))
                userid += 10000
                G.add_node(userid)
                G.add_node(movieid, title=title_dict[movieid])
                G.add_edge(userid, movieid, weight=rating)  # Discarding the timestamp attribute of edges

        # Saving graph as pickle file
        with open(bipartite_path+"full_bipartite.p", 'wb', encoding='UTF-8') as f:
            pickle.dump(G, f)
        print("Graph created and saved.")
    return G   