from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Task, DailyProgress
from .serializers import TaskSerializer, DailyProgressSerializer


# =========================================================
# TASK LIST + CREATE
# =========================================================

class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = (
            Task.objects
            .filter(
                topic__phase__roadmap__user=request.user
            )
            .select_related(
                "topic",
                "topic__phase",
                "topic__phase__roadmap",
            )
            .prefetch_related(
                "daily_progress"
            )
            .order_by(
                "scheduled_date",
                "-created_at"
            )
        )

        serializer = TaskSerializer(
            tasks,
            many=True,
            context={"request": request},
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = TaskSerializer(
            data=request.data,
            context={"request": request},
        )

        if serializer.is_valid():
            task = serializer.save()

            return Response(
                TaskSerializer(
                    task,
                    context={"request": request},
                ).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


# =========================================================
# TASK DETAIL
# =========================================================

class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            task = (
                Task.objects
                .select_related(
                    "topic",
                    "topic__phase",
                    "topic__phase__roadmap",
                )
                .prefetch_related(
                    "daily_progress"
                )
                .get(
                    id=pk,
                    topic__phase__roadmap__user=request.user,
                )
            )

        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TaskSerializer(
            task,
            context={"request": request},
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def patch(self, request, pk):
        try:
            task = Task.objects.get(
                id=pk,
                topic__phase__roadmap__user=request.user,
            )

        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TaskSerializer(
            task,
            data=request.data,
            partial=True,
            context={"request": request},
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        task = serializer.save()

        # -------------------------------------------------
        # Automatically keep status + completed_at in sync
        # -------------------------------------------------

        if "completed" in request.data:

            if task.completed:
                task.status = "Completed"
                task.completed_at = timezone.now()

            else:
                task.status = "Pending"
                task.completed_at = None

            task.save(
                update_fields=[
                    "status",
                    "completed_at",
                    "updated_at",
                ]
            )

        return Response(
            TaskSerializer(
                task,
                context={"request": request},
            ).data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        try:
            task = Task.objects.get(
                id=pk,
                topic__phase__roadmap__user=request.user,
            )

        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        task.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


# =========================================================
# DAILY PROGRESS LIST + CREATE
# =========================================================

class DailyProgressListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    # -----------------------------------------------------
    # GET /tasks/progress/
    # -----------------------------------------------------

    def get(self, request):

        progress = (
            DailyProgress.objects
            .filter(
                task__topic__phase__roadmap__user=request.user
            )
            .select_related(
                "task",
                "task__topic",
                "task__topic__phase",
                "task__topic__phase__roadmap",
            )
            .order_by(
                "-study_date",
                "-created_at",
            )
        )

        serializer = DailyProgressSerializer(
            progress,
            many=True,
            context={"request": request},
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    # -----------------------------------------------------
    # POST /tasks/progress/
    # -----------------------------------------------------

    def post(self, request):

        serializer = DailyProgressSerializer(
            data=request.data,
            context={"request": request},
        )

        if serializer.is_valid():

            progress = serializer.save()

            return Response(
                DailyProgressSerializer(
                    progress,
                    context={"request": request},
                ).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


# =========================================================
# DAILY PROGRESS DETAIL
# =========================================================

class DailyProgressDetailView(APIView):
    permission_classes = [IsAuthenticated]

    # -----------------------------------------------------
    # Helper: get only user's own progress
    # -----------------------------------------------------

    def get_object(self, request, pk):

        try:
            return (
                DailyProgress.objects
                .select_related(
                    "task",
                    "task__topic",
                    "task__topic__phase",
                    "task__topic__phase__roadmap",
                )
                .get(
                    id=pk,
                    task__topic__phase__roadmap__user=request.user,
                )
            )

        except DailyProgress.DoesNotExist:
            return None

    # -----------------------------------------------------
    # GET /tasks/progress/<id>/
    # -----------------------------------------------------

    def get(self, request, pk):

        progress = self.get_object(
            request,
            pk,
        )

        if not progress:
            return Response(
                {"error": "Progress entry not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = DailyProgressSerializer(
            progress,
            context={"request": request},
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    # -----------------------------------------------------
    # PATCH /tasks/progress/<id>/
    # -----------------------------------------------------

    def patch(self, request, pk):

        progress = self.get_object(
            request,
            pk,
        )

        if not progress:
            return Response(
                {"error": "Progress entry not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = DailyProgressSerializer(
            progress,
            data=request.data,
            partial=True,
            context={"request": request},
        )

        if serializer.is_valid():

            progress = serializer.save()

            return Response(
                DailyProgressSerializer(
                    progress,
                    context={"request": request},
                ).data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    # -----------------------------------------------------
    # DELETE /tasks/progress/<id>/
    # -----------------------------------------------------

    def delete(self, request, pk):

        progress = self.get_object(
            request,
            pk,
        )

        if not progress:
            return Response(
                {"error": "Progress entry not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        progress.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )