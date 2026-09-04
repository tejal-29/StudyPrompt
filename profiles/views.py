from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Profile
from .serializers import ProfileSerializer


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)

            serializer = ProfileSerializer(profile)

            return Response(
                {
                    "exists": True,
                    "profile": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Profile.DoesNotExist:
            return Response(
                {
                    "exists": False,
                    "profile": None,
                    "message": "Profile not created yet.",
                },
                status=status.HTTP_200_OK,
            )

    def post(self, request):
        try:
            # Prevent duplicate profiles
            if Profile.objects.filter(user=request.user).exists():
                return Response(
                    {
                        "error": "Profile already exists."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = ProfileSerializer(data=request.data)

            if serializer.is_valid():
                profile = serializer.save(user=request.user)

                return Response(
                    {
                        "message": "Profile created successfully.",
                        "profile": ProfileSerializer(profile).data,
                    },
                    status=status.HTTP_201_CREATED,
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            print("PROFILE CREATE ERROR:", str(e))

            return Response(
                {
                    "error": "Failed to create profile.",
                    "details": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request):
        try:
            profile = Profile.objects.get(user=request.user)

        except Profile.DoesNotExist:
            return Response(
                {
                    "error": "Profile not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ProfileSerializer(
            profile,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            profile = serializer.save()

            return Response(
                {
                    "message": "Profile updated successfully.",
                    "profile": ProfileSerializer(profile).data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )