from rest_framework import serializers

from .models import (
    Topic,
    TopicResource,
    TopicQuiz,
)


class TopicResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = TopicResource
        fields = [
            "id",
            "topic",
            "title",
            "url",
            "resource_type",
        ]


class TopicQuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = TopicQuiz
        fields = [
            "id",
            "topic",
            "question",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "answer",
        ]


class TopicSerializer(serializers.ModelSerializer):

    resources = TopicResourceSerializer(
        many=True,
        read_only=True
    )

    quizzes = TopicQuizSerializer(
        many=True,
        read_only=True
    )

    tasks = serializers.SerializerMethodField()

    phase_name = serializers.CharField(
        source="phase.phase_name",
        read_only=True
    )

    class Meta:
        model = Topic

        fields = [
            "id",
            "phase",
            "phase_name",
            "title",
            "description",
            "difficulty",
            "estimated_hours",
            "progress",
            "completed",
            "ai_summary",
            "resources",
            "quizzes",
            "tasks",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "phase_name",
            "resources",
            "quizzes",
            "tasks",
            "created_at",
            "updated_at",
        ]

    def get_tasks(self, obj):

        tasks = obj.tasks.all()

        return [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "status": task.status,
                "estimated_minutes": task.estimated_minutes,
                "scheduled_date": task.scheduled_date,
                "completed": task.completed,
                "completed_at": task.completed_at,
                "total_study_minutes": sum(
                    progress.time_spent
                    for progress in task.daily_progress.all()
                ),
            }
            for task in tasks
        ]

    def validate_phase(self, phase):

        request = self.context.get("request")

        if request and phase.roadmap.user_id != request.user.id:
            raise serializers.ValidationError(
                "You do not have access to this phase."
            )

        return phase