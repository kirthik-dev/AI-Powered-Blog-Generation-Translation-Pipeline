# AI-Powered Blog Generation & Translation Pipeline

This project is an **API service** that dynamically generates, structures, and translates blog content using advanced LLMs (via OpenRouter) and [LangGraph](https://github.com/langchain-ai/langgraph).  
It is designed for seamless integration with any frontend (HTML/JS, React, Streamlit, etc.).

---

## 🚀 Features

- **Automated Blog Generation:**  
  Generate high-quality, long-form blog posts on any topic.
- **Structured Output:**  
  Converts unstructured drafts into a clean, sectioned JSON format.
- **Translation:**  
  Translates the structured blog into any target language.
- **API-First:**  
  Built with FastAPI for easy integration with any frontend.
- **CORS Enabled:**  
  Ready for local or remote frontend connections.

---

## 🗂️ Project Structure

```
app/
├── __init__.py
├── api.py              # API endpoints (FastAPI router)
├── graph_builder.py    # LangGraph workflow & LLM logic
├── main.py             # FastAPI app entrypoint
├── schemas.py          # Pydantic schemas for requests/responses
└── __pycache__/        # Python cache files
```

---

## ⚙️ Setup Instructions

### 1. **Clone the Repository**

```sh
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. **Create a Virtual Environment**

```sh
python -m venv .venv
```

### 3. **Activate the Environment**

- **Windows:**  
  ```
  .venv\Scripts\activate
  ```
- **macOS/Linux:**  
  ```
  source .venv/bin/activate
  ```

### 4. **Install Dependencies**

```sh
pip install -r requirements.txt
```
*(Create `requirements.txt` with FastAPI, uvicorn, python-dotenv, langgraph, langchain-openai, etc.)*

### 5. **Set Environment Variables**

Create a `.env` file in the root directory with your OpenRouter API key:

```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

---

## 🏃‍♂️ Running the App

### **Start the FastAPI Server**

```sh
uvicorn app.main:app --reload --port 8080
```

- The API will be available at: [http://localhost:8080](http://localhost:8080)
- Interactive API docs: [http://localhost:8080/docs](http://localhost:8080/docs)

---

## 🖥️ Frontend Integration

You can use any frontend (HTML/JS, React, etc.) to interact with this API.

### **Serving Static HTML (Optional)**

To serve your HTML frontend via FastAPI:

1. Place your HTML, CSS, and JS files in a folder, e.g., `app/static/`.
2. Add this to `app/main.py`:

   ```python
   from fastapi.staticfiles import StaticFiles
   app.mount("/static", StaticFiles(directory="app/static"), name="static")
   ```

3. Access your frontend at:  
   [http://localhost:8080/static/yourfile.html](http://localhost:8080/static/yourfile.html)

---

## 📦 API Usage

### **POST `/api/v1/blog/generate`**

**Request Body:**
```json
{
  "topic": "Artificial Intelligence in Healthcare",
  "target_language": "French"
}
```

**Response:**
```json
{
  "message": "Blog generated and translated successfully.",
  "data": {
    "title": "...",
    "introduction": "...",
    "sections": [
      { "heading": "...", "content": "..." }
    ],
    "conclusion": "..."
  }
}
```

---

## 🛠️ Customization

- **LLM Models:**  
  Change model names in `graph_builder.py` to use different OpenRouter models.
- **API Endpoints:**  
  Add more endpoints in `api.py` as needed.
- **Frontend:**  
  Build your own UI or use the provided static serving method.

---

## 🤝 Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [OpenRouter](https://openrouter.ai/)
- [LangChain](https://python.langchain.com/)

---

*Feel free to open issues or PRs for improvements!*
