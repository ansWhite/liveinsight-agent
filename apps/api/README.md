# API Service

FastAPI backend for the shopping guide Agent.

## Responsibilities

- Health check
- Chat and streaming endpoints
- Knowledge ingestion endpoints
- Product search and recommendation endpoints
- Feedback and evaluation endpoints

## Run

```bash
python -m venv .venv
pip install -r requirements.txt
uvicorn app.main:app --reload
```
