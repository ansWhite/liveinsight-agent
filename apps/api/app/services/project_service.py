from uuid import uuid4

from app.schemas.project import ProjectCreate, ProjectRead


class ProjectService:
    def __init__(self) -> None:
        self._projects: dict[str, ProjectRead] = {}
        self._assets: dict[str, list[str]] = {}

    def create_project(self, payload: ProjectCreate) -> ProjectRead:
        project = ProjectRead(name=payload.name, description=payload.description)
        self._projects[project.id] = project
        return project

    def register_video(self, project_id: str, filename: str) -> str:
        asset_id = str(uuid4())
        self._assets.setdefault(project_id, []).append(filename)
        return asset_id


project_service = ProjectService()
