from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session, joinedload

from engine.dependencies import get_db
from engine.projects.models import Project, UserProject
from engine.projects.schemas import BaseProject, FullProject

router = APIRouter(prefix="/projects")


@router.get("/", response_model=list[FullProject])
def index(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)) -> list[FullProject]:
    Authorize.jwt_required()

    projects = db.query(Project).options(joinedload(Project.users)).all()
    return projects


@router.post("/create", response_model=BaseProject)
def create_project(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()

    user = Authorize.get_raw_jwt()

    project = Project()
    db.add(project)
    db.flush()
    db.add(UserProject(user_id=user["id"], project_id=project.id))
    db.commit()

    response = BaseProject(id = project.id, name=project.project_name, descirption=project.description, created_at=str(project.created_at))
    return response
