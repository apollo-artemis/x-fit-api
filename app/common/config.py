"""운영환경 마다 다른 값을 가지는 변수
DB_PW와 같은 정보는 매우 민감한데 어떡할건가?
dictionary 형태로 가지고 오고 싶다면
"""
from dataclasses import dataclass
from os import environ


MYSQL_HOST = environ.get("MYSQL_HOST")
MYSQL_PORT = environ.get("MYSQL_PORT")
DATABASE_NAME = environ.get("DATABASE_NAME")
MYSQL_ROOT_USER = environ.get("MYSQL_ROOT_USER")
MYSQL_ROOT_PASSWORD = environ.get("MYSQL_ROOT_PASSWORD")



@dataclass
class Config:
    """
    기본 Configuration
    """

    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True


@dataclass
class LocalConfig(Config):
    PROJ_RELOAD: bool = True
    DB_URL: str = f"mysql+pymysql://{MYSQL_ROOT_USER}:{MYSQL_ROOT_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/x-fit?charset=utf8mb4"


@dataclass
class DevConfig(Config):
    PROJ_RELOAD: bool = False
    DB_URL: str = f"mysql+pymysql://{MYSQL_ROOT_USER}:{MYSQL_ROOT_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/x-fit?charset=utf8mb4"


@dataclass
class ProdConfig(Config):
    PROJ_RELOAD: bool = False


def conf():
    """
    환경 불러오기
    :return:
    """
    config = dict(prod=ProdConfig(), local=LocalConfig(), dev=DevConfig())
    return config.get(environ.get("API_ENV", "local"))
