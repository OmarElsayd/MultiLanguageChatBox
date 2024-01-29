FROM node:latest as build-step

WORKDIR /usr/src/app

COPY mlcb/package*.json ./

RUN npm install

COPY mlcb/ ./

RUN npm run build --prod

FROM nginx:alpine

RUN mkdir -p /etc/nginx/ssl

COPY --from=build-step /usr/src/app/dist/mlcb/browser /usr/share/nginx/html

# Prod settings
RUN echo "$SSL_CERTIFICATE" > /etc/ssl/cert.crt
RUN echo "$SSL_KEY" > /etc/ssl/cert.key

# Dev settings
#COPY cert.pem /etc/nginx/ssl/cert.pem
#COPY key.pem /etc/nginx/ssl/key.pem

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
