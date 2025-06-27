# app/graph_builder.py

import os
from typing import TypedDict, List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.json import JsonOutputParser

# --- Pydantic Schemas ---
class BlogSection(BaseModel):
    heading: str = Field(description="The heading for this specific blog section.")
    content: str = Field(description="The detailed content for this section.")

class StructuredBlog(BaseModel):
    title: str = Field(description="The main title of the blog post.")
    introduction: str = Field(description="A brief introduction to the blog post.")
    sections: List[BlogSection] = Field(description="A list of the blog's main sections. This should not be empty.")
    conclusion: str = Field(description="A concluding paragraph that summarizes the blog post.")

# --- LangGraph State ---
class GraphState(TypedDict):
    topic: str
    target_language: str
    draft: str
    structured_blog: StructuredBlog
    translated_blog: dict

# --- LLM Helper Function ---
def get_openrouter_llm(model_name: str, temperature: float = 0.7):
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "http://localhost:8080",
            "X-Title": "AI Blog Weaver",
        }
    )

# --- LangGraph Nodes ---
def generate_draft(state: GraphState):
    print("---GENERATING DRAFT (with DeepSeek Chat)---")
    topic = state['topic']
    prompt = ChatPromptTemplate.from_template(
        "You are an expert blog writer. Write a comprehensive, detailed, and high-quality blog post about the following topic: **{topic}**.\n\n"
        "**Requirements:**\n"
        "- The total length of the blog post must be **at least 1000 words**.\n"
        "- It must include a clear introduction, at least 3-5 detailed main sections with headings, and a concluding paragraph.\n"
        "- The content should be informative, engaging, and well-structured.\n\n"
        "Please begin writing now."
    )
    llm = get_openrouter_llm("deepseek/deepseek-chat-v3-0324:free", temperature=0.7)
    chain = prompt | llm
    draft = chain.invoke({"topic": topic}).content
    return {"draft": draft}

def structure_blog(state: GraphState):
    print("---STRUCTURING BLOG (with Qwen 2.5)---") # Updated print statement
    draft = state['draft']
    parser = JsonOutputParser(pydantic_object=StructuredBlog)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a master at parsing text and structuring it into a precise JSON format based on a provided schema. "
         "You must strictly adhere to the schema and ensure ALL fields are populated, especially the 'sections' list which must contain multiple items. "
         "Do not omit any fields. Your output must ONLY be a single, complete, and valid JSON object."),
        ("human", "Please structure the following blog draft into the required JSON format.\n\nDraft:\n{draft}\n\nJSON Schema:\n{format_instructions}")
    ])
    
    # ### <<< THIS IS THE FIX ###
    # Using the correct model name you provided.
    llm = get_openrouter_llm("qwen/qwen2.5-vl-32b-instruct:free", temperature=0)
    
    chain = prompt | llm | parser
    structured_blog = chain.invoke({"draft": draft, "format_instructions": parser.get_format_instructions()})
        
    return {"structured_blog": structured_blog}

def translate_blog(state: GraphState):
    print("---TRANSLATING BLOG (with Llama-4 Maverick)---")
    structured_blog_data = state['structured_blog']
    target_language = state['target_language']

    if not isinstance(structured_blog_data, dict):
        structured_blog_data = structured_blog_data.model_dump()

    if not structured_blog_data.get('sections') or not structured_blog_data.get('conclusion'):
         print("Warning: Structuring step may have failed. Translating incomplete data.")

    if target_language.lower() in ["english", "en"]:
        print("---SKIPPING TRANSLATION (target is English)---")
        return {"translated_blog": structured_blog_data}

    prompt = ChatPromptTemplate.from_template(
        "Translate only the string values in this JSON object to {target_language}. Keep the JSON keys and structure identical. Do not add any commentary.\n\nJSON:\n{blog_json}"
    )
    # Sticking with a reliable translator model
    llm = get_openrouter_llm("meta-llama/llama-4-maverick:free", temperature=0)
    parser = JsonOutputParser()
    chain = prompt | llm | parser

    translated_blog = chain.invoke({"blog_json": structured_blog_data, "target_language": target_language})
    return {"translated_blog": translated_blog}

# --- Graph Assembly (No changes) ---
def get_graph():
    workflow = StateGraph(GraphState)
    workflow.add_node("generate_draft", generate_draft)
    workflow.add_node("structure_blog", structure_blog)
    workflow.add_node("translate_blog", translate_blog)
    workflow.add_edge(START, "generate_draft")
    workflow.add_edge("generate_draft", "structure_blog")
    workflow.add_edge("structure_blog", "translate_blog")
    workflow.add_edge("translate_blog", END)
    return workflow.compile()