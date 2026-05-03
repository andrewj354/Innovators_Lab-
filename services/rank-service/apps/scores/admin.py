from django.contrib import admin
from .models import JuryAssignment

@admin.register(JuryAssignment)
class JuryAssignmentAdmin(admin.ModelAdmin):
    list_display = ('submission', 'jury_user_id', 'is_evaluated', 'assigned_at')
    list_filter = ('is_evaluated', 'assigned_at')
    search_fields = ('jury_user_id', 'submission__id')