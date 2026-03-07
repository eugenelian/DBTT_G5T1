FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files from frontend folder
COPY app/frontend/package*.json ./

RUN npm install

# Copy the rest of the frontend source
COPY app/frontend ./

# Set environment variables
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

# ---------- Production image ----------
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY app/frontend/nginx.conf.template /etc/nginx/conf.d/nginx.conf.template
COPY app/frontend/docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x /docker-entrypoint.sh

EXPOSE 80
ENTRYPOINT ["/docker-entrypoint.sh"]
