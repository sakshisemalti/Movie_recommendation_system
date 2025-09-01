import streamlit as st
import pickle
import pandas as pd

# Load data
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# Recommend function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        if 'poster' in movies.columns:
            recommended_posters.append(movies.iloc[i[0]].poster)
        else:
            recommended_posters.append("https://via.placeholder.com/200x300?text=No+Poster")
    return recommended_movies, recommended_posters


# -------------------- Streamlit UI --------------------

st.title("🎬 Movie Recommendation System")

selected_movie_name = st.selectbox(
    "Choose a movie to get recommendations:",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], width=150)
            st.caption(names[i])

