# Stage 1: Build Stage
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Copy dependency files for layer caching
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build static Go binary
RUN CGO_ENABLED=0 GOOS=linux go build -o server .

# Stage 2: Minimal Non-Root Runtime Stage
FROM alpine:3.19

WORKDIR /app

# Create a non-root user and group (UID/GID 10001)
RUN addgroup -g 10001 -S appgroup && \
    adduser -u 10001 -S appuser -G appgroup

# Copy compiled binary from builder stage and assign ownership to appuser
COPY --from=builder --chown=appuser:appgroup /app/server .

# Switch context from root to non-root user 'appuser'
USER appuser

EXPOSE 8080

CMD ["./server"]
