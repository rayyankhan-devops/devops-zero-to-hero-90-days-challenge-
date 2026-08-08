# STAGE 1: The Builder Stage
# We use Python 3.12 on Alpine Linux to download and compile all software packages we need
FROM python:3.12-alpine AS builder

# Tell Python not to create extra cached bytecode (.pyc) files so we save disk space
ENV PYTHONDONTWRITEBYTECODE=1

# Tell Python to print log messages immediately to the console without delay
ENV PYTHONUNBUFFERED=1

# Set the folder where we will build our project inside the container
WORKDIR /build

# Install basic Linux compiler tools needed to build database drivers
RUN apk add --no-cache build-base libpq-dev binutils

# Create an isolated folder (virtual environment) at /opt/venv to keep our Python libraries organized
RUN python -m venv /opt/venv

# Add our virtual environment folder to the system PATH so Python uses these installed tools automatically
ENV PATH="/opt/venv/bin:$PATH"

# Copy the requirements file (list of Python libraries needed for Tasks service) into the container
COPY services/tasks/requirements.txt .

# Upgrade basic installer tools (pip, setuptools, wheel) to the newest versions
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install all required Python packages listed in requirements.txt without creating extra cache files
RUN pip install --no-cache-dir --no-compile -r requirements.txt

# Delete temp Python cache folders (__pycache__) to make the image smaller
RUN find /opt/venv -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Delete test folders from installed packages to save space
RUN find /opt/venv -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true

# Remove unnecessary debugging data from binary files (.so) to shrink file sizes
RUN find /opt/venv -name "*.so" -exec strip --strip-unneeded {} + 2>/dev/null || true

# Delete any leftover bytecode (.pyc) files
RUN find /opt/venv -name "*.pyc" -delete

# Delete any leftover optimized bytecode (.pyo) files
RUN find /opt/venv -name "*.pyo" -delete

# Remove build tools (pip, setuptools) from the virtual environment since we don't need them at runtime
RUN rm -rf /opt/venv/lib/python3.12/site-packages/pip* \
           /opt/venv/lib/python3.12/site-packages/setuptools* \
           /opt/venv/lib/python3.12/site-packages/wheel*


# STAGE 2: The Final Runner Stage
# We start fresh with a clean, super small Python image to run our application safely
FROM python:3.12-alpine AS runner

# Keep preventing Python from creating bytecode files
ENV PYTHONDONTWRITEBYTECODE=1

# Keep printing logs immediately
ENV PYTHONUNBUFFERED=1

# Tell the container where to find our installed virtual environment binaries
ENV PATH="/opt/venv/bin:$PATH"

# Tell Python where our application code is located so imports work smoothly
ENV PYTHONPATH="/app"

# Set the working directory where our app will run
WORKDIR /app

# Update the Linux package database
RUN apk update

# Upgrade existing operating system packages to fix any security vulnerabilities
RUN apk upgrade --no-cache

# Install PostgreSQL runtime library (libpq) and curl tool for checking server health
RUN apk add --no-cache libpq curl

# Remove temporary installation files and caches to make the final image as small as possible
RUN rm -rf /usr/local/lib/python3.12/site-packages/pip* \
           /usr/local/lib/python3.12/site-packages/setuptools* \
           /usr/local/lib/python3.12/ensurepip \
           /var/cache/apk/* /tmp/* ~/.cache

# Copy the prepared virtual environment from Stage 1 into our final image
COPY --from=builder /opt/venv /opt/venv

# Copy our shared helper code into /app/shared/
COPY shared/ /app/shared/

# Copy our Tasks microservice code into /app/services/tasks/
COPY services/tasks/ /app/services/tasks/

# Copy Auth microservice user models so Tasks service knows about user accounts
COPY services/auth/ /app/services/auth/

# Create a restricted user group named 'appgroup'
RUN addgroup -g 10003 -S appgroup

# Create a restricted normal user named 'appuser' inside 'appgroup'
RUN adduser -u 10003 -S appuser -G appgroup

# Give our restricted user full ownership of the /app folder
RUN chown -R appuser:appgroup /app

# Switch to the restricted 'appuser' so the app does not run as root/administrator
USER appuser

# Open port 5003 for the Tasks service
EXPOSE 5003

# Automatically check every 30 seconds if the Tasks service health endpoint is working
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5003/api/health || exit 1

# Start the production web server (Gunicorn) to serve the Tasks application on port 5003
CMD ["gunicorn", "--bind", "0.0.0.0:5003", "--workers", "2", "--threads", "2", "services.tasks.app:app"]
