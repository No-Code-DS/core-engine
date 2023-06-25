import json
import pickle
import random
from typing import Any

import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from engine.dependencies import get_current_user, get_db
from engine.deployment.models import Deployment
from engine.model_selection.models import StatusEnum
from engine.projects.models import Project

router = APIRouter(prefix="/projects")


@router.post("{project_id}/deploy")
def deploy_model(project_id: int, db: Session = Depends(get_db)):
    """Build an api for trained model"""
    project = db.query(Project).get(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} was not found")

    slug = project.project_name.replace(" ", "_")
    deploy = Deployment(slug=slug)
    db.add(deploy)
    db.flush()
    project.deployment_id = deploy.id
    project.model.status = StatusEnum.DEPLOYED
    db.commit()

    return {"url": f"/projects/deploy/{slug}"}


@router.post("/deploy/{slug}")
def predict(slug: str, data: dict[str, Any], db: Session = Depends(get_db)):
    """run prediction with trained model"""
    deployment = db.query(Deployment).filter_by(slug=slug).order_by(Deployment.id.desc()).first()
    if deployment is None:
        raise HTTPException(status_code=404, detail=f"This project is not deployed")

    print(deployment.id)

    model = deployment.project.model
    model_path = f"trained_models/{model.model_name}{model.id}.pkl"

    with open(model_path, "rb") as pkl:
        trained_model = pickle.load(pkl)
    print(type(trained_model))
    # prediction = trained_model.predict(data.values())
    return random.randint(10, 1000)
