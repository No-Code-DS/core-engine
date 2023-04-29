from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from engine.dependencies import get_db, get_refresh_user
from engine.users.models import User

from engine.users.schemas import LoginUser, SignupUser, TokenSchema
from engine.users.util import create_access_token, create_refresh_token, get_hashed_password, verify_password

router = APIRouter(prefix="/users")


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)) -> TokenSchema:
    if request.headers['Content-Type'] == 'application/json':
        login_user = LoginUser(** await request.json())
    elif request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        login_user = LoginUser.as_form(** await request.form())

    user = db.query(User).filter(User.email==login_user.email).first()
    if not user:
        raise HTTPException(status_code=401,detail="Bad username or password")
    
    if not verify_password(login_user.password, user.hashed_password):
        raise HTTPException(status_code=401,detail="Bad username or password")

    access_token = create_access_token(subject=user.email, email=user.email, id=user.id)
    refresh_token = create_refresh_token(subject=user.email)

    return TokenSchema(access_token=access_token, refresh_token=refresh_token)


@router.post("/signup")
def sign_up(signup_user: SignupUser, db: Session = Depends(get_db)):
    if signup_user.password1 != signup_user.password2:
        raise HTTPException(status_code=400, detail="passwords don't match")

    user = db.query(User).filter(User.email == signup_user.email).first()
    if user:
        raise HTTPException(status_code=409, detail="Email already exists")

    user = User(
        email=signup_user.email, 
        hashed_password=get_hashed_password(signup_user.password1),
    )
    db.add(user)
    db.commit()
    access_token = create_access_token(subject=user.email, email=user.email, id=user.id)
    refresh_token = create_refresh_token(subject=user.email)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post('/refresh')
def refresh(user = Depends(get_refresh_user)):
    access_token = create_access_token(subject=user.email, email=user.email, id=user.id)
    return {"access_token": access_token}
