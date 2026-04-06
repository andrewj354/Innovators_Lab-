from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'tournament', 'status', 'start_time', 'deadline')
    list_filter = ('status', 'tournament')
    search_fields = ('title', 'description')
    date_hierarchy = 'start_time'