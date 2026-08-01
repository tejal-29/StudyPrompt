from django.urls import path

from .views import (
    GenerateRoadmapView,
    RoadmapListView,
    RoadmapDetailView
)

urlpatterns = [

    path(
        "generate/",
        GenerateRoadmapView.as_view(),
        name="generate-roadmap"
    ),

    path(
        "",
        RoadmapListView.as_view(),
        name="roadmap-list"
    ),

    path(
        "<int:pk>/",
        RoadmapDetailView.as_view(),
        name="roadmap-detail"
    ),

]