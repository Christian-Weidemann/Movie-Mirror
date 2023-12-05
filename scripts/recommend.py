import networkx as nx
from statistics import mean

def get_edges(liked_movie_list,d_graph):
    liked_movie_node_list = [node_dict[liked_movie_title] for liked_movie_title in liked_movie_list]
    edges = dict((liked_movie_node, list(d_graph.edges(liked_movie_node, data=True))) for liked_movie_node in liked_movie_node_list)
    return edges

def get_average_weight_per_movie(edges):
    node_weights = dict()
    for node, edges_list in edges.items():
        for edge in edges_list:
            if edge[1] in edges.keys():
                continue
            if edge[1] in node_weights:
                node_weights[edge[1]].append(edge[2]['weight'])
            else:
                node_weights[edge[1]] = [edge[2]['weight']]
        average_weights = [(node,mean(weights)) for node, weights in node_weights.items()]
    return average_weights

def sort_average_weight(average_weight_edges):
    return sorted(average_weight_edges, reverse=True, key=lambda x: x[1])

def k_recommend_from_list(k, movie_graph, liked_movie_list):
    # Checking that types are correct
    if type(k) != int or type(movie_graph) not in [nx.Graph, nx.DiGraph] or type(liked_movie_list) != list:
        raise TypeError(f"Argument(s) have wrong type: {type(k)}, {type(movie_graph)}, {type(liked_movie_list)}.")
    edges = get_edges(liked_movie_list, movie_graph)
    sorted_average_weights = sort_average_weight(get_average_weight_per_movie(edges))
    n_neighbors = [(title_dict[neighbor],weight) for neighbor, weight in sorted_average_weights][:k]
    return n_neighbors

    
def evaluation_recommendation(movie_graph, liked_movie_list, rated_movies):
    """
    Returns neighbor nodes sorted by average weight
    """
    # Checking that types are correct
    if type(movie_graph) not in [nx.Graph, nx.DiGraph] or type(liked_movie_list) != list:
        raise TypeError(f"Argument(s) have wrong type: {type(movie_graph)}, {type(liked_movie_list)}.")
    
    # Considering only edges from liked movies to rated movies
    edges = dict()
    for liked_movie_node in liked_movie_list:
        edges[liked_movie_node] = [edge for edge in movie_graph.edges(liked_movie_node, data=True) if edge[1] in rated_movies]

    sorted_average_weights = sort_average_weight(get_average_weight_per_movie(edges))
    return [movie_node for movie_node, weight in sorted_average_weights]
    