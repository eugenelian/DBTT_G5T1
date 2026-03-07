FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files from frontend folder
COPY app/frontend/package*.json ./

RUN npm install

# Copy the rest of the frontend source
COPY app/frontend ./

RUN npm run build

# ---------- Production image ----------
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
