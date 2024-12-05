FROM node:18-slim AS build

WORKDIR /frontend

COPY package.json package-lock.json* ./
RUN npm install --no-audit --no-fund

COPY . .
RUN npm run build
