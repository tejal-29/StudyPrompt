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
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_daily_study_hours(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "Daily study hours must be at least 1."
            )

        if value > 24:
            raise serializers.ValidationError(
                "Daily study hours cannot exceed 24."
            )

        return value

    def validate_graduation_year(self, value):
        if value < 2000 or value > 2100:
            raise serializers.ValidationError(
                "Please enter a valid graduation year."
            )

        return value