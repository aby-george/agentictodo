
from fastapi import FastAPI, HTTPException
from typing import List
import json
import os
from transformers import pipeline

app = FastAPI()
DB_FILE = "todos.json"

# Load a small HuggingFace model for recommendations (summarization as example)
recommender = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def read_db():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)

def write_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.get("/todos", response_model=List[dict])
def get_todos():
    return read_db()

@app.post("/todos", response_model=dict)
def create_todo(todo: dict):
    todos = read_db()
    if any(t["id"] == todo["id"] for t in todos):
        raise HTTPException(status_code=400, detail="Todo with this ID already exists.")
    todos.append(todo)
    write_db(todos)
    return todo

@app.put("/todos/{todo_id}", response_model=dict)
def update_todo(todo_id: int, updated: dict):
    todos = read_db()
    for idx, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todos[idx] = updated
            write_db(todos)
            return updated
    raise HTTPException(status_code=404, detail="Todo not found.")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    todos = read_db()
    for idx, todo in enumerate(todos):
        if todo["id"] == todo_id:
            del todos[idx]
            write_db(todos)
            return {"detail": "Todo deleted."}
    raise HTTPException(status_code=404, detail="Todo not found.")

