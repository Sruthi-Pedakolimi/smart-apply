FROM node:20-alpine AS builder

WORKDIR /smart-apply/frontend

COPY package*.json ./
RUN npm ci

# copy the code from this frontend to the docker frontend
COPY . .
RUN npm run build


# second stage
FROM nginx:stable-alpine
COPY --from=builder /smart-apply/frontend/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]