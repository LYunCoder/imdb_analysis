import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy as np

def clean_review(review):
    """
    Removes punctuations, stopwords and returns an array of words
    """
    review = review.replace('!', ' ')
    review = review.replace('?', ' ')
    review = review.replace(':', ' ')
    review = review.replace(';', ' ')
    review = review.replace(',', ' ')
    tokens = word_tokenize(review)
    tokens = [w for w in tokens if w not in stopwords.words('english')]
    return tokens

class Indexer:
    """
    Class to load imdb data from file and obtain relevant data structures
    """
    def __init__(self):
        """
        Constructor
        """
        self.reviews = list()

    def read_file(self, filename):
        """
        Reads reviews from a specified file
        """
        f = open(filename)
        data = f.read()
        self.reviews = json.loads(data)

    def get_mappings(self):
        """
        Returns relevant data like vocab size, user list, etc after
        processing review data
        """
        user_dict = dict()
        movie_dict = dict()
        for review in self.reviews:
            user = review['user']
            if user not in user_dict:
                nu = len(user_dict.keys())
                user_dict[user] = nu
            movie = review['movie']
            if movie not in movie_dict:
                nm = len(movie_dict.keys())
                movie_dict[movie] = nm
        nu = len(user_dict.keys())
        user_list = [''] * nu
        for user in user_dict:
            idx = user_dict[user]
            user_list[idx] = user
        nm = len(movie_dict.keys())
        movie_list = [''] * nm
        for movie in movie_dict:
            idx = movie_dict[movie]
            movie_list[idx] = movie 
        rating_matrix = np.zeros((nu, nm))
        for review in self.reviews:
            user = review['user']
            movie = review['movie']
            u_idx = user_dict[user]
            m_idx = movie_dict[movie]
            rating_matrix[u_idx][m_idx] = review['rating']
        dictionary = dict()
        review_matrix = list()
        longest_movie_id = 0
        longest_user_id = 0
        longest_title = 0
        longest_review = 0
        longest_link = 0
        for review in self.reviews:
            temp = review['review']
            #arr = clean_review(temp)
            #compute the number of the longest review added on 2018/12/17
            review_temp = review['review']
            user_temp = review['user']
            movie_temp = review['movie']
            title_temp = review['title']
            link_temp = review['link']
            if longest_movie_id<len(movie_temp):
                longest_movie_id = len(movie_temp)
            if longest_user_id<len(user_temp):
                longest_user_id = len(user_temp)
            if longest_title<len(title_temp):
                longest_title = len(title_temp)
            if longest_review<len(review_temp):
                longest_review = len(review_temp)
            if longest_link<len(link_temp):
                longest_link = len(link_temp)
            #end
            arr = temp.split()
            review_matrix.append(arr)
            for ar in arr:
                ar = ar.strip()
                if ar not in dictionary:
                    dictionary[ar] = 1 
        vocab_size = len(dictionary.keys())
        review_matrix = np.array(review_matrix)
        review_map = list()
        for review in self.reviews:
            review_map.append(
            {
                'user' : review['user'],
                'movie' : review['movie']
            })
        return (vocab_size, user_list, movie_list, rating_matrix, review_matrix, review_map, 
                longest_movie_id, longest_user_id, longest_title, longest_review, longest_link)# -*- coding: utf-8 -*-

