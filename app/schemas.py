# app/schemas.py
from pydantic import BaseModel
from typing import Any

class BlogGenerationRequest(BaseModel):
    topic: str
    target_language: str

class BlogGenerationResponse(BaseModel):
    message: str
    data: Any # This will hold our final translated blog JSON