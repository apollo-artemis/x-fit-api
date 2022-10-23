from dataclasses import dataclass
from os import environ


class BaseOauth:
    def login():
        pass

    def get_access_token(self):
        pass


@dataclass
class KaKaoOauth(BaseOauth):
    url = "https://kauth.kakao.com/oauth/token"
    client_id = environ.get('KAKAO_CLIENT_ID')
    redirect_url = "http://localhost:8080/api/oauth/kakao/login"
