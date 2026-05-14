# LiveInsight API

FastAPI backend for project management, upload registration, analysis jobs, report retrieval, highlight clips, generated scripts, and agent chat.

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Main Routes

- `GET /api/health`
- `POST /api/projects`
- `POST /api/projects/{project_id}/videos`
- `POST /api/analysis/start`
- `GET /api/analysis/status/{task_id}`
- `GET /api/reports/{project_id}`
- `GET /api/clips/{project_id}`
- `GET /api/scripts/{project_id}`
- `POST /api/chat`
