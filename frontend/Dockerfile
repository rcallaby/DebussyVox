FROM node:20-alpine

WORKDIR /app
COPY package.json .
COPY package-lock.json* ./
RUN npm ci --silent

COPY . .

RUN npm run build

# Use a lightweight static server
RUN npm install -g serve

EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
