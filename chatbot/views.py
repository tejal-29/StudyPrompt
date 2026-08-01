from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

        profile = Profile.objects.get(
            user=request.user
        )

        goal = Goal.objects.filter(
            user=request.user
        ).first()

        analytics = AnalyticsService.calculate(
            request.user
        )

        phase = RoadmapPhase.objects.filter(
            roadmap__user=request.user
        ).first()

        history = ChatHistory.objects.filter(
            user=request.user
        )[:5]

        previous = ""

        for chat in history:
            previous += f"User:{chat.user_message}\nAI:{chat.ai_response}\n"

        prompt = CHATBOT_PROMPT.format(

            role=profile.target_role,

            experience=profile.experience_level,

            goal=goal.title if goal else "",

            progress=analytics["progress"],

            phase=phase.phase_name if phase else "",

            history=previous,

            question=question

        )

        answer = ChatbotService.ask(prompt)

        ChatHistory.objects.create(

            user=request.user,

            user_message=question,

            ai_response=answer

        )

        return Response({

            "message": question,

            "response": answer

        })