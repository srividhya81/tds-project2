from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["OPTIONS", "POST"],
    allow_headers=["*"],
)

# Load the pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

@app.post("/api")
def handle_api_request(question: str = Form(...), file: UploadFile = File(None)):
    try:
        # Calculate similarity between the question and function descriptions using embeddings
        question_embedding = model.encode(question)
        function_embeddings = model.encode(function_descriptions)
        cosine_similarities = cosine_similarity([question_embedding], function_embeddings).flatten()
        most_similar_function_index = cosine_similarities.argmax()
        most_similar_function = list(functions_dict.values())[most_similar_function_index]

        # Call the most similar function
        if file:
            return most_similar_function(file=file, question=question)
        else:
            return most_similar_function(question=question)
    except Exception as e:
        return {"error": str(e)}

# Register functions
functions_dict = {
    "compute_similarity": lambda **kwargs: {"api_link": "http://127.0.0.1:8000/similarity"},
    "execute_query": lambda **kwargs: {"api_link": "http://127.0.0.1:8000/execute"}
}

function_descriptions = [
    "Compute similarity between documents and a query",
    "Execute a query and return the result"
]