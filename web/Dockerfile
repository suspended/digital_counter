# Stage 1
FROM node:13 as react-build

ARG REACT_APP_API_SERVER="http://localhost:5000"

WORKDIR /web

COPY package.json /web/package.json
COPY package-lock.json /web/package-lock.json

RUN npm ci --silent

COPY ./public /web/public
COPY ./src /web/src

RUN npm run build

# Stage 2
FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=react-build /web/build /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]