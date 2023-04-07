from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from engine.dependencies import get_db
from engine.users.models import User

from engine.users.schemas import LoginUser

router = APIRouter(prefix="/users")


@router.post("/login")
def login(login_user: LoginUser, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email==login_user.email, User.hashed_password==login_user.password).first()
    if not user:
        raise HTTPException(status_code=401,detail="Bad username or password")
    print(user.email)
    access_token = Authorize.create_access_token(subject=user.email)
    refresh_token = Authorize.create_refresh_token(subject=user.email)
    return {"access_token": access_token, "refresh_token": refresh_token}


# @router.post("/signup")
# def sign_up(signup_user: SignupUser, db: Session = Depends(get_db)):
#     pass


@router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}
