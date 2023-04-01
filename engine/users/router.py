from fastapi import APIRouter

router = APIRouter(prefix="/users")


@router.get("/")
def index():
    return {"message": "hello from users router"}
