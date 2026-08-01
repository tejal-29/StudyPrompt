from django.contrib import admin

from .models import (
    Task,
    DailyProgress
)

admin.site.register(Task)
admin.site.register(DailyProgress)