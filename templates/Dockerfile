FROM python:3.8

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev

COPY . /templates

WORKDIR /templates

RUN npm install

CMD npm serve
