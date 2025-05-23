# First stage: build
FROM node:18 AS build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Second stage: production
FROM node:18

WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/package*.json ./

RUN npm install --only=production
USER heimhere

CMD ["node", "dist/index.js"]
