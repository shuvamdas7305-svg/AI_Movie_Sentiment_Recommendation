import pandas as pd
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager

# Global variables to hold model artifacts and database safely in RAM
vectorizer = None
model = None
movies_df = None


# 1. LIFESPAN MANAGEMENT (LOAD MODEL ARTIFACTS)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Safely handles loading the trained model artifacts and database 
    into memory on server boot.
    """
    global vectorizer, model, movies_df
    print("⏳ System Booting: Loading NLP Artifacts and Movie Database...")
    
    try:
        # Load your exact exported binaries from your Jupyter notebook
        vectorizer = joblib.load('vectorizer.pkl')
        model = joblib.load('sentiment_model.pkl')
        
        # Load your movie dataset for the genre recommendation logic
        movies_df = pd.read_csv('movies_dataset.csv')
        
        print("✅ Success: All Movie Analysis components successfully loaded into memory!")
    except FileNotFoundError as e:
        print(f"❌ Critical File Missing! Detail: {e}")
        print("Please verify vectorizer.pkl, sentiment_model.pkl, and movies_dataset.csv are in this root folder.")
    except Exception as e:
        print(f"❌ Unexpected Error during startup: {str(e)}")
        
    yield
    print("🧹 Shutting down movie prediction server context...")



# 2. INITIALIZE FASTAPI

app = FastAPI(
    title="AI Movie Sentiment & Recommendation Engine",
    description="FastAPI production backend parsing movie reviews and routing content recommendations.",
    version="2.0.0",
    lifespan=lifespan
)



# 3. PYDANTIC SCHEMAS

class ReviewInput(BaseModel):
    review: str

    class Config:
        json_schema_extra = {
            "example": {
                "review": "An absolute cinematic masterpiece! The acting was legendary and the storyline was flawless."
            }
        }



# 4. API ENDPOINTS

@app.get("/")
def health_check():
    """Simple status check probe."""
    return {
        "status": "online",
        "project": "AI Movie Sentiment & Recommendation System",
        "engine_ready": (vectorizer is not None and model is not None and movies_df is not None)
    }


@app.post("/predict")
def predict_review_sentiment(payload: ReviewInput):
    """
    Vectorizes raw text with TF-IDF and maps classification outputs.
    """
    if vectorizer is None or model is None:
        raise HTTPException(status_code=503, detail="Machine learning engine artifacts not found or loaded.")
    
    if not payload.review.strip():
        raise HTTPException(status_code=400, detail="Review string content cannot be blank.")
        
    try:
        # 1. Transform raw text through the loaded TF-IDF Vectorizer
        vectorized_text = vectorizer.transform([payload.review])
        
        # 2. Generate Binary Class Prediction (0 = Negative, 1 = Positive)
        prediction_code = int(model.predict(vectorized_text)[0])
        
        # 3. Calculate exact prediction confidence metrics
        probabilities = model.predict_proba(vectorized_text)[0]
        confidence_score = float(probabilities[prediction_code]) * 100
        
        sentiment_label = "Positive" if prediction_code == 1 else "Negative"
        
        return {
            "sentiment": sentiment_label,
            "confidence": round(confidence_score, 2),
            "prediction_code": prediction_code
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference pipeline failure: {str(e)}")


@app.get("/recommend")
def recommend_movies_by_genre(genre: str):
    """
    Queries movies_dataset.csv and extracts the top 3 highest-rated movies/series matching a genre string.
    """
    if movies_df is None:
        raise HTTPException(status_code=503, detail="Movie database layer unavailable.")
        
    try:
        # Case insensitive substring matching to catch complex lists like "Action, Crime"
        filtered_movies = movies_df[movies_df['genre'].str.contains(genre, case=False, na=False)]
        
        if filtered_movies.empty:
            return []
            
        # Extract top 3 highest-rated items
        top_matches = filtered_movies.sort_values(by='rating', ascending=False).head(3)
        
        recommendation_payload = []
        for _, row in top_matches.iterrows():
            recommendation_payload.append({
                "movie_title": row['movie_title'],
                "release_year": int(row['release_year']),
                "genre": row['genre'],
                "rating": float(row['rating']),
                "description": row['description']
            })
            
        return recommendation_payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation system error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)