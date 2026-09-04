from datetime import timedelta

from django.db.models import Sum
from django.utils import timezone

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from goals.models import Goal
from roadmap.models import Roadmap
from tasks.models import Task, DailyProgress


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        today = timezone.localdate()

        # ==================================================
        # 1. USER GOALS
        # ==================================================

        user_goals = Goal.objects.filter(user=user)

        active_goals = user_goals.exclude(
            status="Completed"
        ).count()

        active_goal = (
            user_goals
            .exclude(status="Completed")
            .order_by("target_date")
            .first()
        )

        # ==================================================
        # 2. ACTIVE ROADMAP
        # ==================================================

        active_roadmap = (
            Roadmap.objects
            .filter(
                user=user,
                status="Active"
            )
            .select_related("goal")
            .order_by("-created_at")
            .first()
        )

        # ==================================================
        # 3. TASKS BELONGING TO ACTIVE ROADMAP
        #
        # Roadmap
        #    ↓
        # RoadmapPhase
        #    ↓
        # Topic
        #    ↓
        # Task
        # ==================================================

        if active_roadmap:

            roadmap_tasks = (
                Task.objects
                .filter(
                    topic__phase__roadmap=active_roadmap
                )
                .select_related(
                    "topic",
                    "topic__phase"
                )
                .order_by(
                    "completed",
                    "created_at"
                )
            )

        else:

            roadmap_tasks = Task.objects.none()

        # ==================================================
        # 4. TASK STATISTICS
        # ==================================================

        total_tasks = roadmap_tasks.count()

        completed_tasks = roadmap_tasks.filter(
            completed=True
        ).count()

        # For dashboard "Today's Tasks"
        #
        # Your Task model currently DOES NOT have a
        # due_date/study_date field.
        #
        # Therefore we cannot technically know which
        # tasks are scheduled for today.
        #
        # For now we show all roadmap tasks.

        tasks_today = total_tasks

        # ==================================================
        # 5. TASK PROGRESS
        # ==================================================

        if total_tasks > 0:

            roadmap_progress = round(
                (completed_tasks / total_tasks) * 100
            )

        else:

            roadmap_progress = 0

        # ==================================================
        # 6. TODAY'S TASK LIST
        # ==================================================

        today_tasks = []

        for task in roadmap_tasks[:5]:

            today_tasks.append(
                {
                    "id": task.id,
                    "title": task.title,
                    "completed": task.completed,
                    "duration_minutes": task.estimated_minutes,
                }
            )

        # ==================================================
        # 7. STUDY TIME
        # ==================================================

        if active_roadmap:

            study_minutes = (
                DailyProgress.objects
                .filter(
                    task__topic__phase__roadmap=active_roadmap
                )
                .aggregate(
                    total=Sum("time_spent")
                )["total"]
                or 0
            )

        else:

            study_minutes = 0

        # ==================================================
        # 8. STUDY STREAK
        # ==================================================

        streak = self.calculate_streak(user)

        # ==================================================
        # 9. RECENT ACTIVITY
        # ==================================================

        recent_activity = []

        recent_tasks = (
            roadmap_tasks
            .filter(
                completed=True,
                completed_at__isnull=False
            )
            .order_by("-completed_at")[:5]
        )

        for task in recent_tasks:

            recent_activity.append(
                {
                    "id": task.id,
                    "title": task.title,
                    "description": "Task completed",
                    "created_at": task.completed_at,
                }
            )

        # ==================================================
        # 10. AI INSIGHT
        # ==================================================

        if not active_goal:

            ai_insight = (
                "Create your first goal and let "
                "StudyPrompt build your personalized "
                "learning roadmap."
            )

        elif not active_roadmap:

            ai_insight = (
                "Your goal is ready. Generate a roadmap "
                "to start your personalized learning journey."
            )

        elif total_tasks == 0:

            ai_insight = (
                "Your roadmap does not have any tasks yet. "
                "Continue building your learning plan."
            )

        elif completed_tasks == total_tasks:

            ai_insight = (
                "Excellent work! You completed all "
                "available tasks in your roadmap."
            )

        else:

            remaining = total_tasks - completed_tasks

            ai_insight = (
                f"You have {remaining} task"
                f"{'s' if remaining != 1 else ''} "
                "remaining. Keep going!"
            )

        # ==================================================
        # 11. RESPONSE
        # ==================================================

        return Response(
            {
                "user": {
                    "name": (
                        getattr(user, "first_name", None)
                        or getattr(user, "name", None)
                        or getattr(user, "email", "Learner")
                    )
                },

                "stats": {
                    "active_goals": active_goals,
                    "roadmap_progress": roadmap_progress,
                    "tasks_today": tasks_today,
                    "tasks_completed": completed_tasks,
                    "study_minutes": study_minutes,
                    "streak": streak,
                },

                "active_goal": (
                    {
                        "id": active_goal.id,
                        "title": active_goal.title,
                        "progress": roadmap_progress,
                        "deadline": active_goal.target_date,
                    }
                    if active_goal
                    else None
                ),

                "active_roadmap": (
                    {
                        "id": active_roadmap.id,
                        "title": active_roadmap.title,
                        "status": active_roadmap.status,
                        "total_weeks": active_roadmap.total_weeks,
                    }
                    if active_roadmap
                    else None
                ),

                "today_tasks": today_tasks,

                "recent_activity": recent_activity,

                "ai_insight": ai_insight,
            }
        )

    # ======================================================
    # STUDY STREAK
    # ======================================================

    def calculate_streak(self, user):

        today = timezone.localdate()

        study_dates = set(
            DailyProgress.objects
            .filter(
                task__topic__phase__roadmap__user=user
            )
            .values_list(
                "study_date",
                flat=True
            )
            .distinct()
        )

        if not study_dates:
            return 0

        streak = 0
        current_date = today

        while current_date in study_dates:

            streak += 1

            current_date -= timedelta(days=1)

        return streak