import requests
from db.conn import db
from db.schemas import Users
from fastapi import APIRouter, Depends, Request, Response
from middlewares.validator import TokenGenerator
from models import SnsType, UserJWT, UserLogin, UserRegister
from services.auth import (check_password, check_pw_format, create_new_user,
                           is_email_exist)
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from utils.custom_oauth import KaKaoOauth

router = APIRouter(prefix="/auth")


@router.post("/register")
async def register(register_info: UserRegister, session: Session = Depends(db.get_db)):
    """_summary_
    `회원가입 API` \n
    - param register_info -> email, password \n
    - param session -> db session
    """
    if not register_info.email or not register_info.password:
        return JSONResponse(status_code=400, content=dict(msg="NO EMAIL OR PASSWORD"))
    if await is_email_exist(register_info):
        return JSONResponse(status_code=400, content=dict(msg="EMAIL ALREADY EXISTS"))
    if not await check_pw_format(register_info.password):
        return JSONResponse(status_code=400, content=dict(msg="WRONG PASSWORD FORMAT"))
    
    await create_new_user(register_info, session)

    return JSONResponse(status_code=201, content=dict(msg="SUCCESSFULLY REGISTERED"))


@router.post("/login")
async def login(user_info: UserLogin, session: Session = Depends(db.get_db)):
    """_summary_
    `로그인 API` \n
    - param user_info -> email, password \n
    - param session -> db session
    """
    if not user_info.email or not user_info.password:
        return JSONResponse(status_code=400, content=dict(msg="NO EMAIL OR PASSWORD"))
    if not await is_email_exist(user_info):
        return JSONResponse(status_code=400, content=dict(msg="WRONG ID OR PASSWORD"))
    if not await check_password(user_info):
        return JSONResponse(status_code=400, content=dict(msg="WRONG ID OR PASSWORD"))

    user = session.query(Users).filter(Users.email == user_info.email).scalar()
    
    token = TokenGenerator().encode_token(
        UserJWT.from_orm(user).dict(include={"id", "email"})
    )
    return JSONResponse(status_code=201, content=dict(Authorization=f"Bearer {token}"))


@router.post("/oauth/{sns_type}")
async def oauth_login(code: str, sns_type: SnsType, session: Session = Depends(db.get_db)):
    
    if sns_type == "kakao":
        url = KaKaoOauth.url
        res_body = {
            "client_id": KaKaoOauth.client_id,
            "redirected_url": KaKaoOauth.redirect_url,
            "code": code
        }
    access_token  = requests.post(url, data=res_body).json()["access_token"]
    
    res_url = "https://kapi.kakao.com/v2/user/me"

    kakao_user_info = requests.post(res_url, headers={"Authorization": f"Bearer {access_token}"}).json()

    return kakao_user_info["nickname"]

    # request_url = f"{url}?client_id={client_id}&&redirect_uri={redirected_url}&grant_type=authorization_code&code={code}"
    
    # return RedirectResponse(request_url)


@router.get("/kakao-logout")
async def kakao_logout(request: Request, response: Response):
    url = "https://kapi.kakao.com/v1/user/unlink"
    KEY = request.cookies['kakao']
    headers = dict(Authorization=f"Bearer {KEY}")
    _res = requests.post(url, headers=headers)
    response.set_cookie(key="kakao", value=None)

    return {"logout": _res.json()}


@router.post('/refresh')
async def refresh(request: Request, auth = Depends(TokenGenerator)):

    if request.method == "POST":
        form = await request.json()
        if form.get("grant_type") == "refresh_token":
            token = form.get("refresh_token")
            payload = auth().decode_token(token)
    

    return payload
    