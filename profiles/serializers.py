from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model = Profile

        fields = [
            "id",
            "full_name",
            "college",
            "branch",
            "graduation_year",
            "target_role",
            "daily_study_hours",
            "experience_level",
            "bio",
            "profile_image",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "user",
            "created_at",
            "updated_at",
        )
