# Stage 1: Build the frontend using Node
FROM node:20 AS builder

WORKDIR /app
COPY ./frontend /app

RUN npm install --legacy-peer-deps
RUN npm run build

# Stage 2: Serve the frontend using NGINX
FROM nginx:alpine

# Copy built files to NGINX's default public folder
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose the default port NGINX uses
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
