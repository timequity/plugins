# Docker Best Practices

## Dockerfile Optimization

### Layer Caching

```dockerfile
# BAD - cache invalidated on any source change
COPY . .
RUN npm install

# GOOD - dependencies cached separately
COPY package*.json ./
RUN npm ci
COPY . .
```

### Multi-stage Builds

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production (smaller image)
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/main.js"]
```

### Security

```dockerfile
# Create non-root user
RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup

# Use it
USER appuser

# Don't run as root
USER 1001:1001
```

### .dockerignore

```
node_modules
.git
.env
*.log
dist
coverage
.DS_Store
```

## Docker Compose

### Development Setup

```yaml
services:
  app:
    build:
      context: .
      target: development
    volumes:
      - .:/app
      - /app/node_modules  # Anonymous volume for deps
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    command: npm run dev
```

### Production Setup

```yaml
services:
  app:
    image: myapp:latest
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Networking

```yaml
services:
  api:
    networks:
      - backend
      - frontend

  db:
    networks:
      - backend

  nginx:
    networks:
      - frontend

networks:
  backend:
    driver: bridge
  frontend:
    driver: bridge
```

### Volumes

```yaml
volumes:
  # Named volume (persistent)
  postgres_data:
    driver: local

  # Bind mount (development)
  # ./local/path:/container/path
```

## Commands Reference

```bash
# Build
docker build -t myapp .
docker build -t myapp --no-cache .
docker build -t myapp --target builder .

# Run
docker run myapp
docker run -d myapp                    # Detached
docker run -p 3000:3000 myapp          # Port mapping
docker run -v $(pwd):/app myapp        # Bind mount
docker run --rm myapp                  # Remove after exit
docker run -it myapp sh                # Interactive shell
docker run --env-file .env myapp       # Env from file

# Logs & Debug
docker logs <container>
docker logs -f <container>             # Follow
docker exec -it <container> sh         # Shell into running
docker inspect <container>

# Cleanup
docker system prune -af                # Remove all unused
docker volume prune -f                 # Remove unused volumes
docker image prune -af                 # Remove unused images

# Compose
docker compose up -d
docker compose down
docker compose logs -f <service>
docker compose exec <service> sh
docker compose build --no-cache
```

## Image Size Optimization

| Base Image | Size | When to Use |
|------------|------|-------------|
| `node:20` | ~1GB | Never in prod |
| `node:20-slim` | ~200MB | When you need apt |
| `node:20-alpine` | ~130MB | Default choice |
| `distroless` | ~20MB | Maximum security |

### Alpine Tips

```dockerfile
# Alpine uses musl libc, may need:
RUN apk add --no-cache libc6-compat

# For native modules:
RUN apk add --no-cache python3 make g++
```
