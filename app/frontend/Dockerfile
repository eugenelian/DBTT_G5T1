FROM node:20-alpine AS builder

WORKDIR /app/app/frontend

COPY package.json ./

RUN npm install

COPY . .

EXPOSE 8080

RUN npm run build

# Set up Production API-gateway

FROM nginx:alpine

COPY --from=builder /app/app/frontend/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
