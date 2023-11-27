import matplotlib.pyplot as plt
import pickle
import networkx as nx
import os

# Path variables
raw_data_path = "data/raw/"
figure_path = "data/figures/"
bipartite_path = "data/bipartite/"
projection_path = "data/projections/"

def save_edgelist(k, graph, file_path, overwrite=False):
    """
    Save a NetworkX graph with weights as an edge list at the specified file path.
    Import into gephi with Data Laboratory > Import Spreadsheet.
    """
    if overwrite or not os.path.exists(projection_path+file_path):

        k_highest_weight_edges = sorted([(u,v,attr['weight']) for u,v,attr in graph.edges(data=True)], reverse=True, key=lambda x:x[2])[:k]

        with open(projection_path+file_path, 'w') as file:
            file.write(f"Source,Target,Weight\n")
            for u, v, weight in k_highest_weight_edges:
                file.write(f"{u},{v},{weight}\n")
        print("Edgelist saved.")

def save_projection(G, path, overwrite=False):
    if overwrite or not os.path.exists(projection_path+path):
        with open(projection_path+path, 'wb') as f:
            pickle.dump(G, f)
        print("Projection saved.")

def load_projection(path):
    if os.path.exists(projection_path+path):
        with open(projection_path+path, 'rb') as f:
            print("Projection loaded.")
            return pickle.load(f)
    else:
        raise ValueError(f"Projection at {projection_path+path} doesn't exist.")

def save_figure(path, overwrite=False):
    if overwrite or not os.path.exists(figure_path+path):
        plt.savefig(figure_path+path, bbox_inches="tight")
        print("Figure saved.")

def load_movie_titles(path):
    # Loading dicts of nodes:movie titles and movie titles:nodes
    with open(raw_data_path+path, 'r', encoding='latin') as f:
            title_dict =  dict()
            node_dict = dict()
            for line in f.readlines():
                movieid, title = line.strip().split('|')[:2]
                movieid = int(movieid)
                title_dict[movieid] = title
                node_dict[title] = movieid
    return title_dict, node_dict

def load_raw_bipartite(path, overwrite=False):
    if not overwrite and os.path.exists(bipartite_path+path):
        with open(bipartite_path+path, 'rb') as f:
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
                G.add_node(movieid)
                G.add_edge(userid, movieid, weight=rating)  # NOTE: Not adding the timestamp attribute of edges

        # Saving graph as pickle file
        with open(bipartite_path+path, 'wb') as f:
            pickle.dump(G, f)
        print("Graph created and saved.")
    return G   