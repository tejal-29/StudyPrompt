# from .models import Topic, TopicResource


# class TopicService:

#     @staticmethod
#     def create_topics(db_phase, topics):

#         for topic_data in topics:

#             topic = Topic.objects.create(
#                 phase=db_phase,

#                 # Support both old and new JSON
#                 title=topic_data.get(
#                     "title",
#                     topic_data.get("topic_name", "")
#                 ),

#                 description=topic_data.get(
#                     "description",
#                     ""
#                 ),

#                 difficulty=topic_data.get(
#                     "difficulty",
#                     "Beginner"
#                 ),

#                 estimated_hours=topic_data.get(
#                     "estimated_hours",
#                     1
#                 ),
#             )

#             resources = topic_data.get("resources", [])

#             if not isinstance(resources, list):
#                 resources = []

#             for resource in resources:

#                 # If Gemini returned only a URL
#                 if isinstance(resource, str):

#                     TopicResource.objects.create(
#                         topic=topic,
#                         title="Learning Resource",
#                         url=resource,
#                         resource_type="Article",
#                     )

#                 # If Gemini returned an object
#                 elif isinstance(resource, dict):

#                     TopicResource.objects.create(
#                         topic=topic,
#                         title=resource.get(
#                             "title",
#                             "Learning Resource"
#                         ),
#                         url=resource.get(
#                             "url",
#                             ""
#                         ),
#                         resource_type=resource.get(
#                             "resource_type",
#                             "Article"
#                         ),
#                     )

from .models import Topic, TopicResource
from tasks.services import TaskService


class TopicService:

    @staticmethod
    def create_topics(db_phase, topics):

        created_topics = []

        for topic_data in topics:

            topic = Topic.objects.create(
                phase=db_phase,

                title=topic_data.get(
                    "title",
                    topic_data.get("topic_name", "")
                ),

                description=topic_data.get(
                    "description",
                    ""
                ),

                difficulty=topic_data.get(
                    "difficulty",
                    "Beginner"
                ),

                estimated_hours=topic_data.get(
                    "estimated_hours",
                    1
                ),
            )

            # -----------------------------------------
            # CREATE TOPIC RESOURCES
            # -----------------------------------------

            resources = topic_data.get(
                "resources",
                []
            )

            if not isinstance(resources, list):
                resources = []

            for resource in resources:

                # Gemini returned only a URL
                if isinstance(resource, str):

                    if resource.strip():

                        TopicResource.objects.create(
                            topic=topic,
                            title="Learning Resource",
                            url=resource,
                            resource_type="Article",
                        )

                # Gemini returned an object
                elif isinstance(resource, dict):

                    url = resource.get(
                        "url",
                        ""
                    )

                    if url:

                        TopicResource.objects.create(
                            topic=topic,
                            title=resource.get(
                                "title",
                                "Learning Resource"
                            ),
                            url=url,
                            resource_type=resource.get(
                                "resource_type",
                                "Article"
                            ),
                        )

            # -----------------------------------------
            # CREATE DEFAULT TASKS
            # -----------------------------------------

            TaskService.create_default_tasks(topic)

            created_topics.append(topic)

        return created_topics