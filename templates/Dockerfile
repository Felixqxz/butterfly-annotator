FROM node:12.18.1
ENV NODE_ENV=production

ARG DEBIAN_FRONTEND=noninteractive

COPY . /templates

WORKDIR /templates

RUN npm install --production
CMD npm run serve