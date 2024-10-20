# 기본 이미지를 python3.10.11 로 설정
FROM python:3.10.11-slim
ENV PYTHONUNBUFFERED 1
RUN apt-get update -y

# docker 내에서 /bangtender 라는 이름의 폴더 생성
RUN mkdir /bangtender

RUN chmod -R 755 /bangtender

# docker 내에서 코드를 실행할 폴더 위치를 /bangtender 로 지정
WORKDIR /bangtender

ADD requirements.txt /bangtender/
RUN pip install --upgrade pip

# 로컬 내 현재 위치에 있는 모든 파일 및 폴더를 docker 의 /bangtender/ 폴더
ADD . /bangtender/