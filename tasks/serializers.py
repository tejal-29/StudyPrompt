from rest_framework import serializers

from .models import (
    Task,
    DailyProgress
)


class DailyProgressSerializer(serializers.ModelSerializer):

    class Meta:

        model = DailyProgress

        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):

    daily_progress = DailyProgressSerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = Task

        fields = "__all__"