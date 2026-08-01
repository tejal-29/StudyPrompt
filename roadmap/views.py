from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from goals.models import Goal
from profiles.models import Profile

from .models import Roadmap, RoadmapPhase
from .serializers import RoadmapSerializer
from .services import generate_roadmap

from topics.services import TopicService


class GenerateRoadmapView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        goal_id = request.data.get("goal_id")

        if not goal_id:

            return Response(
                {"error": "goal_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:

            goal = Goal.objects.get(id=goal_id, user=request.user)

        except Goal.DoesNotExist:

            return Response(
                {"error": "Goal not found"}, status=status.HTTP_404_NOT_FOUND
            )

        try:

            profile = Profile.objects.get(user=request.user)

        except Profile.DoesNotExist:

            return Response(
                {"error": "Please create profile first"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        roadmap_json = generate_roadmap(profile, goal)

        roadmap = Roadmap.objects.create(
            user=request.user,
            goal=goal,
            title=roadmap_json.get("title", roadmap_json.get("roadmap_title")),
            description=roadmap_json["description"],
            total_weeks=roadmap_json["total_weeks"],
        )

        for phase_data in roadmap_json["phases"]:

            db_phase = RoadmapPhase.objects.create(
                roadmap=roadmap,
                phase_name=phase_data["phase_name"],
                start_week=phase_data["start_week"],
                end_week=phase_data["end_week"],
                estimated_days=phase_data["estimated_days"],
                phase_objective=phase_data.get("phase_objective", ""),
                milestone=phase_data.get("milestone", ""),
             
            )

            TopicService.create_topics(db_phase, phase_data["topics"])

        serializer = RoadmapSerializer(roadmap)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoadmapListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        roadmaps = Roadmap.objects.filter(user=request.user)

        serializer = RoadmapSerializer(roadmaps, many=True)

        return Response(serializer.data)


class RoadmapDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        try:

            roadmap = Roadmap.objects.get(id=pk, user=request.user)

        except Roadmap.DoesNotExist:

            return Response(
                {"error": "Roadmap not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = RoadmapSerializer(roadmap)

        return Response(serializer.data)
