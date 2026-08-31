
FROM nginx:stable-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /etc/nginx/html/index.html
COPY datahub.png /etc/nginx/html/datahub.png

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
