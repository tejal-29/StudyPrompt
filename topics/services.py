from .models import Topic, TopicResource


class TopicService:

    @staticmethod
    def create_topics(db_phase, topics):

        for topic_data in topics:

            topic = Topic.objects.create(
                phase=db_phase,

                # Support both old and new JSON
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

            resources = topic_data.get("resources", [])

            if not isinstance(resources, list):
                resources = []

            for resource in resources:

                # If Gemini returned only a URL
                if isinstance(resource, str):

                    TopicResource.objects.create(
                        topic=topic,
                        title="Learning Resource",
                        url=resource,
                        resource_type="Article",
                    )

                # If Gemini returned an object
                elif isinstance(resource, dict):

                    TopicResource.objects.create(
                        topic=topic,
                        title=resource.get(
                            "title",
                            "Learning Resource"
                        ),
                        url=resource.get(
                            "url",
                            ""
                        ),
                        resource_type=resource.get(
                            "resource_type",
                            "Article"
                        ),
                    )