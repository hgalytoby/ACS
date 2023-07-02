FROM node:18.16.1-alpine as frontend
WORKDIR /usr/src/app
COPY ./frontend/. .
RUN npm i
RUN npm run build

FROM nginx:1.20.1-alpine
WORKDIR /usr/src/app
COPY --from=frontend /usr/src/app/dist ./dist
COPY nginx.conf /etc/nginx/conf.d/default.conf
CMD nginx -g 'daemon off;'