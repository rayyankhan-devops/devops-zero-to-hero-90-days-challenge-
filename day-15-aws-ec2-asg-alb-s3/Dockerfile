# Day 15 Standalone Dockerfile for Nginx Static Landing Page
FROM nginx:1.25-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY userdata_nginx.sh /var/www/html/index.html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
