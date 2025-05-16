FROM node:20

WORKDIR /app

COPY package*.json ./
RUN npm i
RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "install"]
CMD ["npm", "run", "dev", "--", "--host"]
