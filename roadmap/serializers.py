from rest_framework import serializers

from .models import (
    Roadmap,
    RoadmapPhase,
    Topic,
)


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = "__all__"


class RoadmapPhaseSerializer(serializers.ModelSerializer):

    topics = TopicSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = RoadmapPhase
        fields = "__all__"


class RoadmapSerializer(serializers.ModelSerializer):

    phases = RoadmapPhaseSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Roadmap
        fields = "__all__"