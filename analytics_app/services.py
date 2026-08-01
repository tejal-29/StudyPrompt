from topics.models import Topic
from tasks.models import Task, DailyProgress


class AnalyticsService:

    @staticmethod
    def calculate(user):

        topics = Topic.objects.filter(
            phase__roadmap__user=user
        )

        tasks = Task.objects.filter(
            topic__phase__roadmap__user=user
        )

        total_topics = topics.count()

        completed_topics = topics.filter(
            completed=True
        ).count()

        total_tasks = tasks.count()

        completed_tasks = tasks.filter(
            completed=True
        ).count()

        total_minutes = sum(

            DailyProgress.objects.filter(
                task__topic__phase__roadmap__user=user
            ).values_list(
                "time_spent",
                flat=True
            )

        )

        hours = total_minutes / 60

        if total_tasks == 0:

            progress = 0

        else:

            progress = round(
                completed_tasks * 100 / total_tasks,
                2
            )

        return {

            "total_topics": total_topics,

            "completed_topics": completed_topics,

            "total_tasks": total_tasks,

            "completed_tasks": completed_tasks,

            "study_hours": hours,

            "progress": progress,

        }