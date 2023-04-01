from fastapi import APIRouter

router = APIRouter(prefix="/projects")


@router.get("/")
def index():
    return {"message": "hello from projects router"}
