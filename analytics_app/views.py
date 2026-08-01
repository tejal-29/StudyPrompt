from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import AnalyticsService


class AnalyticsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = AnalyticsService.calculate(
            request.user
        )

        return Response(data)