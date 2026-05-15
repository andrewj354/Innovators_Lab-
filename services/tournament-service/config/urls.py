"""
URL configuration для Tournament Service (головний)
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# Проста функція без декораторів rest_framework
def health_check(request):
    return JsonResponse({'status': 'healthy', 'service': 'tournament'}, status=200)

urlpatterns = [
    # ПЕРШИМ РЯДКОМ!
    path('api/tournaments/health/', health_check), 
    
    path('admin/', admin.site.urls),
    path('api/', include('apps.tournaments.urls')),
]