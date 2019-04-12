import numpy as np
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
'''
Get recommendations for the groups
Based on age and Occupation
Merged with other users in the view
'''

def group_rec(age,occupation):
    users = pd.read_csv("data/users.csv")
    ratings = pd.read_csv("data/ratings.csv")
    movies = pd.read_csv("data/movies.csv")
    ratings2 = pd.merge(movies, ratings, on = 'movieId')
    information = pd.merge(ratings2, users, on='userId')
    user_demo = information.loc[(information.Occupation == occupation)&(information.rating >= 2.5)&(information.Age == age)]
    movie_data = pd.merge(ratings, movies, on='movieId')
    movie_data.groupby('title')['rating'].mean().sort_values(ascending=False)
    ratings_mean_count = pd.DataFrame(movie_data.groupby('title')['rating'].mean())
    ratings_mean_count['rating_counts'] = pd.DataFrame(movie_data.groupby('title')['rating'].count())
    user_avg_rating = pd.DataFrame(user_demo.groupby('title')['rating'].mean())
    user_avg_rating['count_ratings'] = user_demo.groupby('title')['rating'].count()
    hundred_most_voted = user_avg_rating.sort_values('count_ratings', ascending=False).head(50)
    top_10 = hundred_most_voted.sort_values('rating', ascending=False).head(20)
    return top_10
