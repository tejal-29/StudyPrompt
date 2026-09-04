from django.utils import timezone
from rest_framework import serializers

from .models import Task, DailyProgress


class DailyProgressSerializer(serializers.ModelSerializer):

    task_title = serializers.CharField(
        source="task.title",
        read_only=True
    )

    topic_title = serializers.CharField(
        source="task.topic.title",
        read_only=True
    )

    study_date = serializers.DateField(
        required=False
    )

    class Meta:

        model = DailyProgress

        fields = [
            "id",
            "task",
            "task_title",
            "topic_title",
            "study_date",
            "time_spent",
            "notes",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "task_title",
            "topic_title",
        ]

    def validate_task(self, task):

        request = self.context.get("request")

        if (
            request
            and task.topic.phase.roadmap.user_id
            != request.user.id
        ):
            raise serializers.ValidationError(
                "You do not have access to this task."
            )

        return task

    def validate_time_spent(self, value):

        if value <= 0:

            raise serializers.ValidationError(
                "Study time must be greater than 0 minutes."
            )

        return value

    def create(self, validated_data):

        if not validated_data.get("study_date"):

            validated_data["study_date"] = (
                timezone.localdate()
            )

        return super().create(validated_data)


class TaskSerializer(serializers.ModelSerializer):

    topic_title = serializers.CharField(
        source="topic.title",
        read_only=True
    )

    phase_name = serializers.CharField(
        source="topic.phase.phase_name",
        read_only=True
    )

    roadmap_id = serializers.IntegerField(
        source="topic.phase.roadmap.id",
        read_only=True
    )

    daily_progress = DailyProgressSerializer(
        many=True,
        read_only=True
    )

    total_study_minutes = serializers.SerializerMethodField()

    class Meta:

        model = Task

        fields = [
            "id",
            "topic",
            "topic_title",
            "phase_name",
            "roadmap_id",
            "title",
            "description",
            "priority",
            "status",
            "estimated_minutes",
            "scheduled_date",
            "completed",
            "completed_at",
            "daily_progress",
            "total_study_minutes",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "completed_at",
            "created_at",
            "updated_at",
            "total_study_minutes",
        ]

    def validate_topic(self, topic):

        request = self.context.get("request")

        if (
            request
            and topic.phase.roadmap.user_id
            != request.user.id
        ):
            raise serializers.ValidationError(
                "You do not have access to this topic."
            )

        return topic

    def get_total_study_minutes(self, obj):

        return sum(
            progress.time_spent
            for progress in obj.daily_progress.all()
        )