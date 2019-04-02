import pandas as pd
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from scipy.spatial.distance import cosine


def age_occupation(age,occupation):
    users = pd.read_csv("data/users.csv")
    ratings = pd.read_csv("data/ratings.csv")
    movies = pd.read_csv("data/movies.csv")
    ratings2 = pd.merge(movies, ratings, on = 'movieId')
    information = pd.merge(ratings, users, on='userId')
    user_demo = information.loc[(information.Occupation == occupation)&(information.rating >= 2.5)&(information.Age == age)]
    movie_data = pd.merge(ratings, movies, on='movieId')
    ratings_mean_count = pd.DataFrame(movie_data.groupby('title')['rating'].mean())
    ratings_mean_count['rating_counts'] = pd.DataFrame(movie_data.groupby('title')['rating'].count())
    user_avg_rating = pd.DataFrame(user_demo.groupby('movieId')['rating'].mean())
    user_avg_rating['count_ratings'] = user_demo.groupby('movieId')['rating'].count()
    hundred_most_voted = user_avg_rating.sort_values('count_ratings', ascending=False).head(50)
    top_10 = hundred_most_voted.sort_values('rating', ascending=False).head(10)
    links = pd.read_csv("data/links.csv")
    sim = pd.merge(top_10, links, on='movieId')
    sim = pd.merge(sim, movies, on='movieId')
    sim = sim.values
    return sim

def gender_age(age,gender):
    users = pd.read_csv("data/users.csv")
    ratings = pd.read_csv("data/ratings.csv")
    movies = pd.read_csv("data/movies.csv")
    ratings2 = pd.merge(movies, ratings, on = 'movieId')
    information = pd.merge(ratings, users, on='userId')
    user_demo = information.loc[(information.Gender == gender)&(information.rating >= 2.5)&(information.Age == age)]
    movie_data = pd.merge(ratings, movies, on='movieId')
    ratings_mean_count = pd.DataFrame(movie_data.groupby('title')['rating'].mean())
    ratings_mean_count['rating_counts'] = pd.DataFrame(movie_data.groupby('title')['rating'].count())
    user_avg_rating = pd.DataFrame(user_demo.groupby('movieId')['rating'].mean())
    user_avg_rating['count_ratings'] = user_demo.groupby('movieId')['rating'].count()
    hundred_most_voted = user_avg_rating.sort_values('count_ratings', ascending=False).head(50)
    top_10 = hundred_most_voted.sort_values('rating', ascending=False).head(10)
    links = pd.read_csv("data/links.csv")
    sim = pd.merge(top_10, links, on='movieId')
    sim = pd.merge(sim, movies, on='movieId')
    sim = sim.values
    return sim



def gender_occupation(gender,occupation):
    users = pd.read_csv("data/users.csv")
    ratings = pd.read_csv("data/ratings.csv")
    movies = pd.read_csv("data/movies.csv")
    ratings2 = pd.merge(movies, ratings, on = 'movieId')
    information = pd.merge(ratings, users, on='userId')
    user_demo = information.loc[(information.Occupation == occupation)&(information.rating >= 3)&(information.Gender == gender)]
    movie_data = pd.merge(ratings, movies, on='movieId')
    ratings_mean_count = pd.DataFrame(movie_data.groupby('title')['rating'].mean())
    ratings_mean_count['rating_counts'] = pd.DataFrame(movie_data.groupby('title')['rating'].count())
    user_avg_rating = pd.DataFrame(user_demo.groupby('movieId')['rating'].mean())
    user_avg_rating['count_ratings'] = user_demo.groupby('movieId')['rating'].count()
    hundred_most_voted = user_avg_rating.sort_values('count_ratings', ascending=False).head(50)
    top_10 = hundred_most_voted.sort_values('rating', ascending=False).head(10)
    links = pd.read_csv("data/links.csv")
    sim = pd.merge(top_10, links, on='movieId')
    sim = pd.merge(sim, movies, on='movieId')
    sim = sim.values
    return sim

def SimilarMovies(Movie_Id):
    ratings = pd.read_csv("data/ratings.csv")
    movies = pd.read_csv("data/movies.csv")
    ratings = pd.merge(ratings, movies, on='movieId')
    avg_rating = pd.DataFrame(ratings.groupby('movieId')['rating'].mean())
    avg_rating['count_ratings'] = ratings.groupby('movieId')['rating'].count()
    ratings_matrix = ratings.pivot_table(index='userId', columns='movieId', values='rating')
    user_rating = ratings_matrix[Movie_Id]
    similar_to = ratings_matrix.corrwith(user_rating)
    corr = pd.DataFrame(similar_to, columns=['Correlation'])
    corr.dropna(inplace=True)
    corr = corr.join(avg_rating['count_ratings'])
    similar = corr[corr['count_ratings'] > 50].sort_values(by='Correlation', ascending=False).head(10)
    links = pd.read_csv("data/links.csv")
    sim = pd.merge(similar, links, on='movieId')
    sim = pd.merge(sim, movies, on='movieId')
    lists = sim['title'].values
    sim = sim.values
    return sim
