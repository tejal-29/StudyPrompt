from django.contrib import admin

from .models import (
    Topic,
    TopicQuiz,
    TopicResource
)

admin.site.register(Topic)

admin.site.register(TopicQuiz)

admin.site.register(TopicResource)