FROM node:20

WORKDIR /app
COPY ./frontend /app

COPY . .

EXPOSE 5173

# Remove existing node_modules and install fresh at container startup
CMD ["sh", "-c", "rm -rf node_modules package-lock.json && npm install --legacy-peer-deps && npm run dev -- --host"]
