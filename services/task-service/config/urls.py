from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/task/', include('apps.tasks.urls')),
    path('api/submissions/',include('apps.tournaments.urls')),

]
