@echo off
REM Script to run tests for all services on Windows

setlocal enabledelayedexpansion

echo =========================================
echo Running Tests for Tournament Platform
echo =========================================
echo.

set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "NC=[0m"

REM Test user-service
echo %YELLOW%Testing User Service...%NC%
cd services\user-service
python -m pytest --cov=apps --cov-report=term-missing -v
if !errorlevel! neq 0 (
    echo %RED%User Service tests failed%NC%
)
cd ..\..
echo.

REM Test tournament-service
echo %YELLOW%Testing Tournament Service...%NC%
cd services\tournament-service
python -m pytest --cov=apps --cov-report=term-missing -v
if !errorlevel! neq 0 (
    echo %RED%Tournament Service tests failed%NC%
)
cd ..\..
echo.

REM Test submission-service
echo %YELLOW%Testing Submission Service...%NC%
cd services\submission-service
python -m pytest --cov=apps --cov-report=term-missing -v
if !errorlevel! neq 0 (
    echo %RED%Submission Service tests failed%NC%
)
cd ..\..
echo.

REM Test api-gateway
echo %YELLOW%Testing API Gateway...%NC%
cd api-gateway
python -m pytest --cov=apps --cov-report=term-missing -v
if !errorlevel! neq 0 (
    echo %RED%API Gateway tests failed%NC%
)
cd ..
echo.

echo %GREEN%=========================================%NC%
echo %GREEN%All tests completed!%NC%
echo %GREEN%=========================================%NC%

endlocal
