FROM node:18.20.2-alpine AS frontend
WORKDIR /usr/src/app
COPY frontend .
RUN npm cache clean --force && npm install
RUN npm run build

FROM nginx:1.25.2-alpine
WORKDIR /usr/src/app
COPY --from=frontend /usr/src/app/dist ./dist
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
CMD nginx -g 'daemon off;'