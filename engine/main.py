from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from .dependencies import get_db

from .users.router import router as users_router
from .projects.router import router as projects_router
from .cleaning.router import router as cleaning_router

from .users.models import Organization


origins = ["http://localhost"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"http://localhost:30[00-99]{2}",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


app.include_router(users_router)
app.include_router(projects_router)
app.include_router(cleaning_router)


@app.get("/")
def index(db: Session = Depends(get_db)):
    organizations = db.query(Organization).all()
    return {"message": "hi", "data": organizations}
