# Organization Server Demo

This is a FastAPI-based REST API that serves as a demo organization server for the Claire Ecosystem. It provides session management and bot integration capabilities with Auth0 authentication.

## Features

- Health check endpoint (`/` and `/health`)
- Interaction with the Claire API
- Auth0 authentication support
- CORS middleware support
- Environment-based configuration

## Requirements

- Python 3.13+
- FastAPI
- Pydantic
- Pydantic Settings
- Uvicorn
- FastAPI Auth0
- aiohttp

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   uv sync
   ```

## Usage

Run the server:
```bash
uv run uvicorn src.organization_server_demo.app:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health
- `GET /` - Health check endpoint
- `GET /health` - Health check endpoint

### Sessions
- `POST /session` - Create a new session
- `GET /session` - List sessions for authenticated user
- `POST /session/{session_id}/renew` - Renew an existing session
- `DELETE /session/{session_id}` - Delete a session

### Bots
- `GET /bots` - List available bots

## Development

Install development dependencies:
```bash
uv sync --extra dev
```

Run tests:
```bash
pytest
```

## Docker

Build the Docker image:
```bash
docker build -t organization-server-demo .
```

Run the container:
```bash
docker run -p 8000:8000 organization-server-demo
```