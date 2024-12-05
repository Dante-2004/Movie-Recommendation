import psycopg2
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify

# Database connection settings
DB_SETTINGS = {
    "host": "localhost",
    "database": "moviesdb",
    "user": "postgres",
    "password": "2004"
}

# Connect to the database and fetch movie data
def fetch_movies():
    conn = psycopg2.connect(**DB_SETTINGS)
    query = "SELECT movie_id, title, tags FROM movies;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Generate recommendations
def get_recommendations(movie_title, movies_df):
    # Combine tags and convert to a vector
    vectorizer = CountVectorizer(stop_words='english')
    count_matrix = vectorizer.fit_transform(movies_df['tags'])

    # Compute cosine similarity
    cosine_sim = cosine_similarity(count_matrix)

    # Get the index of the movie
    idx = movies_df[movies_df['title'] == movie_title].index[0]

    # Get similarity scores for all movies
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get top 10 similar movies
    top_movies = [movies_df.iloc[i[0]]['title'] for i in sim_scores[1:11]]
    return top_movies

# Flask App
app = Flask(__name__)

@app.route("/recommend", methods=["GET"])
def recommend():
    movie_title = request.args.get("movie")
    movies_df = fetch_movies()
    
    if movie_title not in movies_df['title'].values:
        return jsonify({"error": "Movie not found in database."})

    recommendations = get_recommendations(movie_title, movies_df)
    return jsonify({"recommendations": recommendations})

if __name__ == "__main__":
    app.run(debug=True)
