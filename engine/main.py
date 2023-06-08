from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .cleaning.router import router as cleaning_router
from .feature_engineering.router import router as fe_router
from .model_selection.router import router as models_router
from .projects.router import router as projects_router
from .users.router import router as users_router

origins = ["http://localhost", "http://datalume.ai", "https://datalume.ai"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"http://(.*amazonaws\.com)|(localhost:30[00-99]{2})",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users_router, prefix="/api")
app.include_router(cleaning_router, prefix="/api")
app.include_router(fe_router, prefix="/api")
app.include_router(models_router, prefix="/api")
app.include_router(projects_router, prefix="/api")
