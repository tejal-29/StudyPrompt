from django.db import models
from django.utils import timezone

from topics.models import Topic


class Task(models.Model):

    PRIORITY = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]

    STATUS = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY,
        default="Medium"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending"
    )

    estimated_minutes = models.PositiveIntegerField(
        default=30
    )

    completed = models.BooleanField(
        default=False
    )

    completed_at = models.DateTimeField(
        blank=True,
        null=True
    )

    scheduled_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def mark_completed(self):
        self.completed = True
        self.status = "Completed"
        self.completed_at = timezone.now()

        self.save(
            update_fields=[
                "completed",
                "status",
                "completed_at",
                "updated_at",
            ]
        )

    def mark_incomplete(self):
        self.completed = False
        self.status = "Pending"
        self.completed_at = None

        self.save(
            update_fields=[
                "completed",
                "status",
                "completed_at",
                "updated_at",
            ]
        )

    def __str__(self):
        return self.title


class DailyProgress(models.Model):

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="daily_progress"
    )

    study_date = models.DateField()

    time_spent = models.PositiveIntegerField(
        help_text="Study time in minutes"
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-study_date", "-created_at"]

    def __str__(self):
        return f"{self.task.title} - {self.study_date}"