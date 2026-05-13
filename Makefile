.PHONY: help build up down logs test lint migrate shell clean restart

help:
	@echo "Tournament Platform - Make Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make quick-start      # Quick setup with Docker Compose"
	@echo "  make build            # Build Docker images"
	@echo "  make up               # Start all services"
	@echo "  make down             # Stop all services"
	@echo ""
	@echo "Development:"
	@echo "  make logs             # View all logs"
	@echo "  make logs-gateway     # View API Gateway logs"
	@echo "  make logs-user        # View User Service logs"
	@echo "  make logs-tournament  # View Tournament Service logs"
	@echo "  make logs-submission  # View Submission Service logs"
	@echo ""
	@echo "Testing:"
	@echo "  make test             # Run all tests"
	@echo "  make test-user        # Test User Service"
	@echo "  make test-tournament  # Test Tournament Service"
	@echo "  make test-submission  # Test Submission Service"
	@echo "  make test-gateway     # Test API Gateway"
	@echo "  make test-cov         # Run tests with coverage"
	@echo "  make lint             # Run linters"
	@echo ""
	@echo "Database:"
	@echo "  make migrate          # Run all migrations"
	@echo "  make migrate-user     # Migrate User Service"
	@echo "  make migrate-tournament # Migrate Tournament Service"
	@echo "  make migrate-submission # Migrate Submission Service"
	@echo "  make shell            # Access Django shell"
	@echo "  make db-reset         # Reset database"
	@echo ""
	@echo "Utilities:"
	@echo "  make status           # Check container status"
	@echo "  make restart          # Restart all services"
	@echo "  make clean            # Clean up Docker artifacts"

# Setup Commands
quick-start:
	@bash quick_start.sh

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

status:
	docker-compose ps

# Log Commands
logs:
	docker-compose logs -f

logs-gateway:
	docker-compose logs -f api-gateway

logs-user:
	docker-compose logs -f user-service

logs-tournament:
	docker-compose logs -f tournament-service

logs-submission:
	docker-compose logs -f submission-service

# Test Commands
test:
	@bash run_tests.sh

test-user:
	docker-compose exec -T user-service pytest --cov=apps

test-tournament:
	docker-compose exec -T tournament-service pytest --cov=apps

test-submission:
	docker-compose exec -T submission-service pytest --cov=apps

test-gateway:
	docker-compose exec -T api-gateway pytest --cov=apps

test-cov:
	@cd services/user-service && pytest --cov=apps --cov-report=html
	@cd services/tournament-service && pytest --cov=apps --cov-report=html
	@cd services/submission-service && pytest --cov=apps --cov-report=html
	@cd api-gateway && pytest --cov=apps --cov-report=html
	@echo "Coverage reports generated in htmlcov/"

# Lint Commands
lint:
	cd services/user-service && flake8 apps/
	cd services/tournament-service && flake8 apps/
	cd services/submission-service && flake8 apps/
	cd api-gateway && flake8 apps/

# Database Commands
migrate:
	docker-compose exec -T api-gateway python manage.py migrate
	docker-compose exec -T user-service python manage.py migrate
	docker-compose exec -T tournament-service python manage.py migrate
	docker-compose exec -T submission-service python manage.py migrate

migrate-user:
	docker-compose exec -T user-service python manage.py migrate

migrate-tournament:
	docker-compose exec -T tournament-service python manage.py migrate

migrate-submission:
	docker-compose exec -T submission-service python manage.py migrate

makemigrations:
	docker-compose exec -T user-service python manage.py makemigrations
	docker-compose exec -T tournament-service python manage.py makemigrations
	docker-compose exec -T submission-service python manage.py makemigrations

shell:
	docker-compose exec api-gateway python manage.py shell

db-reset:
	docker-compose down -v
	docker-compose up -d
	$(MAKE) migrate

# Utility Commands
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	docker system prune -f

health:
	@echo "Checking service health..."
	@curl -s http://localhost:8000/health/ | python -m json.tool || echo "API Gateway not responding"
	@curl -s http://localhost:8001/api/auth/health/ | python -m json.tool || echo "User Service not responding"
	@curl -s http://localhost:8003/api/tournaments/health/ | python -m json.tool || echo "Tournament Service not responding"
	@curl -s http://localhost:8002/api/tasks/health/ | python -m json.tool || echo "Submission Service not responding"
