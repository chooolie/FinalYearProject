#this is something that will work in future when there are users that have voted on movies
#can only show it working based on current user data i have acquired
#At the moment, this will not be helpful unless a user is to make ratings.

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

ratings = pd.read_csv("ratings.csv")
movies = pd.read_csv("movies.csv")
ratings = pd.merge(ratings, movies, on='movieId')

#get the average rating for each movie and add to DF avg_rating
avg_rating = pd.DataFrame(ratings.groupby('movieId')['rating'].mean())
#Get count of ammount of votes per movie and add to DF
avg_rating['count_ratings'] = ratings.groupby('movieId')['rating'].count()


def similar_user(user):
    #merge ratings and movies
    ratings = pd.read_csv("ratings.csv")
    movies = pd.read_csv("movies.csv")
    ratings = pd.merge(ratings, movies, on='movieId')
    ratings_matrix = ratings.pivot_table(index='title', columns='userId', values='rating')
    user_id = ratings_matrix[user]
    similar_to=ratings_matrix.corrwith(user_id)
    correlation = pd.DataFrame(similar_to, columns=['Correlation'])
    correlation.dropna(inplace=True)
    correlation = correlation.join(avg_rating['count_ratings'])
    similar_movies = correlation[correlation['count_ratings'] > 1].sort_values(by='Correlation', ascending=False).head(5)
    return similar_movies

def users_faves(user):
    ratings = pd.read_csv("ratings.csv")
    user_demo = ratings.loc[(ratings.userId == user)].sort_values(by=['rating'], ascending=False).head(4)
    #return 5 most similar users based on ratings
    return user_demo

def get_movies(user):
    sim = similar_user(user)
    sim = sim.iloc[:,0:0]

    all_movies = []
    for col in sim.iterrows():
        all_movies.append(users_faves(col[0]))

    top_movies = []

    user1 =all_movies[0]
    top_movies.extend(user1['movieId'].values.tolist())
    user2 = all_movies[1]
    top_movies.extend(user2['movieId'].values.tolist())
    user3 = all_movies[2]
    top_movies.extend(user3['movieId'].values.tolist())
    user4 = all_movies[3]
    top_movies.extend(user4['movieId'].values.tolist())
    user5 = all_movies[4]
    top_movies.extend(user5['movieId'].values.tolist())

    return top_movies

#send in users id
all_movies = get_movies(400)
all_movies
