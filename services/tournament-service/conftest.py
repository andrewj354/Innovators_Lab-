# pytest configuration

import os
import sys
import django
from django.conf import settings

def pytest_configure():
    """Configure pytest for Django"""
    if not settings.configured:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        django.setup()
