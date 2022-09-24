from os import environ

MYSQL_HOST = "172.18.0.2" if environ.get("API_ENV") == "local" else "x-fit-dev.c9guns9brwvr.ap-northeast-2.rds.amazonaws.com"