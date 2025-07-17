from fastapi import FastAPI
import httpx
from transformers import pipeline

app = FastAPI()

# Load a small HuggingFace model for recommendations (summarization as example)
recommender = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

DB_URL = "http://db:8004/todos"

@app.get("/")
def read_root():
    return {"message": "Recommendation Agent is running"}

@app.get("/recommend")
async def recommend():
    async with httpx.AsyncClient() as client:
        r = await client.get(DB_URL)
        todos = r.json()
    if not todos:
        return {"recommendation": "No todos found."}
    # Use LLM to prioritize tasks (simple prompt)
    todo_descriptions = "; ".join([f"{t.get('title','')}: {t.get('description','')}" for t in todos])
    prompt = f"Given these tasks, which should the user prioritize and why? {todo_descriptions}"
    result = recommender(prompt, max_length=40, min_length=10, do_sample=False)[0]["summary_text"]
    return {"recommendation": result}
