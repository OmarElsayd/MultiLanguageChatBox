# Build stage for Node.js
FROM node:latest as build-step
WORKDIR /usr/src/app
COPY mlcb/package*.json ./
RUN npm install
COPY mlcb/ ./
RUN npm run build --prod

# Nginx to serve the built application
FROM nginx:alpine
COPY --from=build-step /usr/src/app/dist/mlcb/browser /usr/share/nginx/html
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
EXPOSE 443

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
