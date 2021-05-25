FROM python:slim-buster

LABEL MAINTAINER="Yoshino-s"

WORKDIR /app

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

RUN apt update && apt upgrade -y

RUN apt install libreoffice-core unoconv -y

COPY ./requirements.txt /app/

RUN cd /app && pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

COPY . /app

ENTRYPOINT [ "/app/afa.py" ]

CMD [ "--help" ]