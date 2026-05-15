# Docker Setup Guide

## Prerequisites
- Docker and Docker Compose installed
- Port 3000, 5173, 8000, 8001, 8002, 8003, 5432, 6379 are available

## Quick Start

### 1. Build and Start All Services

```bash
cd Innovators_Lab-
docker-compose up --build
```

This will:
- Create PostgreSQL database with all necessary databases
- Start Redis cache
- Build and start API Gateway (port 8000)
- Build and start User Service (port 8001)
- Build and start Submission Service (port 8002)
- Build and start Tournament Service (port 8003)
- Build and start Frontend (ports 3000, 5173)

### 2. Wait for Services to Be Ready

All services have health checks. Wait for messages like:
```
user-service  | Starting development server at http://0.0.0.0:8001/
```

### 3. Access the Application

- **Frontend**: http://localhost:3000 or http://localhost:5173
- **API Gateway**: http://localhost:8000
- **User Service**: http://localhost:8001
- **Submission Service**: http://localhost:8002
- **Tournament Service**: http://localhost:8003
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## Database Initialization

The databases are automatically created via `init-db.sql`:
- `user_db` - User authentication and profiles
- `gateway_db` - API Gateway data
- `submission_db` - Submission and task data
- `tournament_db` - Tournament management
- `rank_db` - Rankings and scores

## Environment Variables

### User Service (.env)
```
SECRET_KEY=user-service-secret-key-change-in-production
DEBUG=True
DB_NAME=user_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1,user-service,0.0.0.0
```

### API Gateway (.env)
```
SECRET_KEY=api-gateway-secret-key-change-in-production
DEBUG=True
DB_NAME=gateway_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1,api-gateway,0.0.0.0
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
VITE_API_GATEWAY_URL=http://localhost:8000
```

## Common Commands

### Start services
```bash
docker-compose up
```

### Start services in background
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose down
```

### Stop and remove volumes (WARNING: deletes database data)
```bash
docker-compose down -v
```

### View logs
```bash
docker-compose logs -f
```

### View logs from specific service
```bash
docker-compose logs -f user-service
```

### Access container shell
```bash
docker-compose exec user-service sh
```

### Run migrations manually
```bash
docker-compose exec user-service python manage.py migrate
```

### Create superuser
```bash
docker-compose exec user-service python manage.py createsuperuser
```

### Run Django shell
```bash
docker-compose exec user-service python manage.py shell
```

## Troubleshooting

### Port Already in Use
If a port is already in use, modify the port mapping in `docker-compose.yml`:
```yaml
ports:
  - "8001:8001"  # Change first 8001 to another port like 8011
```

### Database Connection Error
Check if PostgreSQL is running:
```bash
docker-compose logs postgres
```

### Migrations Not Running
Run migrations manually:
```bash
docker-compose exec user-service python manage.py migrate
docker-compose exec api-gateway python manage.py migrate
```

### Container Exits Immediately
Check logs:
```bash
docker-compose logs user-service
```

### CORS Errors
The CORS is configured in docker-compose.yml and settings.py. Make sure:
1. Frontend URL is in CORS_ALLOWED_ORIGINS
2. Requests include correct headers
3. Check docker-compose logs for header details

## Testing API Endpoints

### Register User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

### Get Current User
```bash
curl -X GET http://localhost:8000/api/auth/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Performance Notes

- First build may take 5-10 minutes
- Database initialization takes ~10-30 seconds
- Services start in order: db → postgres → user-service → api-gateway → frontend
- Use `docker-compose up -d` for background mode

## Production Considerations

⚠️ **WARNING**: This configuration is for development only!

For production:
1. Use environment-specific settings
2. Set DEBUG=False
3. Change SECRET_KEY to secure random value
4. Use separate database credentials
5. Remove volumes that persist sensitive data
6. Use production-grade database backups
7. Implement proper logging and monitoring
8. Use reverse proxy (nginx)
9. Enable HTTPS/SSL

## Additional Resources

- API Documentation: See `API_ENDPOINTS.md`
- Django Documentation: https://docs.djangoproject.com/
- Docker Documentation: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/

---

For questions or issues, check the logs or consult the individual service documentation.
