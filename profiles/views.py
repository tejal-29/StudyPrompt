from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Profile
from .serializers import ProfileSerializer


class ProfileView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def get_object(self):
        return self.get_queryset().get()

class CreateProfileView(generics.CreateAPIView):

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )

