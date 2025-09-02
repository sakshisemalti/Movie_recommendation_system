import streamlit as st
import pickle
import pandas as pd

st.set_page_config(page_title="🎬 Genre & Rating Recommender", layout="wide")

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data():
    movies = pickle.load(open('notebooks/movies.pkl','rb'))
    similarity = pickle.load(open('notebooks/similarity.pkl','rb'))
    movies.columns = [c.replace("'", "").strip() for c in movies.columns]
    return movies, similarity

movies, similarity = load_data()

# -------------------- UI STYLING --------------------
st.markdown("""
    <style>
        /* Buttons */
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

# -------------------- HEADER --------------------
st.markdown("""
    <h1 style='text-align: center; color: #b3d9ff; font-family: "Comic Sans MS", cursive, sans-serif; font-size:48px'>
        🎬 Movie Recommendation System
    </h1>
    <p style='text-align: center; color: #f3f6f4; font-size:18px'>
        Recommendations by Genre & Rating
    </p>
    <hr style='border: 2px solid #b3d9ff'>
""", unsafe_allow_html=True)

# -------------------- FILTERS --------------------
all_genres = sorted({g for sublist in movies['genres'] for g in sublist})
selected_genres = st.multiselect("Filter by Genre", all_genres)

# Star-based rating filter
rating_options = [1, 2, 3, 4, 5]
min_rating_stars = st.selectbox("Minimum Rating ⭐", rating_options, index=0)
min_rating_value = min_rating_stars * 2  # Scale to 0–10 TMDB rating
st.markdown(f"<span style='color:#FFD700'>{'⭐'*min_rating_stars}</span>", unsafe_allow_html=True)

# -------------------- RECOMMEND FUNCTION --------------------
def recommend_filtered(selected_genres=None, min_rating=0):
    filtered_movies = movies.copy()
    if selected_genres:
        filtered_movies = filtered_movies[filtered_movies['genres'].apply(lambda x: any(g in x for g in selected_genres))]
    filtered_movies = filtered_movies[filtered_movies['vote_average'] >= min_rating]
    # Top 5 by rating
    top_movies = filtered_movies.sort_values(by='vote_average', ascending=False).head(5)
    return top_movies['title'].tolist(), top_movies['poster'].tolist()

# -------------------- BUTTON --------------------
if st.button("Recommend"):
    names, posters = recommend_filtered(selected_genres, min_rating_value)
    if names:
        st.subheader("Top Recommendations")
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
    else:
        st.warning("No movies found with the selected filters.")