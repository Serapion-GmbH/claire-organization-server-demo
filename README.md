# Organization Server Demo

This FastAPI-based API serves as a demo organization server for the Claire Ecosystem.
It handles session management and retrieval of available bots using Auth0 as the authentication provider.

## Overview

An organization server translates the user request of a specific organization to the Claire API. This translation allows an organization to manage its users via a custom authentication provider.
A user authenticates itself against the organization server, which then forwards the user request to the Claire API
using its own API key. This architecture means Claire does not need to know about the user, but only about the organization.

## API Endpoints

### Sessions

- `POST /session` - Create a new session
- `GET /session` - List sessions for authenticated user
- `POST /session/{session_id}/renew` - Renew an existing session
- `DELETE /session/{session_id}` - Delete a session

### Bots

- `GET /bots` - List available bots

## Installation

1. Install uv on your system:

  ```bash
  pip install uv
  ```

2. Install Python dependencies via uv:

  ```bash
  uv sync
  ```

## Configuration

### Generate Organization API Key

To generate an organization API key, you can use the interactive `generate_api_key.sh` script:

```bash
./generate_api_key.sh
```

Or use the following curl command:

```bash
curl -X 'POST' \
  'https://api-core.nova-ai.de/organizations/your-organization-id/api_keys' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer your-bearer-token' \
  -H 'Content-Type: application/json' \
  -d '{
  "label": "your-api-key-label",
  "scopes": [
    "session"
  ],
  "expires_at": "your-expiration-date" # e.g. "2024-12-31T23:59:59Z"
}'
```

### Create Environment File

Create a .env.local file and copy the content of the `.env.example` into it:

```bash
cp .env.example .env.local
```

Configure the environment variables in `.env.local` as needed. The following variables are available:

```env
AUTH0__DOMAIN="" # Auth0 tenant domain
AUTH0__AUDIENCE="" # Auth0 audience for the Auth0 API

CLAIRE__BASE_URL="https://api-core.nova-ai.de" # Base URL of the Claire API
CLAIRE__API_KEY="" # API key for the Claire API
CLAIRE__ENABLED_DEVICE_ACTION_IDS="[]" # Comma-separated list of enabled device action IDs for this organization (optional)

CORS__ALLOWED_ORIGINS='*' # Comma-separated list of allowed origins for CORS
```

## Usage

Run the server:

```bash
uv run uvicorn src.organization_server_demo.app:app --reload
```

The API will be available at `http://localhost:8000`

## Docker

Build the Docker image:

```bash
docker build -t organization-server-demo .
```

Run the container:

```bash
docker run -p 8000:8000 organization-server-demo
```