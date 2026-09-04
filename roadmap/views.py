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
from tasks.models import Task


class GenerateRoadmapView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        # -------------------------------------------------
        # GET GOAL
        # -------------------------------------------------

        goal_id = request.data.get("goal_id")

        if not goal_id:

            return Response(
                {
                    "error": "goal_id is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

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

        # -------------------------------------------------
        # GET PROFILE
        # -------------------------------------------------

        try:

            profile = Profile.objects.get(
                user=request.user
            )

        except Profile.DoesNotExist:

            return Response(
                {
                    "error": "Please create profile first"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -------------------------------------------------
        # GENERATE AI ROADMAP
        # -------------------------------------------------

        try:

            roadmap_json = generate_roadmap(
                profile,
                goal
            )

        except Exception as e:

            print(
                "ROADMAP GENERATION ERROR:",
                str(e)
            )

            return Response(
                {
                    "error": "Failed to generate roadmap",
                    "details": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # -------------------------------------------------
        # CREATE ROADMAP
        # -------------------------------------------------

        try:

            roadmap = Roadmap.objects.create(

                user=request.user,

                goal=goal,

                title=(
                    roadmap_json.get("title")
                    or
                    roadmap_json.get("roadmap_title")
                    or
                    f"Roadmap for {goal.title}"
                ),

                description=roadmap_json.get(
                    "description",
                    ""
                ),

                total_weeks=roadmap_json.get(
                    "total_weeks",
                    1
                ),
            )

            # -------------------------------------------------
            # CREATE PHASES
            # -------------------------------------------------

            phases = roadmap_json.get(
                "phases",
                []
            )

            for phase_index, phase_data in enumerate(
                phases,
                start=1
            ):

                db_phase = RoadmapPhase.objects.create(

                    roadmap=roadmap,

                    phase_name=phase_data.get(
                        "phase_name",
                        f"Phase {phase_index}"
                    ),

                    start_week=phase_data.get(
                        "start_week",
                        1
                    ),

                    end_week=phase_data.get(
                        "end_week",
                        phase_data.get(
                            "start_week",
                            1
                        )
                    ),

                    estimated_days=phase_data.get(
                        "estimated_days",
                        7
                    ),

                    phase_objective=phase_data.get(
                        "phase_objective",
                        ""
                    ),

                    milestone=phase_data.get(
                        "milestone",
                        ""
                    ),
                )

                # -------------------------------------------------
                # CREATE TOPICS + TASKS
                # -------------------------------------------------

                topics = phase_data.get(
                    "topics",
                    []
                )

                for topic_index, topic_data in enumerate(
                    topics,
                    start=1
                ):

                    # -------------------------------
                    # CREATE TOPIC
                    # -------------------------------

                    topic_title = (
                        topic_data.get("title")
                        or
                        topic_data.get("topic_title")
                        or
                        topic_data.get("name")
                        or
                        f"Topic {topic_index}"
                    )

                    topic = Topic.objects.create(

                        phase=db_phase,

                        title=topic_title,

                        description=topic_data.get(
                            "description",
                            ""
                        ),

                        difficulty=(
                            topic_data.get(
                                "difficulty",
                                "Beginner"
                            )
                            if topic_data.get(
                                "difficulty"
                            ) in [
                                "Beginner",
                                "Intermediate",
                                "Advanced",
                            ]
                            else "Beginner"
                        ),

                        estimated_hours=topic_data.get(
                            "estimated_hours",
                            1
                        ),

                        progress=0,

                        completed=False,

                        ai_summary=topic_data.get(
                            "ai_summary",
                            ""
                        ),
                    )

                    # -------------------------------
                    # CREATE TASKS
                    # -------------------------------

                    generated_tasks = topic_data.get(
                        "tasks",
                        []
                    )

                    # If AI provides tasks
                    if generated_tasks:

                        for task_index, task_data in enumerate(
                            generated_tasks,
                            start=1
                        ):

                            if isinstance(
                                task_data,
                                str
                            ):

                                Task.objects.create(

                                    topic=topic,

                                    title=task_data,

                                    description="",

                                    priority="Medium",

                                    status="Pending",

                                    estimated_minutes=30,

                                    completed=False,
                                )

                            else:

                                Task.objects.create(

                                    topic=topic,

                                    title=(
                                        task_data.get(
                                            "title"
                                        )
                                        or
                                        task_data.get(
                                            "task"
                                        )
                                        or
                                        f"Task {task_index}"
                                    ),

                                    description=task_data.get(
                                        "description",
                                        ""
                                    ),

                                    priority=(
                                        task_data.get(
                                            "priority",
                                            "Medium"
                                        )
                                        if task_data.get(
                                            "priority"
                                        ) in [
                                            "Low",
                                            "Medium",
                                            "High",
                                        ]
                                        else "Medium"
                                    ),

                                    status="Pending",

                                    estimated_minutes=(
                                        task_data.get(
                                            "estimated_minutes",
                                            30
                                        )
                                    ),

                                    completed=False,
                                )

                    # -------------------------------
                    # FALLBACK TASKS
                    # -------------------------------

                    else:

                        Task.objects.create(

                            topic=topic,

                            title=(
                                f"Learn {topic.title}"
                            ),

                            description=(
                                f"Study the fundamentals "
                                f"and concepts of "
                                f"{topic.title}."
                            ),

                            priority="Medium",

                            status="Pending",

                            estimated_minutes=30,

                            completed=False,
                        )

                        Task.objects.create(

                            topic=topic,

                            title=(
                                f"Practice {topic.title}"
                            ),

                            description=(
                                f"Practice exercises "
                                f"and problems related "
                                f"to {topic.title}."
                            ),

                            priority="Medium",

                            status="Pending",

                            estimated_minutes=45,

                            completed=False,
                        )

                        Task.objects.create(

                            topic=topic,

                            title=(
                                f"Review {topic.title}"
                            ),

                            description=(
                                f"Review what you learned "
                                f"about {topic.title}."
                            ),

                            priority="Low",

                            status="Pending",

                            estimated_minutes=20,

                            completed=False,
                        )

            # -------------------------------------------------
            # RETURN ROADMAP
            # -------------------------------------------------

            serializer = RoadmapSerializer(
                roadmap
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:

            print(
                "ROADMAP DATABASE ERROR:",
                str(e)
            )

            return Response(
                {
                    "error": "Could not save roadmap",
                    "details": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class RoadmapDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        try:

            roadmap = Roadmap.objects.get(
                id=pk,
                user=request.user
            )

        except Roadmap.DoesNotExist:

            return Response(
                {
                    "error": "Roadmap not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = RoadmapSerializer(
            roadmap
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )