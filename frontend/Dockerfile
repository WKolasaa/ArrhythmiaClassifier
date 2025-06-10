# Build Stage
FROM node:20 AS build

WORKDIR /app
COPY ./frontend/ /app/

RUN npm install --legacy-peer-deps
RUN npm run build

# Serve Stage
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
