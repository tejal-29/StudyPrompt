from .models import Task


class TaskService:

    @staticmethod
    def create_default_tasks(topic):
        """
        Create a useful default set of learning tasks
        for a newly created topic.
        """

        tasks = [
            {
                "title": f"Learn {topic.title}",
                "description": (
                    f"Study the fundamentals and core concepts "
                    f"of {topic.title}."
                ),
                "priority": "Medium",
                "estimated_minutes": 60,
            },
            {
                "title": f"Practice {topic.title}",
                "description": (
                    f"Practice exercises and examples related "
                    f"to {topic.title}."
                ),
                "priority": "Medium",
                "estimated_minutes": 45,
            },
            {
                "title": f"Build a small project using {topic.title}",
                "description": (
                    f"Apply what you learned by building a "
                    f"small practical project using {topic.title}."
                ),
                "priority": "High",
                "estimated_minutes": 90,
            },
            {
                "title": f"Revise {topic.title}",
                "description": (
                    f"Review the important concepts, notes, "
                    f"and common mistakes related to {topic.title}."
                ),
                "priority": "Low",
                "estimated_minutes": 30,
            },
        ]

        created_tasks = []

        for task_data in tasks:
            task = Task.objects.create(
                topic=topic,
                title=task_data["title"],
                description=task_data["description"],
                priority=task_data["priority"],
                status="Pending",
                estimated_minutes=task_data["estimated_minutes"],
            )

            created_tasks.append(task)

        return created_tasks