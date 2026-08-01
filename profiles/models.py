from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


class Profile(models.Model):

    EXPERIENCE_LEVEL = [

        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    full_name = models.CharField(max_length=200)

    college = models.CharField(max_length=200)

    branch = models.CharField(max_length=150)

    graduation_year = models.IntegerField()

    target_role = models.CharField(max_length=150)

    daily_study_hours = models.PositiveIntegerField()

    experience_level = models.CharField(
        max_length=20,
        choices=EXPERIENCE_LEVEL,
        default="Beginner"
    )

    bio = models.TextField(blank=True)

    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name