# pytest configuration for all services

import os
import sys
import django
from django.conf import settings

# Add the service to the path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def pytest_configure():
    """Configure pytest for Django"""
    if not settings.configured:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        django.setup()

# Pytest markers
def pytest_configure_markers():
    """Define pytest markers"""
    return [
        "django_db: mark test as requiring database",
        "integration: mark test as integration test",
        "unit: mark test as unit test",
    ]
