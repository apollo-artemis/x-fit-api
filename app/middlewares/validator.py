import os
import time
from datetime import datetime, timedelta

import jwt
from models import UserJWT
from errors import exceptions
from fastapi.security import HTTPBearer
from services.auth import url_pattern_check
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from utils.logger import api_logger


class TokenGenerator:
    security = HTTPBearer()
    secret_key = os.environ.get("SECRET_KEY")
    algorithm = os.environ.get("ALGORITHM")

    def encode_token(self, user_info):
        payload = {
            "iat": datetime.now(),
            "exp": datetime.now() + timedelta(hours=1),
            "sub": user_info,
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=self.algorithm)
        except jwt.ExpiredSignatureError:
            raise exceptions.TokenExpiredEx()
        except jwt.DecodeError:
            raise exceptions.TokenDecodeEx()
        return payload["sub"]


class AuthRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request.state.req_time = datetime.now()
        request.state.start = time.time()
        request.state.inspect = None
        request.state.user = None
        request.state.service = None
        headers = request.headers
        url = request.url.path
        error = None
        # AWS에서는 로드밸런서를 통하면서 x-forwarded-for가 생김
        ip = (
            request.headers["x-forwarded-for"]
            if "x-forwarded-for" in request.headers.keys()
            else request.client.host
        )
        request.state.ip = ip.split(",")[0] if "," in ip else ip

        if await url_pattern_check(
            url, os.environ.get("EXCEPT_PATH_REGEX")
        ) or url in os.environ.get("EXCEPT_PATH_LIST"):
            return await call_next(request)
        if request.method == "OPTIONS":
            return await call_next(request)

        if "authorization" not in headers.keys():
            error = exceptions.NotAuthorized()
            await api_logger(request=request, error=error)
            return JSONResponse(
                status_code=error.status_code,
                content=dict(
                    status=error.status_code,
                    msg=error.msg,
                    detail=error.detail,
                    code=error.code,
                ),
            )

        try:
            token = headers.get("authorization").split(" ")[1].strip()
            token_info = TokenGenerator().decode_token(token)
            request.state.user = UserJWT(**token_info)
            response = await call_next(request)
            await api_logger(request=request, response=response)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            if e == jwt.ExpiredSignatureError:
                error = exceptions.TokenExpiredEx()
            else:
                error = exceptions.TokenDecodeEx()
            error_dict = dict(
                status=error.status_code,
                msg=error.msg,
                detail=error.detail,
                code=error.code,
            )

            response = JSONResponse(status_code=error.status_code, content=error_dict)
            await api_logger(request=request, error=error)

        return response
