# Support Chatbot

Customer support assistant built with FastAPI + LangGraph + Groq LLM. It offers:
- A web chat UI at `/`
- A JSON chat API at `/chat`
- A simple CLI mode in `main.py`

## Requirements
- Python `3.11`
- A Groq API key

## Setup
1. Create a virtual environment and install dependencies:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -U pip
   pip install -e .
   ```
   If you use `uv`, you can run:
   ```powershell
   uv sync
   ```

2. Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your_key_here
   ```

## Run
- **Web UI / API**
  ```powershell
  uvicorn main:api --reload
  ```
  Then open `http://localhost:8000/`.

- **CLI mode**
  ```powershell
  python main.py
  ```

## API
- `GET /health` -> health check
- `POST /chat` with JSON:
  ```json
  { "message": "Hello", "thread_id": "demo" }
  ```

## Notes
This project loads environment variables from the root `.env` and falls back to `src/.env` if needed. The `GROQ_API_KEY` is required.
