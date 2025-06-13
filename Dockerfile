# Base image: Python 3.13 slim for minimal image size while maintaining functionality
FROM python:3.13-slim

# Create and set the application directory in the container
WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first to utilize Docker's layer caching
# This means dependencies will only be reinstalled if requirements.txt changes
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# Create necessary directories
RUN mkdir -p app/rag app/data/chroma_db

# Copy only the essential files
COPY app/main.py ./app/
COPY app/rag/chain.py ./app/rag/
COPY app/rag/__init__.py ./app/rag/
COPY app/data/chroma_db/ ./app/data/chroma_db/
COPY .env .

# Document the port that the FastAPI application will use
# Note: This is for documentation only, actual port mapping is done at runtime
EXPOSE 8000

# Start the FastAPI application using uvicorn
# --host 0.0.0.0 makes the server accessible from outside the container
# --port 8000 matches the exposed port above
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]