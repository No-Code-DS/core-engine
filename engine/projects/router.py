import shutil
from fastapi import APIRouter, Depends, Form, UploadFile, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session, joinedload

from engine.dependencies import get_db
from engine.projects.models import DataSource, Project, UserProject
from engine.projects.schemas import BaseDataSource, BaseProject, FullProject

router = APIRouter(prefix="/projects")


@router.get("/", response_model=list[FullProject])
def list_projects(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)) -> list[FullProject]:
    Authorize.jwt_required()

    projects = db.query(Project).options(joinedload(Project.users)).all()
    return projects


@router.get("/{project_id}")
def get_project(project_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)) -> FullProject:
    Authorize.jwt_required()

    project = db.query(Project).options(joinedload(Project.users)).where(Project.id == project_id).one()
    return project


@router.post("/create", response_model=BaseProject, response_description="Created project object")
def create_project(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()

    user = Authorize.get_raw_jwt()

    project = Project()
    db.add(project)
    db.flush()
    db.add(UserProject(user_id=user["id"], project_id=project.id))
    db.commit()

    response = BaseProject(id = project.id, project_name=project.project_name, description=project.description, created_at=str(project.created_at))
    return response


@router.post("/{project_id}/data_source", response_description="Created data source object")
def create_data_source(
    project_id: int,
    file: UploadFile,
    data_source_name: str = Form(),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
) -> BaseDataSource:
    Authorize.jwt_required()

    project: Project = db.query(Project).get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} was not found")

    file_path = f"upload/data/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    data_source = DataSource(data_source_name=data_source_name, file_path=file_path)
    project.data_source = data_source
    db.commit()

    return data_source
