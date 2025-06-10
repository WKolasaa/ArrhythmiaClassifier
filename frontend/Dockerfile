FROM node:20

WORKDIR /app
COPY . . 

EXPOSE 5173

RUN npm install --legacy-peer-deps
RUN npm run build
RUN npm install -g serve

CMD ["serve", "-s", "dist", "-l", "5173"]
