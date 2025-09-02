import streamlit as st
import pickle
import pandas as pd

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="🎬 Movie Recommender",page_icon="🎬",layout="wide")

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data():
    movies = pickle.load(open('notebooks/movies.pkl','rb'))
    similarity = pickle.load(open('notebooks/similarity.pkl','rb'))
    # Fix column names just in case
    movies.columns = [c.replace("'", "").strip() for c in movies.columns]
    return movies, similarity

movies, similarity = load_data()

# -------------------- UI STYLING --------------------
st.markdown("""
    <style>
        div.stButton > button:first-child {
            background-color: #99ccff;
            color:black;
            font-size:16px;
            border-radius:10px;
            height:50px;
            width:250px;
        }
        div.stButton > button:hover {
            background-color: #f3f6f4;
            color:black;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <h1 style='text-align: center; color: #b3d9ff; font-family: "Comic Sans MS", cursive, sans-serif; font-size:48px'>
        🎬 Movie Recommendation System
    </h1>
    <p style='text-align: center; color: #f3f6f4; font-size:18px'>
        Recommendations by Movie Title
    </p>
    <hr style='border: 2px solid #b3d9ff'>
""", unsafe_allow_html=True)

# -------------------- RECOMMEND FUNCTION --------------------
def recommend(movie):
    if movie not in movies['title'].values:
        return [], []

    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i, _ in movies_list:
        recommended_movies.append(movies.iloc[i].title)
        recommended_posters.append(movies.iloc[i].poster)
    return recommended_movies, recommended_posters

# -------------------- MOVIE SELECTION --------------------
selected_movie_name = st.selectbox(
    "Choose a movie:",
    movies['title'].values,
    index=None,
    placeholder="Type to search..."
)

if st.button("Recommend") and selected_movie_name:
    names, posters = recommend(selected_movie_name)
    if names:
        st.subheader(f"Top Recommendations for '{selected_movie_name}'")
        cols = st.columns(5)
        for i, (name, poster) in enumerate(zip(names, posters)):
            with cols[i % 5]:
                vote = movies[movies['title']==name]['vote_average'].values[0]
                st.markdown(f"""
                    <div style='background-color:#000000; padding:10px; border-radius:10px; text-align:center'>
                        <img src="{poster}" width="150">
                        <p style='color:#f3f6f4; font-weight:bold;'>⭐ {vote:.1f}</p>
                        <p style='color:#f3f6f4; font-weight:bold;'>{name}</p>
                    </div>
                """, unsafe_allow_html=True)
