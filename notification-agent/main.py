from fastapi import FastAPI
import httpx
from transformers import pipeline

app = FastAPI()

# Load a small HuggingFace model for notifications (summarization as example)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

DB_URL = "http://db:8004/todos"

@app.get("/")
def read_root():
    return {"message": "Notification Agent is running"}

@app.get("/notify")
async def notify():
    # Fetch todos from db service
    async with httpx.AsyncClient() as client:
        r = await client.get(DB_URL)
        todos = r.json()
    if not todos:
        return {"notification": "No todos found."}
    # Create a summary notification using the LLM
    todo_titles = ", ".join([t.get("title", "") for t in todos])
    prompt = f"Summarize these tasks for a notification: {todo_titles}"
    summary = summarizer(prompt, max_length=30, min_length=5, do_sample=False)[0]["summary_text"]
    return {"notification": summary}
