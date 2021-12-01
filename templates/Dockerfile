FROM node:12.18.1

ARG DEBIAN_FRONTEND=noninteractive

COPY . /templates

WORKDIR /templates


RUN rm -rf node_modules
RUN npm install vue
RUN npm install
RUN npm install @vue/cli-service
COPY . .
CMD npm run serve