# 🎬 Movie Recommendation System

A **content-based Movie Recommendation System** built using Python, Scikit-learn, and Streamlit.  
The system recommends movies similar to a selected title and also allows filtering by **genre** and **rating**, displaying **posters** for a visually rich user experience.

## Features

- **Movie Title Recommendation:**  
  - Select a movie from the search bar to get **top 5 similar movies**.  
  - Recommendations include **posters, genres, and ratings**.  

- **Genre & Rating Filtering:**  
  - Filter movies by multiple genres.  
  - Select **minimum rating** using **star-based ratings (1–5⭐)**.  
  - Displays **top-rated movies matching the filters**.  

- **Content-Based Filtering:**  
  - Uses **TF-IDF vectorization** and **Cosine Similarity** on movie **overview, genres, keywords, cast, and crew**.  

- **Pickle Integration:**  
  - Preprocessed movie dataset (`movies.pkl`) and similarity matrix (`similarity.pkl`) for faster load times.

## Tech Stack

- **Python 3.9+**  
- **Pandas / NumPy** → Data preprocessing  
- **Scikit-learn** → TF-IDF & Cosine Similarity  
- **Streamlit** → Interactive web interface  
- **Pickle** → Save/load preprocessed datasets  
- **Dataset** → Kaggle TMDb 5k Movies + Poster dataset  

## Contributions
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

MIT License  

## Acknowledgements
- The Movie Database (TMDb)
- Kaggle Datasets
- Streamlit community

