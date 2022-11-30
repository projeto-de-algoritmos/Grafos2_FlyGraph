FROM node:13.12.0-alpine
WORKDIR /app/frontend

COPY package.json package-lock.json ./
RUN npm install -s
RUN npm install react-scripts@5.*.* -g -s
RUN npm install -g -s create-react-app
COPY . ./
RUN npm run build
EXPOSE 3000