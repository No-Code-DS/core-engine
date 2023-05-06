from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .users.router import router as users_router
from .projects.router import router as projects_router
from .cleaning.router import router as cleaning_router
from .feature_engineering.router import router as fe_router


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


app.include_router(users_router)
app.include_router(cleaning_router)
app.include_router(fe_router)
app.include_router(projects_router)
