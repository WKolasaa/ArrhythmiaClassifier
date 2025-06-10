# Stage 1: Build React/Vite/Angular app
FROM node:20 AS builder
WORKDIR /app
COPY ./frontend /app
RUN npm install --legacy-peer-deps && npm run build

# Stage 2: Serve with NGINX
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
