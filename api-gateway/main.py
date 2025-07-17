NOTIFICATION_AGENT_URL = "http://notification-agent:8002/notify"

@app.get("/notify")
async def get_notification():
    async with httpx.AsyncClient() as client:
        r = await client.get(NOTIFICATION_AGENT_URL)
        return JSONResponse(status_code=r.status_code, content=r.json())

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import httpx
from typing import List

app = FastAPI()

TASK_RUNNER_URL = "http://task-runner:8001"
RECOMMENDATION_AGENT_URL = "http://recommendation-agent:8005/recommend"

@app.get("/")
def read_root():
    return {"message": "API Gateway is running"}

@app.get("/todos")
async def get_todos():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{TASK_RUNNER_URL}/todos")
        return JSONResponse(status_code=r.status_code, content=r.json())

@app.post("/todos")
async def create_todo(todo: dict):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{TASK_RUNNER_URL}/todos", json=todo)
        return JSONResponse(status_code=r.status_code, content=r.json())

@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{TASK_RUNNER_URL}/todos/{todo_id}")
        return JSONResponse(status_code=r.status_code, content=r.json())

@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, todo: dict):
    async with httpx.AsyncClient() as client:
        r = await client.put(f"{TASK_RUNNER_URL}/todos/{todo_id}", json=todo)
        return JSONResponse(status_code=r.status_code, content=r.json())


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.delete(f"{TASK_RUNNER_URL}/todos/{todo_id}")
        return JSONResponse(status_code=r.status_code, content=r.json())

# Recommender endpoint
@app.get("/recommend")
async def get_recommendation():
    async with httpx.AsyncClient() as client:
        r = await client.get(RECOMMENDATION_AGENT_URL)
        return JSONResponse(status_code=r.status_code, content=r.json())
