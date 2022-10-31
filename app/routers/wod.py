from db.conn import db
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from middlewares.validator import TokenGenerator
from models import WodCreate, WodDetail, WodUpdate
from services.wod import (create_user_wod, get_wod_detail, update_wod_info,
                          wod_delete, wod_ownership_check)
from sqlalchemy.orm import Session

API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)
router = APIRouter(prefix="/wod")


# 와드 기록 생성(create)
@router.post("/create")
async def create_new_wod(
    wod_info: WodRecordCreate, 
    session: Session = Depends(db.session), 
    token: str = Depends(API_KEY_HEADER)
):

    auth = TokenGenerator()
    user_info = auth.decode_token(token.split(" ")[1].strip())
    
    create_user_wod(wod_info, user_info['id'], session)
    
    return JSONResponse(status_code=200, content=dict(msg='success'))


# 와드 내용 보기(read)
@router.get("/{wod_id}", response_model=WodDetail)
async def wod_view(
    wod_id: int, 
    token: str = Depends(API_KEY_HEADER),
    session: Session = Depends(db.session)
):
    auth = TokenGenerator()
    user_info = auth.decode_token(token.split(" ")[1].strip())
    wod_info = await get_wod_detail(wod_id, session)

    return wod_info


## 여기서부터는 미완성

# 와드 수정(update)
@router.put("/{wod_id}")
async def update_wod(
    wod_id: int, 
    wod_info: WodUpdate, 
    session: Session = Depends(db.session), 
    token: str = Depends(API_KEY_HEADER)
):
    
    auth = TokenGenerator()
    user_info = auth.decode_token(token.split(" ")[1].strip())
    
    wod_ownership_check(wod_id, user_info["id"], session)
    update_wod_info(wod_id, wod_info, session)

    return JSONResponse(status_code=200, content=dict(msg='Successfully Updated'))

    
# 와드 삭제(delete)
@router.delete("/{wod_id}")
async def delete_wod(
    wod_id: int, 
    session: Session = Depends(db.session), 
    token: str = Depends(API_KEY_HEADER)
):
    auth = TokenGenerator()
    user_info = auth.decode_token(token.split(" ")[1].strip())
    
    wod_ownership_check(wod_id, user_info["id"], session)
    wod_delete(wod_id, session)
    
    return JSONResponse(status_code=200, content=dict(msg='Successfully Deleted'))


# 와드 리스트 보기(read list) - 작성자, 작성 일시, 좋아요, 제목, 조회수 필요할듯
@router.get("/wod-records")
async def get_all_wods():
    pass
