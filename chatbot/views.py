from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from profiles.models import Profile
from goals.models import Goal
from roadmap.models import RoadmapPhase
from analytics_app.services import AnalyticsService

from .models import ChatHistory
from .prompts import CHATBOT_PROMPT
from .services import ChatbotService


class ChatbotAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        question = request.data.get("message")

        # Validate message
        if not question or not str(question).strip():
            return Response(
                {
                    "error": "Message is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        question = str(question).strip()

        # Get user profile
        try:
            profile = Profile.objects.get(
                user=request.user
            )
        except Profile.DoesNotExist:
            return Response(
                {
                    "error": "User profile not found."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get user's goal
        goal = Goal.objects.filter(
            user=request.user
        ).first()

        # Get analytics
        analytics = AnalyticsService.calculate(
            request.user
        )

        # Get roadmap phase
        phase = RoadmapPhase.objects.filter(
            roadmap__user=request.user
        ).first()

        # Get previous conversations
        history = ChatHistory.objects.filter(
            user=request.user
        ).order_by("-created_at")[:5]

        previous = ""

        for chat in reversed(history):
            previous += (
                f"User: {chat.user_message}\n"
                f"AI: {chat.ai_response}\n"
            )

        # Build prompt
        prompt = CHATBOT_PROMPT.format(
            role=profile.target_role,
            experience=profile.experience_level,
            goal=goal.title if goal else "",
            progress=analytics.get("progress", 0),
            phase=phase.phase_name if phase else "",
            history=previous,
            question=question
        )

        # Get AI response
        answer = ChatbotService.ask(prompt)

        # Save conversation
        ChatHistory.objects.create(
            user=request.user,
            user_message=question,
            ai_response=answer
        )

        return Response(
            {
                "message": question,
                "response": answer
            },
            status=status.HTTP_200_OK
        )