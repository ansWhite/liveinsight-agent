from fastapi import APIRouter, UploadFile

from app.schemas.analysis import AnalysisRequest, AnalysisStatus, ChatRequest, ChatResponse
from app.schemas.project import ProjectCreate, ProjectRead
from app.schemas.report import HighlightClip, InsightReport, ScriptDraft
from app.services.analysis_service import analysis_service
from app.services.project_service import project_service

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/projects", response_model=ProjectRead)
async def create_project(payload: ProjectCreate) -> ProjectRead:
    return project_service.create_project(payload)


@router.post("/projects/{project_id}/videos")
async def upload_video(project_id: str, file: UploadFile) -> dict[str, str]:
    asset_id = project_service.register_video(project_id=project_id, filename=file.filename or "upload.mp4")
    return {"project_id": project_id, "asset_id": asset_id, "status": "registered"}


@router.post("/analysis/start", response_model=AnalysisStatus)
async def start_analysis(payload: AnalysisRequest) -> AnalysisStatus:
    return analysis_service.start_analysis(payload)


@router.get("/analysis/status/{task_id}", response_model=AnalysisStatus)
async def get_analysis_status(task_id: str) -> AnalysisStatus:
    return analysis_service.get_status(task_id)


@router.get("/reports/{project_id}", response_model=InsightReport)
async def get_report(project_id: str) -> InsightReport:
    return analysis_service.get_report(project_id)


@router.get("/clips/{project_id}", response_model=list[HighlightClip])
async def get_highlight_clips(project_id: str) -> list[HighlightClip]:
    return analysis_service.get_highlights(project_id)


@router.get("/scripts/{project_id}", response_model=list[ScriptDraft])
async def get_scripts(project_id: str) -> list[ScriptDraft]:
    return analysis_service.get_scripts(project_id)


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest) -> ChatResponse:
    return analysis_service.chat(payload)
