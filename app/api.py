# app/api.py - FINAL, SIMPLIFIED, AND ROBUST VERSION

import traceback
from fastapi import APIRouter, Depends, HTTPException
from .schemas import BlogGenerationRequest, BlogGenerationResponse
from .graph_builder import get_graph
from langgraph.graph.graph import CompiledGraph

router = APIRouter()

# Build the graph instance once at startup
graph_app = get_graph()

def get_graph_app() -> CompiledGraph:
    return graph_app

@router.post("/generate", response_model=BlogGenerationResponse)
async def generate_blog_endpoint(
    request: BlogGenerationRequest,
    graph: CompiledGraph = Depends(get_graph_app)
):
    """
    Takes a topic and language, and returns a structured, translated blog post.
    """
    try:
        # The input must contain all keys defined in the initial state.
        # Even if they are empty, they must exist.
        inputs = {
            "topic": request.topic,
            "target_language": request.target_language,
            "draft": "",
            "structured_blog": None,
            "translated_blog": None,
        }

        # Use the .invoke() method, which is the most stable.
        final_state = graph.invoke(inputs)

        result_data = final_state.get('translated_blog', {})
        return BlogGenerationResponse(
            message="Blog generated and translated successfully.",
            data=result_data
        )

    except Exception as e:
        print("--- DETAILED ERROR TRACEBACK ---")
        print(traceback.format_exc())
        print("--- END OF TRACEBACK ---")
        raise HTTPException(
            status_code=500,
            detail=f"An internal error occurred. Error: {e}"
        )