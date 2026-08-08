#!/usr/bin/env bash

# Stop running the script immediately if any step fails or reports an error
set -e

# Name of our shared Docker network
NETWORK_NAME="securevault"

# Default to using PostgreSQL database unless specified otherwise
USE_POSTGRES=${1:-"true"}

# Step 1 Message
echo "=== 1. Checking Docker Network ==="

# Check if our 'securevault' network exists on your computer
if ! docker network inspect "$NETWORK_NAME" >/dev/null 2>&1; then
    # Network does not exist yet, so we create it
    echo "Creating Docker network: $NETWORK_NAME"
    docker network create "$NETWORK_NAME"
else
    # Network already exists, so we keep using it
    echo "Docker network '$NETWORK_NAME' already exists."
fi

# Define a helper function to check if a Docker image is already built locally
ensure_image() {
    # Store the image tag name
    local img_tag="$1"
    # Store path to Dockerfile
    local dockerfile_path="$2"
    # Store build folder path
    local build_ctx="$3"

    echo "=== Checking local image: $img_tag ==="
    # Check if image already exists in Docker's cache
    if docker image inspect "$img_tag" >/dev/null 2>&1; then
        # Image exists, so skip building to save time
        echo "✅ Local image '$img_tag' found. Using local image."
    else
        # Image is missing, so build it now using Dockerfile
        echo "⚠️ Image '$img_tag' not found locally. Building image..."
        docker build -t "$img_tag" -f "$dockerfile_path" "$build_ctx"
    fi
}

# Make sure Auth service image is available (builds if missing)
ensure_image "secretvault-auth:v1.0.0" "services/auth/Dockerfile" "."

# Make sure Notes service image is available (builds if missing)
ensure_image "secretvault-notes:v1.0.0" "services/notes/Dockerfile" "."

# Make sure Tasks service image is available (builds if missing)
ensure_image "secretvault-tasks:v1.0.0" "services/tasks/Dockerfile" "."

# Make sure Frontend image is available (builds if missing)
ensure_image "securevault-frontend:v1.0.0" "frontend/Dockerfile" "./frontend"

# Check if user wants PostgreSQL database
if [ "$USE_POSTGRES" = "true" ]; then
    echo "=== 2. Starting PostgreSQL Database Container ==="
    # Remove any old database container running under the same name
    docker rm -f securevault-db 2>/dev/null || true
    # Run the PostgreSQL 16 database container in the background
    docker run -d \
      --name securevault-db \
      --network "$NETWORK_NAME" \
      -p 5432:5432 \
      -e POSTGRES_USER=secureuser \
      -e POSTGRES_PASSWORD=securepassword \
      -e POSTGRES_DB=securevault \
      -v securevault_postgres_data:/var/lib/postgresql/data \
      postgres:16-alpine

    echo "Waiting for PostgreSQL database to be ready..."
    # Keep checking until PostgreSQL database answers and is ready for connections
    until docker exec securevault-db pg_isready -U secureuser -d securevault >/dev/null 2>&1; do
        # Wait 1 second before trying again
        sleep 1
    done
    echo "✅ Database is ready!"

    # Set connection link pointing to PostgreSQL
    DB_URL="postgresql+psycopg://secureuser:securepassword@securevault-db:5432/securevault"
else
    echo "=== 2. Using Local SQLite Database ==="
    # Set connection link pointing to SQLite file
    DB_URL="sqlite:////app/shared/securevault.db"
fi

# Step 3 Message
echo "=== 3. Starting Services on Network '$NETWORK_NAME' ==="

# Remove old Auth container if running
docker rm -f secretvault-auth 2>/dev/null || true

# Run Auth service container on port 5001
docker run -d \
  --name secretvault-auth \
  --network "$NETWORK_NAME" \
  -p 5001:5001 \
  -e SECRET_KEY="dev-secret-change-in-production" \
  -e PASSWORD_SALT="securevault-salt" \
  -e DATABASE_URL="$DB_URL" \
  secretvault-auth:v1.0.0

# Remove old Notes container if running
docker rm -f secretvault-notes 2>/dev/null || true

# Run Notes service container on port 5002
docker run -d \
  --name secretvault-notes \
  --network "$NETWORK_NAME" \
  -p 5002:5002 \
  -e SECRET_KEY="dev-secret-change-in-production" \
  -e DATABASE_URL="$DB_URL" \
  secretvault-notes:v1.0.0

# Remove old Tasks container if running
docker rm -f secretvault-tasks 2>/dev/null || true

# Run Tasks service container on port 5003
docker run -d \
  --name secretvault-tasks \
  --network "$NETWORK_NAME" \
  -p 5003:5003 \
  -e SECRET_KEY="dev-secret-change-in-production" \
  -e DATABASE_URL="$DB_URL" \
  secretvault-tasks:v1.0.0

# Remove old Frontend container if running
docker rm -f securevault-frontend 2>/dev/null || true

# Run Frontend website container on port 8080
docker run -d \
  --name securevault-frontend \
  --network "$NETWORK_NAME" \
  -p 8080:8080 \
  securevault-frontend:v1.0.0

# Print success message
echo "=== 🚀 All SecretVault services & DB are running on network '$NETWORK_NAME' ==="

# Display all running containers on our network
docker ps --filter "network=$NETWORK_NAME"
