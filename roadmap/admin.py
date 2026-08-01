from django.contrib import admin

from .models import (
    Roadmap,
    RoadmapPhase,
    Topic,
)

admin.site.register(Roadmap)
admin.site.register(RoadmapPhase)
admin.site.register(Topic)