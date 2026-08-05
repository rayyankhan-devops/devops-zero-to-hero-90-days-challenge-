# STAGE 1: Builder Stage
FROM golang:1.22-alpine AS builder

WORKDIR /usr/src/app

# Copy dependency definition files
COPY backend/go.mod backend/go.sum ./
RUN go mod download

# Copy backend source code & public frontend files
COPY backend/ ./
COPY public/ ../public/

# Build static binary
RUN CGO_ENABLED=0 GOOS=linux go build -o /server main.go


# STAGE 2: Standard Alpine Runtime Stage
FROM alpine:latest

RUN apk --no-cache add ca-certificates

# Create non-root group and user (gouser:gouser)
RUN addgroup -S gouser && adduser -S -G gouser gouser

WORKDIR /app

# Copy binary and static assets with non-root ownership
COPY --from=builder --chown=gouser:gouser /server ./server
COPY --from=builder --chown=gouser:gouser /usr/src/public ../public

# Switch to non-root user
USER gouser

EXPOSE 8080

CMD ["./server"]