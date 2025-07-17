

from fastapi import FastAPI, HTTPException
from typing import List
from models import Todo
import httpx

app = FastAPI()

DB_URL = "http://db:8004/todos"
NOTIFY_URL = "http://notification-agent:8002/notify"

@app.get("/")
def read_root():
    return {"message": "Task Runner is running"}

@app.get("/todos", response_model=List[Todo])
async def get_todos():
    async with httpx.AsyncClient() as client:
        r = await client.get(DB_URL)
        return r.json()

@app.post("/todos", response_model=Todo)
async def create_todo(todo: Todo):
    async with httpx.AsyncClient() as client:
        r = await client.post(DB_URL, json=todo.dict())
        # Trigger notification after creation
        await client.get(NOTIFY_URL)
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        return r.json()

@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{DB_URL}/{todo_id}")
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        return r.json()

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, updated: Todo):
    async with httpx.AsyncClient() as client:
        r = await client.put(f"{DB_URL}/{todo_id}", json=updated.dict())
        # Trigger notification after update
        await client.get(NOTIFY_URL)
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        return r.json()

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.delete(f"{DB_URL}/{todo_id}")
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        return r.json()
