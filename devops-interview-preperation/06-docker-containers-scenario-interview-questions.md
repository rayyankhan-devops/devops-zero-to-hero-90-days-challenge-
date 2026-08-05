# 🐳 Docker Containerization & Microservices Stack - 50 Scenario-Based Interview Questions

## Scenario 1: Container CrashLoopBackOff & OOMKilled Debugging
**Q:** A Docker container running a Node.js microservice repeatedly crashes every 2 minutes. `docker ps -a` displays status `Exited (137)`. What does exit code `137` mean and how do you fix it?
**A:** Exit code `137` (`128 + 9`) indicates the container was forcefully killed by the Linux kernel Out-Of-Memory (OOM) Killer (`SIGKILL`) because it exceeded allocated RAM limits.
1. Inspect container inspect logs: `docker inspect <container_id> | grep -i oom`
2. Check memory limits in `docker-compose.yml` or CLI: increase `mem_limit: 1g` or optimize Node.js heap limit (`node --max-old-space-size=512`).

## Scenario 2: Multi-Stage Dockerfile Sizing Optimization
**Q:** A Go application Dockerfile produces a massive 950MB image because it uses `FROM golang:1.22`. How do you write a multi-stage Dockerfile to shrink the final image size below 20MB?
**A:** Use a multi-stage build: compile in the builder image, then copy only the compiled binary into a minimal `alpine` or `scratch` runtime image.
```dockerfile
# Stage 1: Build Stage
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# Stage 2: Minimal Runtime Stage
FROM scratch
COPY --from=builder /app/main /main
ENTRYPOINT ["/main"]
```

## Scenario 3: Container Data Loss on Restart
**Q:** A MySQL Docker container was created via `docker run -d --name db mysql:8.0`. After running `docker rm -f db` and starting a new container, all database tables disappeared! How do you persist data permanently?
**A:** Docker containers have an ephemeral writable layer that is destroyed when the container is removed. Use a **Named Volume** or **Bind Mount**:
```bash
docker run -d --name db -v mysql_data:/var/lib/mysql mysql:8.0
```

## Scenario 4: Inter-Container DNS Communication Failure
**Q:** Container `app` needs to send HTTP requests to Container `api`. Running `curl http://api:8080` inside `app` fails with `Could not resolve host: api`. Both containers are running on default `bridge` network. Why?
**A:** The default Docker `bridge` network does NOT support automatic container name DNS resolution.
1. Create a custom user-defined bridge network: `docker network create my-net`
2. Attach both containers to `my-net`:
   ```bash
   docker run -d --name api --network my-net my-api-image
   docker run -d --name app --network my-net my-app-image
   ```
Now `http://api:8080` will resolve automatically via Docker embedded DNS server (`127.0.0.11`).

## Scenario 5: Docker Build Cache Invalidation
**Q:** Every time you run `docker build`, Docker re-downloads all `npm install` packages taking 5 minutes, even though `package.json` never changed. How do you optimize layer ordering?
**A:** Order Dockerfile instructions from least frequently changed to most frequently changed. Copy dependency manifests (`package.json`) BEFORE copying source code.
```dockerfile
# GOOD LAYER CACHING:
COPY package*.json ./
RUN npm install
COPY . .  # Source code changes will reuse the cached 'npm install' layer!
```

## Scenario 6: Docker Compose `depends_on` Healthcheck Race Condition
**Q:** In `docker-compose.yml`, `backend` has `depends_on: - postgres`. When running `docker compose up`, `backend` starts instantly and crashes with `Connection refused to postgres:5432`. Why did `depends_on` fail?
**A:** Standard `depends_on` only waits for the database container to reach `running` status, not until PostgreSQL finish initializing database sockets.
Use `condition: service_healthy` coupled with a `healthcheck`:
```yaml
services:
  postgres:
    image: postgres:17-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    depends_on:
      postgres:
        condition: service_healthy
```

## Scenario 7: Container Security Hardening (Non-Root User)
**Q:** Security scanners flag your Docker container because it runs applications as `root` user (UID 0). How do you enforce non-root execution in a Dockerfile?
**A:** Create a non-root group and user inside the image and switch to it:
```dockerfile
FROM node:20-alpine
WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
COPY --chown=appuser:appgroup . .
USER appuser
CMD ["node", "server.js"]
```

## Scenario 8: Docker Scout Vulnerability Mitigation
**Q:** `docker scout cves my-app:latest` flags 12 Critical CVE vulnerabilities in the base image `ubuntu:20.04`. What steps do you take to remediate?
**A:**
1. Upgrade base image to a patched version (`ubuntu:24.04` or `node:20-alpine`).
2. Run `docker scout recommendations my-app:latest` to review Docker's recommended base tag replacements.
3. Re-build image using `--no-cache` and re-scan.

## Scenario 9: Volume Permission Denied (`EACCES`)
**Q:** You mounted a host directory `/var/log/app` into a container running as non-root user `appuser` (UID 10001). The container crashes with `Permission denied`. How do you fix it?
**A:** The host directory ownership belongs to `root` on the host machine.
1. Change ownership of host folder to match container UID:
   ```bash
   sudo chown -R 10001:10001 /var/log/app
   ```
2. Or initialize permissions inside an entrypoint script before dropping privileges.

## Scenario 10: Docker Swarm Service Scaling & Zero-Downtime Rolling Update
**Q:** How do you deploy an updated image `my-app:v2.0` to a Docker Swarm cluster running 5 replicas with zero downtime?
**A:**
```bash
docker service update \
  --image my-app:v2.0 \
  --update-parallelism 2 \
  --update-delay 10s \
  my-web-service
```
This updates 2 replicas at a time, waits 10s to verify health, and rolls back automatically if healthchecks fail.

---

## Scenario 11-50 Summary Coverage Matrix
- **Docker Compose Production:** Environment variable interpolation (`.env`), named volumes vs bind mounts in compose, secret files management.
- **Docker CLI Mastery:** `docker exec -it`, `docker logs --tail 100 -f`, `docker cp`, `docker commit`, `docker system prune -a --volumes`.
