import pandas as pd
import difflib
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# Set up for serving static files (like CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up for serving HTML templates
templates = Jinja2Templates(directory="templates")

# Load movie data
movie_data = pd.read_csv('data/movies.csv')  # Update this path to your CSV file

selected_features = ['genres','keywords','tagline','cast','director']
print(selected_features)

for feature in selected_features:
    movie_data[feature] = movie_data[feature].fillna('')

combined_features = movie_data['genres'] + ' ' + movie_data['keywords'] + ' ' +movie_data['tagline'] + ' ' +movie_data['cast'] + ' ' + movie_data['director']



# Create the TF-IDF Vectorizer and fit it
vectorizer = TfidfVectorizer()
feature_vector = vectorizer.fit_transform(combined_features)

# Calculate cosine similarity
similarity_matrix = cosine_similarity(feature_vector)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/results", response_class=HTMLResponse)
async def get_results(request: Request, movie_name: str):
    try:
        # Debug: Print the movie name received
        print("Received movie name:", movie_name)

        # Normalize input
        movie_name = movie_name.lower()

        # Find the close match for the movie name
        list_all_titles = movie_data['title'].str.lower().tolist()  # Convert titles to lower case
        find_closematch = difflib.get_close_matches(movie_name, list_all_titles)

        # Debug: Print the close matches found
        print("Close matches found:", find_closematch)

        if not find_closematch:
            recommended_movies = ["No similar movie found."]
        else:
            closematch = find_closematch[0]

            # Debug: Print the close match
            print("Close match:", closematch)

            # Access the movie by matching title with lower case
            index_movie = movie_data[movie_data['title'].str.lower() == closematch]['index'].values

            # Check if index_movie has any values
            if len(index_movie) == 0:
                recommended_movies = ["No similar movie found."]
            else:
                index_movie = index_movie[0]  # Access the first element safely

                # Debug: Print the index of the matched movie
                print("Index of matched movie:", index_movie)

                # Get similarity scores
                similar_score = list(enumerate(similarity_matrix[index_movie]))
                # Sort movies based on similarity score
                sort_similar_movie = sorted(similar_score, key=lambda x: x[1], reverse=True)

                recommended_movies = []
                for movie in sort_similar_movie[1:31]:  # Get top 10 recommendations, skip the first (the movie itself)
                    index = movie[0]
                    title_from_index = movie_data['title'].iloc[index]  # Use iloc for safe access
                    recommended_movies.append(title_from_index)  # Collect recommended titles

        # Debug: Print the recommended movies
        print("Recommended movies:", recommended_movies)

        return templates.TemplateResponse("results.html", {"request": request, "movies": recommended_movies})

    except Exception as e:
        print("An error occurred:", e)
        return templates.TemplateResponse("results.html", {"request": request, "movies": ["Internal Server Error. Please try again later."]})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
