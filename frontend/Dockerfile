FROM node:20

WORKDIR /app

COPY package*.json ./

RUN npm cache clean --force && \
    rm -rf node_modules package-lock.json && \
    npm install

COPY . .

EXPOSE 3000
EXPOSE 5173

CMD ["npm", "run", "dev"]
