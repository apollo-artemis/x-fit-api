from db.conn import get_db
from db.models import User
from db.schemas import UserJWT, UserLogin, UserRegister
from fastapi import APIRouter, Depends
from middlewares.validator import TokenGenerator
from services.auth import (
    check_password,
    check_pw_format,
    create_new_user,
    is_email_exist,
)
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

router = APIRouter(prefix="/auth")


@router.post("/register")
async def register(register_info: UserRegister, session: Session = Depends(get_db)):
    """_summary_
    `회원가입 API` \n
    - param register_info -> email, password \n
    - param session -> db session
    """
    if not register_info.email or not register_info.password:
        return JSONResponse(status_code=400, content=dict(msg="NO EMAIL OR PASSWORD"))
    if is_email_exist(register_info):
        return JSONResponse(status_code=400, content=dict(msg="EMAIL ALREADY EXISTS"))
    if not check_pw_format(register_info.password):
        return JSONResponse(status_code=400, content=dict(msg="WRONG PASSWORD FORMAT"))

    create_new_user(register_info, session)

    return JSONResponse(status_code=201, content=dict(msg="SUCCESSFULLY REGISTERED"))


@router.post("/login")
async def login(user_info: UserLogin, session: Session = Depends(get_db)):
    """_summary_
    `로그인 API` \n
    - param user_info -> email, password \n
    - param session -> db session
    """
    if not user_info.email or not user_info.password:
        return JSONResponse(status_code=400, content=dict(msg="NO EMAIL OR PASSWORD"))
    if not is_email_exist(user_info):
        return JSONResponse(status_code=400, content=dict(msg="WRONG ID OR PASSWORD"))
    if not await check_password(user_info):
        return JSONResponse(status_code=400, content=dict(msg="WRONG ID OR PASSWORD"))

    user = session.query(User).filter(User.email == user_info.email)

    token = TokenGenerator().encode_token(
        UserJWT.from_orm(user).dict(include={"id", "email"})
    )
    return JSONResponse(status_code=201, content=dict(Authorization=f"Bearer {token}"))
