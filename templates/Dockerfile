FROM python:3.8

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev

COPY . /templates

WORKDIR /templates

RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.0/install.sh | bash
RUN nvm install node 
RUN npm install

CMD npm serve
