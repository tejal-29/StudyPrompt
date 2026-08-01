from django.db import models
from django.conf import settings
from goals.models import Goal


class Roadmap(models.Model):

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Completed", "Completed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="roadmaps"
    )

    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="roadmaps")

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    total_weeks = models.PositiveIntegerField(default=0)

    generated_by = models.CharField(max_length=50, default="Gemini")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Active")

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class RoadmapPhase(models.Model):

    roadmap = models.ForeignKey(
        Roadmap,
        on_delete=models.CASCADE,
        related_name="phases"
    )

    phase_name = models.CharField(max_length=255)

    start_week = models.PositiveIntegerField()

    end_week = models.PositiveIntegerField()

    estimated_days = models.PositiveIntegerField()

    phase_objective = models.TextField(blank=True)

    milestone = models.TextField(blank=True)

    def __str__(self):
        return self.phase_name


# class Topic(models.Model):

#     DIFFICULTY = [
#         ("Beginner", "Beginner"),
#         ("Intermediate", "Intermediate"),
#         ("Advanced", "Advanced"),
#     ]

#     phase = models.ForeignKey(
#         RoadmapPhase,
#         on_delete=models.CASCADE,
#         related_name="topics"
#     )

#     topic_name = models.CharField(max_length=255)

#     difficulty = models.CharField(
#         max_length=20,
#         choices=DIFFICULTY,
#         default="Beginner"
#     )

#     estimated_hours = models.PositiveIntegerField(default=0)

#     resources = models.TextField(blank=True)

#     def __str__(self):
#         return self.topic_name
