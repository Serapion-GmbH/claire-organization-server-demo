# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy source code
COPY src/ ./src/
COPY README.md ./

# Expose port
EXPOSE 8000

# Run the application
CMD ["uv", "run", "uvicorn", "src.organization_server_demo.app:app", "--host", "0.0.0.0", "--port", "8000"]