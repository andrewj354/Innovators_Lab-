"""
URL configuration для Tournament Service (головний)
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.tournaments.urls')),
]
