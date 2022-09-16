from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from db.conn import db
from db.schemas import Users, Wods
from services.wod import create_user_wod, get_wod_detail
from models import WodCreate, WodDetail
from middlewares.validator import TokenGenerator
from errors import exceptions as ex


API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)
router = APIRouter(prefix="/wod")


# 와드 기록 생성(create)
@router.post("/create")
async def create_new_wod(
    wod_info: WodCreate, 
    session: Session = Depends(db.session), 
    token: str = Depends(API_KEY_HEADER)
):

    try:
        if not token:
            raise ex.TokenDecodeEx("No Token")
        auth = TokenGenerator()
        user_info = auth.decode_token(token)
    
    except Exception as e:
        error: Exception = await ex.custom_exception_handler(e)
        error_dict: dict = dict(status=error.status_code, msg=error.msg, detail=error.detail, ex=error.ex)
        raise HTTPException(status_code=error.status_code, detail=error_dict)
    
    create_user_wod(wod_info, user_info['id'], session)
    
    return JSONResponse(status_code=200, content=dict(msg='success'))


# 와드 내용 보기(read)
@router.get("/{wod_id}", response_model=WodDetail)
async def wod_view(
    wod_id: int, 
    token: str = Depends(API_KEY_HEADER),
    session: Session = Depends(db.session)
):
    
    wod_info = await get_wod_detail(wod_id, session)

    return wod_info


## 여기서부터는 미완성

# 와드 수정(update)
@router.put("/{wod_id}")
async def update_wod(
    wod_id: int, 
    wod_info, 
    session: Session = Depends(db.session), 
    token: str = Depends(API_KEY_HEADER)
):
    wod_item = 0



# 와드 삭제(delete)
@router.delete("/{wod_id}")
async def update_wod(
    wod_id: int, 
    wod_info, 
    session: Session = Depends(db.session), 
    token: str = Depends(API_KEY_HEADER)
):
    wod_item = 0
    pass


# 와드 리스트 보기(read list) - 작성자, 작성 일시, 좋아요, 제목, 조회수 필요할듯
@router.get("/wod-records")
async def get_all_wods():
    pass
