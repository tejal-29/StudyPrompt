from django.db import models
from django.conf import settings


class Goal(models.Model):

    STATUS = [

        ("Not Started", "Not Started"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    PRIORITY = [

        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="goals"
    )

    title = models.CharField(max_length=250)

    description = models.TextField(blank=True)

    target_date = models.DateField()

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY,
        default="Medium"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Not Started"
    )

    estimated_hours = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title