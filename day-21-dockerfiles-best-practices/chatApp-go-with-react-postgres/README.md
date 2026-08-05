# 🚀 Go + React + PostgreSQL Fullstack Chat App (`chatApp-go-with-react-postgres`)

A production-ready fullstack real-time chat application built with **Go** (API + WebSockets), **React 18 + Vite** (glassmorphic dark UI), and **PostgreSQL 17** (persistent database).

This repository is crafted to demonstrate professional software practices, clean architecture, environment variable handling (`.env`, `.env.local`), and **hands-on Docker containerization using non-root security best practices for BOTH backend & frontend**.

---

## 📌 Architecture & Tech Stack

```
                        ┌──────────────────────────────────────────────────┐
                        │             Docker Network: chat-app-network     │
                        │                                                  │
┌─────────────────┐     │   ┌──────────────────┐    ┌──────────────────┐   │
│ Browser         │────►│   │ chatapp-frontend │    │  chatapp-backend │   │
│ http://localhost│3000:│   │(Nginx Non-Root)  │    │ (Go Non-Root User│   │
│                 │8080 │   │  Port 8080       │    │  appuser:10001)  │   │
└─────────────────┘     │   └──────────────────┘    └────────┬─────────┘   │
                        │                                    │             │
                        │                           DB_HOST=local-postgres │
                        │                                    ▼             │
                        │                           ┌──────────────────┐   │
                        │                           │  local-postgres  │   │
                        │                           │  (PostgreSQL 17) │   │
                        │                           │  Port 5432       │   │
                        │                           └──────────────────┘   │
                        └──────────────────────────────────────────────────┘
```

- **Backend**: Go 1.21, `database/sql`, `lib/pq` (PostgreSQL driver), `gorilla/websocket` (real-time chat hub), `godotenv` (environment loading), `rs/cors`.
- **Frontend**: React 18, Vite, Glassmorphism Vanilla CSS, `lucide-react` icons, WebSockets API.
- **Database**: PostgreSQL 17 (Auto-initializes table schema `messages` on startup).
- **Security & Docker**: Non-root execution for both frontend (`nginx` UID 101) & backend (`appuser` UID 10001), multi-stage builds, custom Docker network DNS resolution (`chat-app-network`).

---

## 📁 Repository Structure

```
chatApp-go-with-react-postgres/
├── backend/
│   ├── config/config.go      # Environment loader (reads .env or system env vars)
│   ├── db/db.go              # PostgreSQL connection & auto-table schema creation
│   ├── handlers/chat.go      # REST message history API & WebSocket client hub
│   ├── models/message.go     # Message struct definition
│   ├── main.go               # Go entrypoint & CORS router
│   ├── go.mod / go.sum       # Go modules
│   ├── .env.example          # Backend env template
│   ├── .env                  # Backend active local environment
│   └── Dockerfile            # Non-Root Multi-Stage Go Dockerfile (appuser UID 10001)
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Modern Chat interface (join modal, channels, WS)
│   │   ├── index.css         # Glassmorphism dark theme & animations
│   │   └── main.jsx          # React DOM entrypoint
│   ├── nginx.conf            # Unprivileged Nginx configuration (Port 8080)
│   ├── package.json          # Frontend dependencies (React, Vite, Lucide)
│   ├── vite.config.js        # Vite dev server configuration
│   ├── .env.example          # Frontend env template
│   ├── .env.local            # Frontend active local environment overrides
│   └── Dockerfile            # Non-Root Multi-Stage Dockerfile (nginxinc/nginx-unprivileged)
├── .env.example              # Root environment template
└── README.md                 # Master documentation & guide
```

---

## 🔐 Environment Variables (`.env`, `.env.local`, `.env.example`)

### 1. Backend Configuration (`backend/.env`)
| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `PORT` | `8080` | Port Go HTTP & WebSocket server listens on |
| `DB_HOST` | `localhost` | `localhost` for local machine, or `local-postgres` inside Docker |
| `DB_PORT` | `5432` | PostgreSQL database port |
| `DB_USER` | `postgres` | Database username |
| `DB_PASSWORD` | `postgres` | Database password |
| `DB_NAME` | `chatapp` | Database name |

> **💡 How Go reads environment variables**: Go uses `godotenv.Load()`. If environment variables are set in the operating system or container (via `docker run -e DB_HOST=...`), Go prioritizes system variables over `.env` file values!

### 2. Frontend Configuration (`frontend/.env.local`)
| Variable | Value | Description |
| :--- | :--- | :--- |
| `VITE_API_URL` | `http://localhost:8080` | Backend REST API endpoint |
| `VITE_WS_URL` | `ws://localhost:8080` | Backend WebSocket endpoint |

> **⚠️ Vite Security Requirement**: All client-side environment variables in Vite **MUST** start with `VITE_` (e.g. `VITE_API_URL`). Non-prefixed variables are excluded from the browser bundle for security.

---

## 🛠️ Running Locally (Without Docker)

### Step 1: Start PostgreSQL
```bash
docker run -d \
  --name local-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=chatapp \
  -p 5432:5432 \
  postgres:17-alpine
```

### Step 2: Start Go Backend
```bash
cd backend
go run main.go
```
*Console output:* `Successfully connected to PostgreSQL at localhost:5432` and `Server listening on port :8080`.

