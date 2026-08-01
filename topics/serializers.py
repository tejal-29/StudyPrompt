from rest_framework import serializers

from .models import (
    Topic,
    TopicResource,
    TopicQuiz,
)


class TopicResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = TopicResource
        fields = "__all__"


class TopicQuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = TopicQuiz
        fields = "__all__"


class TopicSerializer(serializers.ModelSerializer):

    resources = TopicResourceSerializer(
        many=True,
        read_only=True
    )

    quizzes = TopicQuizSerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = Topic

        fields = "__all__"