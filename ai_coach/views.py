from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from profiles.models import Profile
from goals.models import Goal

from analytics_app.services import AnalyticsService

from .models import AIConversation
from .services import AICoachService


class AskAICoachView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        question = request.data.get("question")

        profile = Profile.objects.get(user=request.user)

        goal = Goal.objects.filter(user=request.user).first()

        analytics = AnalyticsService.calculate(request.user)

        answer = AICoachService.ask(
            profile,
            goal,
            analytics,
            question
        )

        AIConversation.objects.create(

            user=request.user,

            question=question,

            answer=answer

        )

        return Response({

            "question": question,

            "answer": answer

        })