# # pull official base image

FROM --platform=linux/amd64 python:3.10-slim-buster

# # set work directory

WORKDIR /app

# # set environment variables

ENV PYTHONPATH /app/:/app:$PYTHONPATH

# # upgrade pip

RUN pip install --upgrade pip

# # install dependencies

# RUN apk update\
#  && apk add zlib-dev libxml2-dev libxslt-dev libressl-dev libffi-dev\

# # pillow alpine dependencies \

# # https://github.com/python-pillow/docker-images/blob/master/alpine/Dockerfile

# # https://pillow.readthedocs.io/en/stable/installation.html

# && apk add freetype-dev fribidi-dev harfbuzz-dev jpeg-dev lcms2-dev openjpeg-dev tcl-dev tiff-dev tk-dev\
#  libwebp-dev libimagequant-dev libxcb-dev libpng-dev glib-dev make\

# #

# && apk add curl\

# #

# && apk add --virtual .tmp-build-deps\
#  gcc python3-dev musl-dev cargo

# # install python packages

# COPY ./requirements-fastapi.txt ./
# RUN pip install -r requirements-fastapi.txt

# # remove build dependencies

# RUN apk del .tmp-build-deps

# # copy project

COPY ./ /app/

# # run CMD

EXPOSE 8000
