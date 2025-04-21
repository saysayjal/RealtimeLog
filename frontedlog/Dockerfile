FROM node:20-alpine as build-stage

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

RUN npm run build || (echo "Build failed!" && ls -la && exit 1)

RUN ls -la /app/dist || (echo "No dist folder created!" && exit 1)

FROM nginx:alpine

RUN mkdir -p /usr/share/nginx/html

COPY --from=build-stage /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]