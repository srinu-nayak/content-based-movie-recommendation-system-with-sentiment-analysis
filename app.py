import os
import pickle
import streamlit as st
import requests
import gdown

def download_file_gdown(file_id, destination):
    url = f"https://drive.google.com/uc?id={file_id}"
    if not os.path.exists(destination):
        st.write(f"Downloading {destination}...")
        gdown.download(url, destination, quiet=False)
    else:
        st.write(f"{destination} already exists, skipping download.")

def load_pickle_from_file(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return "https://via.placeholder.com/500x750?text=No+Image"

MOVIE_LIST_FILE_ID = "1Y5e7JoNp5ALDWD7ZMrg8yZvX2pZ0YVLB"
SIMILARITY_FILE_ID = "1VnMEoCqrlP2FC-UIq7L3PX34coOsRvW0"

MOVIE_LIST_PATH = "movie_list.pkl"
SIMILARITY_PATH = "similarity.pkl"

download_file_gdown(MOVIE_LIST_FILE_ID, MOVIE_LIST_PATH)
download_file_gdown(SIMILARITY_FILE_ID, SIMILARITY_PATH)

movies = load_pickle_from_file(MOVIE_LIST_PATH)
similarity = load_pickle_from_file(SIMILARITY_PATH)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

st.header('🎬 Movie Recommender System')

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
