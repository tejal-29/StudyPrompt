from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from goals.models import Goal
from profiles.models import Profile

from .models import Roadmap, RoadmapPhase
from .serializers import RoadmapSerializer
from .services import generate_roadmap
from topics.models import Topic



class GenerateRoadmapView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        goal_id = request.data.get("goal_id")

        try:
            goal = Goal.objects.get(
                id=goal_id,
                user=request.user
            )

        except Goal.DoesNotExist:

            return Response(
                {
                    "error": "Goal not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        profile = Profile.objects.get(
            user=request.user
        )

        roadmap_json = generate_roadmap(
            profile,
            goal
        )

        roadmap = Roadmap.objects.create(

            user=request.user,

            goal=goal,

            title=roadmap_json["roadmap_title"],

            description=roadmap_json["description"],

            total_weeks=roadmap_json["total_weeks"]

        )

        for phase in roadmap_json["phases"]:

            db_phase = RoadmapPhase.objects.create(

                roadmap=roadmap,

                phase_name=phase["phase_name"],

                week_number=phase["week_number"],

                estimated_days=phase["estimated_days"]

            )

            for topic in phase["topics"]:

                Topic.objects.create(

                    phase=db_phase,

                    topic_name=topic["topic_name"],

                    difficulty=topic["difficulty"],

                    estimated_hours=topic["estimated_hours"],

                    resources=topic["resources"]

                )

        serializer = RoadmapSerializer(roadmap)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class RoadmapListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        roadmaps = Roadmap.objects.filter(
            user=request.user
        )

        serializer = RoadmapSerializer(
            roadmaps,
            many=True
        )

        return Response(serializer.data)


class RoadmapDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        roadmap = Roadmap.objects.get(
            id=pk,
            user=request.user
        )

        serializer = RoadmapSerializer(
            roadmap
        )

        return Response(serializer.data)