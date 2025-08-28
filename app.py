import streamlit as st
import pickle

# --- Load preprocessed data ---
movies = pickle.load(open("notebooks/movies.pkl", "rb"))
similarity = pickle.load(open("notebooks/similarity.pkl", "rb"))

# --- Fill missing posters with placeholder ---
movies['poster_url'] = movies['poster_url'].fillna(
    "https://via.placeholder.com/500x750.png?text=No+Poster"
)

# --- Recommendation function ---
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        return [], []  # movie not found
    
    distances = similarity[index]
    movie_list_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list_indices:
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(movies.iloc[i[0]].poster_url)

    return recommended_movies, recommended_posters

# --- Streamlit UI ---
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommendation System")

movie_list = movies['title'].values
selected_movie = st.selectbox("Select a movie:", movie_list)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)
    
    if not names:
        st.warning("Movie not found or no recommendations available!")
    else:
        # Display recommendations in 5 columns
        cols = st.columns(5)
        for col, name, poster in zip(cols, names, posters):
            with col:
                st.image(poster, caption=name, use_container_width=True)
