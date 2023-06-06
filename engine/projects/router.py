import shutil
from typing import Any

import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session, joinedload

from engine.dependencies import get_current_user, get_db
from engine.projects.models import DataSource, Project, UserProject
from engine.projects.schemas import BaseDataSource, BaseProject, FullProject, ProjectCreate
from engine.users.schemas import LoggedinUser

router = APIRouter(prefix="/projects")


@router.get("/", response_model=list[FullProject])
def list_projects(_=Depends(get_current_user), db: Session = Depends(get_db)) -> list[FullProject]:

    projects = db.query(Project).options(joinedload(Project.users)).all()
    print(projects[-1].model.__dict__)
    return projects


@router.get("/{project_id}")
def get_project(project_id: int, _=Depends(get_current_user), db: Session = Depends(get_db)) -> FullProject:
    project = db.query(Project).options(joinedload(Project.users)).get(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} was not found")
    return project


@router.post("/create", response_model=BaseProject, response_description="Created project object")
def create_project(
    project_create: ProjectCreate,
    user: LoggedinUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = Project(project_name=project_create.project_name, description=project_create.description)
    db.add(project)
    db.flush()
    db.add(UserProject(user_id=user.id, project_id=project.id))
    db.commit()

    response = BaseProject(
        id=project.id,
        project_name=project.project_name,
        description=project.description,
        created_at=str(project.created_at),
    )
    return response


@router.post("/{project_id}/data_source", response_description="Created data source object")
def create_data_source(
    project_id: int,
    file: UploadFile,
    data_source_name: str = Form(),
    _=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> BaseDataSource:
    project: Project = db.query(Project).get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} was not found")

    file_type = file.filename.split(".")[-1]
    raw_path = f"upload/data/raw_data/{data_source_name}.{file_type}"
    with open(raw_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    data_source = DataSource(data_source_name=data_source_name, raw_path=raw_path)
    project.data_source = data_source
    db.commit()

    return data_source


@router.get("/{project_id}/data_source")
def get_data_source(
    project_id: int, _=Depends(get_current_user), db: Session = Depends(get_db)
) -> dict[str, Any]:
    project: Project = db.query(Project).get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} was not found")

    try:
        if project.data_source.ready_path is not None:
            data = pd.read_csv(project.data_source.ready_path)
        elif project.data_source.clean_path is not None:
            data = pd.read_csv(project.data_source.clean_path)
        elif project.data_source.raw_path is not None:
            data = pd.read_csv(project.data_source.raw_path)
        else:
            raise HTTPException(status_code=404, detail="Datasource file was deleted or corrupted")

        data.replace(np.nan, None, inplace=True)

        return data.to_dict("list")
    except FileNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Datasource was not found for project with id {project_id}"
        )
