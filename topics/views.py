from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Topic
from .serializers import TopicSerializer


class TopicListCreateView(generics.ListCreateAPIView):

    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return (
            Topic.objects
            .filter(
                phase__roadmap__user=self.request.user
            )
            .select_related(
                "phase",
                "phase__roadmap"
            )
            .prefetch_related(
                "resources",
                "quizzes",
                "tasks",
                "tasks__daily_progress"
            )
            .order_by("id")
        )


class TopicDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return (
            Topic.objects
            .filter(
                phase__roadmap__user=self.request.user
            )
            .select_related(
                "phase",
                "phase__roadmap"
            )
            .prefetch_related(
                "resources",
                "quizzes",
                "tasks",
                "tasks__daily_progress"
            )
        )