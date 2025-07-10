import requests
import streamlit as st
import pickle
import pandas as pd

# Load data
movies_dict = pickle.load(open(r"C:\Users\Gursimar Singh Phull\OneDrive\Desktop\moviesdict.pkl", 'rb'))
similarity = pickle.load(open(r"C:\Users\Gursimar Singh Phull\OneDrive\Desktop\similarity.pkl", 'rb'))
movies = pd.DataFrame(movies_dict)

# Function to fetch movie poster from TMDB
def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=3a2a4e61b259d44729b386403584cac2&language=en-US'.format(movie_id)
    )
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500' + data['poster_path']

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]]['id']


        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

# Streamlit app
st.title("Movie Recommending System")

# Dropdown to select a movie
selected_movie_name = st.selectbox(
    "Select a movie:",
    movies['title'].values
)

# Button to show recommendations
if st.button('Recommend', key='recommend_button'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
