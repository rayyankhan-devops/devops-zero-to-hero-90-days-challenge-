# Use Docker's modern build features
# syntax=docker/dockerfile:1.7

# Start with a super small, lightweight Nginx web server base image (~15MB)
# Nginx is used to serve our website and handle web traffic securely without root permissions
FROM nginxinc/nginx-unprivileged:1.27-alpine-slim

# Create a build variable for the app version (default is 1.0.0)
ARG VERSION=1.0.0

# Create a build variable to store the date when the image was built
ARG BUILD_DATE

# Create a build variable to store the Git commit ID reference
ARG VCS_REF

# Temporarily switch to administrator (root) user to install updates safely
USER root

# Update the operating system packages to fix any security bugs, then delete leftover cache to save space
RUN apk update && apk upgrade --no-cache && rm -rf /var/cache/apk/* /tmp/* /usr/share/nginx/html/*

# Copy our custom Nginx web server settings so it knows how to route web requests to our backend services
COPY --chown=101:101 default.conf /etc/nginx/conf.d/default.conf

# Copy our main website webpage (index.html) into Nginx's public web folder
COPY --chown=101:101 index.html /usr/share/nginx/html/index.html

# Copy our website styling file (style.css) into Nginx's public web folder
COPY --chown=101:101 style.css /usr/share/nginx/html/style.css

# Copy our website code logic file (app.js) into Nginx's public web folder
COPY --chown=101:101 app.js /usr/share/nginx/html/app.js

# Switch back to a regular non-admin user (ID 101) for safety, so hackers cannot take over the server
USER 101

# Label the container image with basic info like title, author, description, and source link
LABEL \
    org.opencontainers.image.title="SecretVault Frontend" \
    org.opencontainers.image.description="Production-ready SecretVault frontend built with HTML, CSS and JavaScript" \
    org.opencontainers.image.version="${VERSION}" \
    org.opencontainers.image.authors="Muhammad Rayyan <rkkhan0750@gmail.com>" \
    org.opencontainers.image.vendor="Rayyan DevOps" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.source="https://github.com/rayyankhan-devops/SecretVault-devsecops" \
    org.opencontainers.image.documentation="https://github.com/rayyankhan-devops/SecretVault-devsecops/blob/main/README.md" \
    org.opencontainers.image.url="https://github.com/rayyankhan-devops/SecretVault-devsecops" \
    org.opencontainers.image.revision="${VCS_REF}" \
    org.opencontainers.image.created="${BUILD_DATE}"

# Tell Docker that this container accepts incoming web traffic on port 8080
EXPOSE 8080

# Check every 30 seconds if the web server is still working properly
HEALTHCHECK --interval=30s \
            --timeout=3s \
            --start-period=5s \
            --retries=3 \
CMD wget --spider --quiet http://127.0.0.1:8080/ || exit 1