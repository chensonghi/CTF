FROM node:22.8.0-slim

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

USER 404:404
CMD node index.js