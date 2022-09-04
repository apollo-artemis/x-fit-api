from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from fastapi.requests import Request
from sqlalchemy.orm import Session
from db.conn import db
from db.schemas import Users
from models import WodCreate
from middlewares.validator import TokenGenerator


API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)
router = APIRouter(prefix="/wod")

@router.post("/{wod_id}")
def create_new_wod(wod_id: int, wod_info: WodCreate, session: Session = Depends(db.session), token: str = Depends(API_KEY_HEADER)):
    # data = request.json()
    auth = TokenGenerator()
    user_info = auth.decode_token(token)
    print(user_info)
    # **data
    # query = Users.insert().values(title=data["title"], text=data["text"])
    # last_record_id = session.execute(query)
    return JSONResponse(status_code=200, content=dict(msg='success'))


@router.get("/wod-records")
def record_view(request: Request):
    return JSONResponse(status_code=200, content=dict(msg='success')) 