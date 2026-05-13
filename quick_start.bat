@echo off
REM Quick start script for Tournament Platform (Windows)

setlocal enabledelayedexpansion

echo =========================================
echo Tournament Platform - Quick Start Setup
echo =========================================
echo.

REM Check Docker
echo Checking requirements...
docker --version >nul 2>&1
if errorlevel 1 (
    echo X Docker not found
    echo Please install Docker from https://www.docker.com
    pause
    exit /b 1
)
echo [OK] Docker found

REM Check Docker Compose
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo X Docker Compose not found
    echo Please install Docker Compose from https://docs.docker.com/compose/install/
    pause
    exit /b 1
)
echo [OK] Docker Compose found

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [OPTIONAL] Python not found
) else (
    echo [OK] Python found
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [OPTIONAL] Node.js not found
) else (
    echo [OK] Node.js found
)

echo.
echo Preparing environment...

REM Create .env if not exists
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo [OK] .env file created
) else (
    echo [OK] .env file already exists
)

echo.
echo Building Docker images...
docker-compose build

echo.
echo Starting services...
docker-compose up -d

echo.
echo Waiting for services to be ready...
timeout /t 10 /nobreak

echo.
echo Running migrations...
docker-compose exec -T api-gateway python manage.py migrate
docker-compose exec -T user-service python manage.py migrate
docker-compose exec -T tournament-service python manage.py migrate
docker-compose exec -T submission-service python manage.py migrate

echo.
echo =========================================
echo [OK] Setup completed successfully!
echo =========================================
echo.

echo Available at:
echo   Frontend:           http://localhost:3000
echo   API Gateway:        http://localhost:8000
echo   User Service:       http://localhost:8001
echo   Task Service:       http://localhost:8002
echo   Tournament Service: http://localhost:8003
echo.

echo Useful commands:
echo   docker-compose logs -f              # View all logs
echo   docker-compose ps                   # Check container status
echo   docker-compose stop                 # Stop all services
echo   docker-compose down -v              # Stop and remove services
echo   run_tests.bat                       # Run tests
echo.

echo Documentation:
echo   Deployment Guide: DEPLOYMENT_GUIDE.md
echo   Testing Guide:    TESTING_GUIDE.md
echo   Architecture:     ARCHITECTURE.md
echo.

pause
