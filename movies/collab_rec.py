import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import csr_matrix
from mpl_toolkits.axes_grid1 import make_axes_locatable
from sklearn.cluster import KMeans
'''
https://github.com/gouravaich/k-means-clustering-movie-ratings/blob/master/k-means%20Clustering%20of%20Movie%20Ratings.ipynb
'''
###Practicing getting clustering working =>
###Ended up not being used

def users_top_rating(top_movies, max):
    ## Get the rop rated movies - max is ammount sent in
    top_movies['counts'] = pd.Series(top_movies.count(axis=1))
    top_movies_users = top_movies.sort_values('counts', ascending=False)
    top_movies_users_selection = top_movies_users.iloc[:max, :]
    top_movies_users_selection = top_movies_users_selection.drop(['counts'], axis=1)

    return top_movies_users_selection

def highest_rated_movie(user_ratings, max_ratings):
    user_ratings = user_ratings.append(user_ratings.count(), ignore_index=True)
    user_ratings_sorted = user_ratings.sort_values(len(user_ratings)-1, axis=1, ascending=False)
    user_ratings_sorted = user_ratings_sorted.drop(user_ratings_sorted.tail(1).index)
    top_movies = user_ratings_sorted.iloc[:, :max_ratings]
    return top_movies

def rating_density(user_movie_ratings, n_movies, n_users):
    top_movies = highest_rated_movie(user_movie_ratings, n_movies)
    top_movies = users_top_rating(top_movies, n_users)
    return top_movies

def get_recommendation(users_id):

    movies = pd.read_csv('data/movies.csv')
    movies.head()
    ratings = pd.read_csv('data/ratings.csv')
    ratings.head()
    ratings = pd.merge(ratings, movies, on='movieId')
    ratings_matrix = ratings.pivot_table(index='userId', columns='title', values='rating')

    user_movie_ratings =  pd.pivot_table(ratings, index='userId', columns= 'title', values='rating')
    ##Send 2000 to get the top 2000 movies
    top_3thousand = highest_rated_movie(user_movie_ratings, 3000)
    sparse_ratings = csr_matrix(pd.SparseDataFrame(top_3thousand).to_coo())
    predictions = KMeans(n_clusters=2, algorithm='full').fit_predict(sparse_ratings)
    clustered = pd.concat([top_3thousand.reset_index(), pd.DataFrame({'group':predictions})], axis=1)
    cluster_number = 1
    #number of users = 600 - some users wont be able to use this function if they have not rated enough movies
    num_users = 610
    num_movies = 1000 # Only will show the top 1000 movies
    cluster = clustered[clustered.group == cluster_number].drop(['index', 'group'], axis=1)

    cluster = rating_density(cluster, num_movies, num_users)

    #user_2_ratings  = cluster.loc[user_id, :]
    user_2_ratings = cluster.iloc[cluster.index==users_id].T.squeeze()
    user_2_unrated_movies =  user_2_ratings[user_2_ratings.isnull()]
    avg_ratings = pd.concat([user_2_unrated_movies, cluster.mean()], axis=1, join='inner').loc[:,0]
    result = avg_ratings.sort_values(ascending=False)[:10]
    result = result.index.tolist()
    return user_2_ratings