### Step 3: Start React Frontend
In a new terminal:
```bash
cd frontend
npm run dev
```
Open **`http://localhost:3000`** in your browser.

---

## 🐳 Complete Manual Docker Guide (Step-by-Step)

Here is the exact complete command sequence to create your Docker network and run all 3 containers.

### 1. Create a Shared Docker Network
Create a bridge network so containers can communicate using their container names as hostnames:
```bash
docker network create chat-app-network
```

---

### 2. Run PostgreSQL Container
```bash
docker run -d \
  --name local-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=chatapp \
  -p 5432:5432 \
  --network chat-app-network \
  -v postgres-data:/var/lib/postgresql/data \
  postgres:17-alpine
```

---

### 3. Build & Run Non-Root Go Backend Container

#### Non-Root Go Dockerfile Details:
The Go container creates a non-privileged user `appuser` (UID `10001`) and switches context (`USER appuser`) so the binary runs securely without root privileges.

#### Build the Backend Image:
```bash
docker build -t chatapp-backend backend
```

#### Run the Backend Container:
```bash
docker run -d \
  --name chatapp-backend \
  --network chat-app-network \
  -p 8080:8080 \
  -e PORT=8080 \
  -e DB_HOST=local-postgres \
  -e DB_PORT=5432 \
  -e DB_USER=postgres \
  -e DB_PASSWORD=postgres \
  -e DB_NAME=chatapp \
  chatapp-backend
```
*(Notice: `-e DB_HOST=local-postgres` uses Docker's internal network DNS to locate the database container!)*

---

### 4. Build & Run Non-Root React Frontend Container

#### Why Non-Root? (Security Best Practice)
Standard Nginx images run as `root` (UID 0) and try to write to `/run/nginx.pid`, resulting in `Permission denied` when executed without root privileges.
We use **`nginxinc/nginx-unprivileged:alpine`** with unprivileged port **`8080`** (ports < 1024 require root privileges in Linux).

#### Build the Frontend Image:
```bash
docker build -t rayyan12311/chatapp-frontend-go:v1.0.0 frontend
```

#### Run the Frontend Container:
```bash
docker run -d \
  --name chatapp-frontend \
  --network chat-app-network \
  -p 3000:8080 \
  rayyan12311/chatapp-frontend-go:v1.0.0
```

---

## 🌐 Complete Docker Network Commands Cheat-Sheet

Docker Networks allow containers to discover each other by container name (e.g. `chatapp-backend` connecting to `local-postgres`).

| Action | Command | Explanation |
| :--- | :--- | :--- |
| **Create Network** | `docker network create chat-app-network` | Creates a custom bridge network |
| **List Networks** | `docker network ls` | Displays all active Docker networks |
| **Inspect Network** | `docker network inspect chat-app-network` | Shows connected containers & IP addresses |
| **Connect Container** | `docker network connect chat-app-network <container-name>` | Connects a running container to network |
| **Disconnect Container**| `docker network disconnect chat-app-network <container-name>` | Disconnects a container from network |
| **Remove Network** | `docker network rm chat-app-network` | Deletes a custom network (when no containers attached) |
| **Prune Unused Networks**| `docker network prune` | Removes all unused Docker networks |

---

## 💾 Complete Docker Volume Commands Cheat-Sheet

Docker Volumes persist your database data independently of container lifecycles (so PostgreSQL data isn't lost when containers are deleted).

| Action | Command | Explanation |
| :--- | :--- | :--- |
| **Create Named Volume**| `docker volume create postgres-data` | Creates a persistent named volume |
| **List Volumes** | `docker volume ls` | Lists all volumes stored by Docker |
| **Inspect Volume** | `docker volume inspect postgres-data` | Shows host storage mount path (`/var/lib/docker/volumes/...`) |
| **Mount Volume** | `docker run -v postgres-data:/var/lib/postgresql/data ...` | Mounts volume inside PostgreSQL container |
| **Remove Volume** | `docker volume rm postgres-data` | Deletes a volume and all its stored data |
| **Prune Unused Volumes**| `docker volume prune` | Deletes all unattached volumes |

---

## 🧪 Verification & Inspection Commands

### Check All Running Containers
```bash
docker ps
```

### Verify Non-Root User Execution for Both Containers
```bash
# Check Frontend container user:
docker exec chatapp-frontend whoami
# Output: nginx (UID 101)

# Check Backend container user:
docker exec chatapp-backend whoami
# Output: appuser (UID 10001)
```

### Inspect Backend Real-time Logs
```bash
docker logs -f chatapp-backend
```

### Query Database Messages Directly inside Postgres
```bash
docker exec -it local-postgres psql -U postgres -d chatapp -c "SELECT * FROM messages;"
```

---

## 🌐 Testing Real-Time Chat

1. Open **`http://localhost:3000`** in your browser.
2. Enter your name (e.g. **Rayyan**).
3. Open a second browser tab (or Incognito window) at `http://localhost:3000` and enter a second name (e.g. **Alex**).
4. Switch between channels (`#general`, `#devops`, `#random`).
5. Send messages — they appear in real-time across both windows via WebSockets and are persisted to PostgreSQL!

Enjoy building & practicing DevOps! 🎉
