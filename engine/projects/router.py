import shutil
from typing import Any
from fastapi import APIRouter, Depends, Form, UploadFile, HTTPException
import numpy as np
import pandas as pd
from sqlalchemy.orm import Session, joinedload

from engine.dependencies import get_current_user, get_db
from engine.projects.models import DataSource, Project, UserProject
from engine.projects.schemas import BaseDataSource, BaseProject, FullProject
from engine.users.schemas import LoggedinUser

router = APIRouter(prefix="/projects")


@router.get("/", response_model=list[FullProject])
def list_projects(_ = Depends(get_current_user), db: Session = Depends(get_db)) -> list[FullProject]:

    projects = db.query(Project).options(joinedload(Project.users)).all()
    return projects


@router.get("/{project_id}")
def get_project(project_id: int, _ = Depends(get_current_user), db: Session = Depends(get_db)) -> FullProject:
    project = db.query(Project).options(joinedload(Project.users)).get(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} was not found")
    return project


@router.post("/create", response_model=BaseProject, response_description="Created project object")
def create_project(user: LoggedinUser = Depends(get_current_user), db: Session = Depends(get_db)):
    project = Project()
    db.add(project)
    db.flush()
    db.add(UserProject(user_id=user.id, project_id=project.id))
    db.commit()

    response = BaseProject(id = project.id, project_name=project.project_name, description=project.description, created_at=str(project.created_at))
    return response


@router.post("/{project_id}/data_source", response_description="Created data source object")
def create_data_source(
    project_id: int,
    file: UploadFile,
    data_source_name: str = Form(),
    _ = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> BaseDataSource:
    project: Project = db.query(Project).get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} was not found")

    raw_path = f"upload/data/raw_data/{file.filename}"
    with open(raw_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    clean_path = f"upload/data/cleaned_data/{file.filename}"
    shutil.copyfile(raw_path, clean_path)

    data_source = DataSource(data_source_name=data_source_name, file_path=clean_path)
    project.data_source = data_source
    db.commit()

    return data_source


@router.get("/{project_id}/data_source")
def get_data_source(project_id: int, _ = Depends(get_current_user), db: Session = Depends(get_db)) -> dict[str, Any]:
    project: Project = db.query(Project).get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} was not found")
    
    try:
        data = pd.read_csv(project.data_source.file_path)
        data.replace(np.nan, None, inplace=True)

        return data.to_dict("list")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Datasource was not found for project with id {project_id}")
