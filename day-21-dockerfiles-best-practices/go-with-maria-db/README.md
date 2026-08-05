# Go + MariaDB Full-Stack Microservice Portal 🚀

A modern, production-ready full-stack application built with a **Go 1.22 REST API**, **MariaDB 11 database**, and a **Glassmorphic HTML/CSS/JS frontend UI**.

Designed for hands-on learning of Docker containerization, multi-stage builds, container security (non-root users & zero-vulnerability scratch images), Docker networking, and volume persistence.

---

## 📁 Architecture & Directory Structure

```
go-with-maria-db/
├── backend/
│   ├── main.go           # Go HTTP server, REST API endpoints, DB connection & auto-migrations
│   ├── go.mod            # Go module definition
│   └── go.sum            # Checksum lockfile for Go dependencies
├── public/
│   ├── index.html        # Glassmorphic UI with connection status & item management
│   ├── style.css         # Custom CSS design system (HSL tokens, glassmorphism, animations)
│   └── app.js            # Frontend JavaScript handling REST API fetch/post/delete
├── Dockerfile            # Standard Alpine multi-stage Dockerfile (for practice & learning)
├── Dockerfile.secure     # Zero-vulnerability production Dockerfile (scratch, 2.9MB, 0 CVEs)
├── .gitignore            # Git ignore rules for binaries, OS files, & secrets
├── .dockerignore         # Docker build ignore rules for lightweight context
└── README.md             # Complete project documentation
```

---

## 🐳 Dockerfile Comparison

| Feature | Standard [Dockerfile](file:///Users/muhammadrayyan/devops/docker/go-with-maria-db/Dockerfile) | Zero-Vulnerability [Dockerfile.secure](file:///Users/muhammadrayyan/devops/docker/go-with-maria-db/Dockerfile.secure) |
| :--- | :--- | :--- |
| **Use Case** | Practice & Learning | Production Deployment |
| **Base Runtime** | `alpine:latest` | `scratch` (Empty 0-byte image) |
| **Image Size** | ~22 MB | **2.9 MB** |
| **Scout Scan Status** | Standard OS libraries | **0 CVEs (100% Clean)** |
| **Shell Available** | Yes (`/bin/sh`) | **No (Zero Shell)** |
| **Binary Optimization** | Standard build | `-trimpath -ldflags="-w -s"` |
| **User Privileges** | Non-root `gouser` | Non-root `gouser:65532` |

---

## 🌐 Docker Network Commands Reference

Docker networks allow containers to communicate with each other using container names instead of temporary IP addresses.

### Network Cheat Sheet

| Command | Action |
| :--- | :--- |
| `docker network create app-net` | Create a custom bridge network named `app-net` |
| `docker network ls` | List all active Docker networks |
| `docker network inspect app-net` | View details, connected containers, & assigned IPs |
| `docker network connect app-net <container>` | Connect a running container to `app-net` |
| `docker network disconnect app-net <container>` | Disconnect a container from `app-net` |
| `docker network rm app-net` | Delete a network |
| `docker network prune` | Remove all unused networks |

### How Container Networking Works in This Project
1. When MariaDB runs on `app-net` with `--name mariadb-local`, Docker's internal DNS maps `mariadb-local` to its IP.
2. The Go App container connects to `app-net` and accesses MariaDB using `-e DB_HOST=mariadb-local`.

---

## 💾 Docker Volume Commands Reference (Data Persistence)

Docker volumes persist database data on your host disk so that data is not lost when containers are stopped or deleted.

### Volume Cheat Sheet

| Command | Action |
| :--- | :--- |
| `docker volume create mariadb_data` | Create a named volume for database persistence |
| `docker volume ls` | List all Docker volumes on host |
| `docker volume inspect mariadb_data` | Inspect volume storage path on host system |
| `docker volume rm mariadb_data` | Remove a volume (deletes database data) |
| `docker volume prune` | Remove all unused volumes |

### Running MariaDB with Persistent Volume Mounts

- **Named Volume Syntax (Recommended)**:
  ```bash
  docker run -d --name mariadb-local \
    --network app-net \
    -v mariadb_data:/var/lib/mysql \
    -e MARIADB_ROOT_PASSWORD=rootpassword \
    -e MARIADB_DATABASE=mariadb_db \
    -e MARIADB_USER=mariadb_user \
    -e MARIADB_PASSWORD=mariadb_password \
    -p 3306:3306 \
    mariadb:11.2
  ```

- **Bind Mount Syntax (Host directory)**:
  ```bash
  docker run -d --name mariadb-local \
    --network app-net \
    -v $(pwd)/mariadb_data:/var/lib/mysql \
    -e MARIADB_ROOT_PASSWORD=rootpassword \
    -e MARIADB_DATABASE=mariadb_db \
    -e MARIADB_USER=mariadb_user \
    -e MARIADB_PASSWORD=mariadb_password \
    -p 3306:3306 \
    mariadb:11.2
  ```

---

## 🛠️ Complete Step-by-Step Execution Guide

```bash
# 1. Create a custom Docker network
docker network create app-net

# 2. Create a persistent volume for MariaDB
docker volume create mariadb_data

# 3. Start MariaDB container on the network with volume persistence
docker run -d --name mariadb-local \
  --network app-net \
  -v mariadb_data:/var/lib/mysql \
  -e MARIADB_ROOT_PASSWORD=rootpassword \
  -e MARIADB_DATABASE=mariadb_db \
  -e MARIADB_USER=mariadb_user \
  -e MARIADB_PASSWORD=mariadb_password \
  -p 3306:3306 \
  mariadb:11.2

# 4. Build the Go Docker image
# Option A: Zero-vulnerability production image (2.9MB, 0 CVEs)
docker build -t rayyan12311/basic-go-app:v1.0.2 -f Dockerfile.secure .

# Option B: Standard practice image
docker build -t rayyan12311/basic-go-app:v1.0.0 -f Dockerfile .

# 5. Run the Go App container on the network
docker run -d --name go-app \
  --network app-net \
  -e DB_HOST=mariadb-local \
  -e DB_PORT=3306 \
  -e DB_USER=mariadb_user \
  -e DB_PASSWORD=mariadb_password \
  -e DB_NAME=mariadb_db \
  -p 8080:8080 \
  rayyan12311/basic-go-app:v1.0.2
```

Access the frontend application at **[http://localhost:8080](http://localhost:8080)**.

---

## 📡 REST API Specifications

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Serves static frontend application (`public/index.html`) |
| `GET` | `/api/health` | Returns server health and MariaDB connection status |
| `GET` | `/api/items` | Fetches all stored items from MariaDB |
| `POST` | `/api/items` | Inserts a new record into MariaDB (`{"title": "...", "description": "..."}`) |
| `DELETE` | `/api/items?id=X` | Deletes a record from MariaDB by ID |

---

## 💻 Interacting with MariaDB via CLI

To inspect or query the MariaDB database directly inside its container:

```bash
docker exec -it mariadb-local mariadb -u mariadb_user -pmariadb_password mariadb_db
```

SQL Query Examples:
```sql
SHOW TABLES;
SELECT * FROM items;
```
