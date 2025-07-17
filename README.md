# Agentic To-Do Application

This is a modern, agentic microservices-based To-Do application built with Python, FastAPI, Docker, and HuggingFace Transformers. It demonstrates agentic offload patterns, where specialized agents handle tasks such as notifications and recommendations using LLMs.

## Architecture

- **API Gateway**: Central entry point for all user requests.
- **Task Runner**: Handles CRUD operations for to-dos.
- **DB Service**: Persists to-dos in a JSON file.
- **Notification Agent**: Uses an LLM to summarize tasks and generate notifications.
- **Recommendation Agent**: Uses an LLM to prioritize tasks for the user.

## Features

- CRUD for to-do items
- Smart notifications powered by LLMs
- Task prioritization recommendations via LLMs
- Agentic offload: services can run locally, on edge, or in the cloud
- Fully containerized with Docker Compose

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)

### Clone the Repository

```sh
git clone <your-repo-url>
cd Agentic-Compose-Application
```

### Build and Run All Services

```sh
docker-compose up --build
```

### Service Endpoints

- **API Gateway**: [http://localhost:8000](http://localhost:8000)
  - `GET /todos` - List all to-dos
  - `POST /todos` - Create a new to-do
  - `GET /todos/{todo_id}` - Get a specific to-do
  - `PUT /todos/{todo_id}` - Update a to-do
  - `DELETE /todos/{todo_id}` - Delete a to-do
  - `GET /notify` - Get LLM-powered notification summary
  - `GET /recommend` - Get LLM-powered prioritized recommendations

## Agentic Offload

You can offload agents (e.g., Notification or Recommendation) to the cloud by:
- Building and pushing their Docker images to a registry
- Deploying them on cloud container services (Azure, AWS, GCP)
- Updating service URLs in the API Gateway to point to the cloud endpoints

## Customization

- Change LLM models in `notification-agent` or `recommendation-agent` for different behaviors.
- Extend agents for more advanced workflows.
