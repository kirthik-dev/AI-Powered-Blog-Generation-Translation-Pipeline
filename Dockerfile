# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install uv, our fast package manager
RUN pip install uv

# Copy the entire application source code into the container
COPY . /app

# Install all Python dependencies using uv
RUN uv pip install --no-cache "fastapi[all]" "langchain-openai" "langgraph" "langchain" "python-dotenv" "langsmith"

# Expose the port the app will run on
EXPOSE 8080

# Command to run the application when the container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]