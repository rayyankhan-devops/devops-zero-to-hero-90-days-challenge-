# Stage 1: Build React Production Bundle
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependency manifests first for build caching
COPY package.json package-lock.json* ./

RUN npm ci || npm install

# Copy source code and build
COPY . .
RUN npm run build

# Stage 2: Official Non-Root Unprivileged Nginx Image
FROM nginxinc/nginx-unprivileged:alpine

# Copy custom non-root Nginx config (listens on port 8080)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy compiled static site from Stage 1
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]