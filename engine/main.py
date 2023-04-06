from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .dependencies import get_db

from .users.router import router as users_router
from .projects.router import router as projects_router

from .users.models import Organization


app = FastAPI()

app.include_router(users_router)
app.include_router(projects_router)


@app.get("/")
def index(db: Session = Depends(get_db)):
    organizations = db.query(Organization).all()
    return {"message": "hi", "data": organizations}
