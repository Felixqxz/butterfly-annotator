FROM node:12.18.1
ENV NODE_ENV=production

ARG DEBIAN_FRONTEND=noninteractive

COPY . /templates

WORKDIR /templates

RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.0/install.sh | bash
RUN nvm install node 
RUN npm install --production

CMD npm serve
