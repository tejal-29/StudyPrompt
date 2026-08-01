from django.db import models
from django.conf import settings


class Analytics(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    total_topics = models.PositiveIntegerField(default=0)

    completed_topics = models.PositiveIntegerField(default=0)

    total_tasks = models.PositiveIntegerField(default=0)

    completed_tasks = models.PositiveIntegerField(default=0)

    total_study_hours = models.FloatField(default=0)

    study_streak = models.PositiveIntegerField(default=0)

    overall_progress = models.FloatField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email