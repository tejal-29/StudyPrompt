from django.db import models
from roadmap.models import RoadmapPhase


class Topic(models.Model):

    LEVELS = [
        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced"),
    ]

    phase = models.ForeignKey(
        RoadmapPhase,
        on_delete=models.CASCADE,
        related_name="topics"
    )

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    difficulty = models.CharField(
        max_length=20,
        choices=LEVELS,
        default="Beginner"
    )

    estimated_hours = models.PositiveIntegerField(default=1)

    progress = models.PositiveIntegerField(default=0)

    completed = models.BooleanField(default=False)

    ai_summary = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title


class TopicResource(models.Model):

    RESOURCE_TYPES = [
        ("Video", "Video"),
        ("Article", "Article"),
        ("Documentation", "Documentation"),
        ("Practice", "Practice"),
    ]

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="resources"
    )

    title = models.CharField(max_length=255)

    url = models.URLField()

    resource_type = models.CharField(
        max_length=30,
        choices=RESOURCE_TYPES,
        default="Article"
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.title} ({self.resource_type})"


class TopicQuiz(models.Model):

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="quizzes"
    )

    question = models.TextField()

    option_a = models.CharField(max_length=255)

    option_b = models.CharField(max_length=255)

    option_c = models.CharField(max_length=255)

    option_d = models.CharField(max_length=255)

    answer = models.CharField(max_length=1)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.question