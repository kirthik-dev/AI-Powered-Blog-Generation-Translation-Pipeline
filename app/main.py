# app/main.py

from fastapi import FastAPI
from dotenv import load_dotenv
from .api import router as blog_router
# 1. Import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI-Powered Blog Generation & Translation Pipeline",
    description="An API for dynamically generating and translating blog content using LangGraph and OpenRouter.",
    version="1.0.0"
)

# 2. Define the origins (URLs) that are allowed to connect.
# We will use "*" to allow all origins for simple local development.
origins = [
    "*", 
    # For production, you would list specific domains like:
    # "http://example.com",
    # "https://www.your-frontend-site.com",
]

# 3. Add the CORS middleware to your app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)

# Include your API router
app.include_router(blog_router, prefix="/api/v1/blog", tags=["Blog Generation"])

@app.get("/", tags=["Health Check"])
async def root():
    return {"status": "ok"}