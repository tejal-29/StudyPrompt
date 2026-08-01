from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Topic
from .serializers import TopicSerializer


class TopicListCreateView(generics.ListCreateAPIView):

    serializer_class = TopicSerializer

    permission_classes = [IsAuthenticated]

    queryset = Topic.objects.all()


class TopicDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = TopicSerializer

    permission_classes = [IsAuthenticated]

    queryset = Topic.objects.all()