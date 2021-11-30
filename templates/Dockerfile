FROM node:12.18.1
ENV NODE_ENV=production

ARG DEBIAN_FRONTEND=noninteractive

COPY . /templates

WORKDIR /templates

RUN rm -rf node_modules
RUN npm install @vue/cli-service
RUN npm install 
CMD npm run serve