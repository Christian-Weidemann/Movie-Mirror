# Split the graph into 2 sets: user and movie nodes
user_nodes, movie_nodes = nx.algorithms.bipartite.basic.sets(G)

# Generate the weighted projections
weighted_projection_users = bipartite.weighted_projected_graph(G, user_nodes)
weighted_projection_movie = bipartite.weighted_projected_graph(G, movie_nodes)

# How many movies each user has rated
# Compute degree centrality for the users projection
degree_centrality_users = nx.degree_centrality(weighted_projection_users)

# Print the degree centrality for each node in the users projection
# print("Degree centrality for users:")
# for node, centrality in users_degree_centrality.items():
    # print(f"Node {node}: {centrality}")

# Calculate the degree centrality of each movie (why are they so high?!) (How many ratings per movie)

# Compute degree centrality for the movie projection
degree_centrality_movies = nx.degree_centrality(weighted_projection_movie)

# Print the degree centrality for each node in the movie projection
# print("Degree centrality for movies:")
# for node, centrality in movie_degree_centrality.items():
#     print(f"Node {node}: {centrality}")

# The most infuelncial user (max degree centrality), movie popularity (max degree centrality)

# Find the user with the highest degree centrality
most_influential_user = max(degree_centrality_users, key=degree_centrality_users.get)
centrality_value_user = degree_centrality_users[most_influential_user]

# Add the 1000 to user ID
most_influential_user += 10240

print(f"The most influential user is {most_influential_user} with degree centrality {centrality_value_user}")


# Find the movie with the highest degree centrality
most_rated_movie = max(degree_centrality_movies, key=degree_centrality_movies.get)
centrality_value_movie = degree_centrality_movies[most_rated_movie]

print(f"The most rated movie is {most_rated_movie} with degree centrality {centrality_value_movie}")

# Followed Marie's way of getting the projection and it gets the same results, since the reuslts up there were suspicious 

# Followed Marie's nodes from the exercises to get the degree centrality,since the achieved results looked suspicious.
# Split the graph into 2 sets: user and movie nodes
#user_nodes, movie_nodes = nx.algorithms.bipartite.basic.sets(G)
nodes = nx.algorithms.bipartite.basic.sets(G)

# turn the bipartite network into an adjacency matrix
adjmat_user = nx.algorithms.bipartite.matrix.biadjacency_matrix(G, nodes[1])
adjmat_movie = nx.algorithms.bipartite.matrix.biadjacency_matrix(G, nodes[0])

# we then use the simple weighting method to get the weighted projection 
#projected_users = adjmat_users.dot(adjmat_user.T)
#print(projected_users)
#In your example, the entry (0, 486) 10 
# indicates that user 0 is connected to user 486 with a strength of 10.


projected_movies = adjmat_movies.dot(adjmat_movies.T) 

#Create weighted graphs from the weighted adjacency matrices
#G_users = nx.Graph(projected_users)
G_movies = nx.Graph(projected_movies)

# Step 2: Calculate degree centrality for users and movies
#degree_centrality_users = nx.degree_centrality(G_users)
degree_centrality_movies = nx.degree_centrality(G_movies)

# Print the degree centrality for users
#for user, centrality in degree_centrality_users.items():
    #print(f"User {user} has degree centrality: {centrality}")

# Print the degree centrality for movies
# for movie, centrality in degree_centrality_movies.items():
#     print(f"Movie {movie} has degree centrality: {centrality}")
