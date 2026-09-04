# from django.urls import path

# from .views import (
#     TaskListCreateView,
#     TaskDetailView,
#     DailyProgressListCreateView,
#     DailyProgressDetailView,
# )


# urlpatterns = [

#     # Tasks
#     path(
#         "",
#         TaskListCreateView.as_view(),
#         name="task-list-create",
#     ),

#     path(
#         "<int:pk>/",
#         TaskDetailView.as_view(),
#         name="task-detail",
#     ),

#     # Daily Progress
#     path(
#         "progress/",
#         DailyProgressListCreateView.as_view(),
#         name="daily-progress-list-create",
#     ),

#     path(
#         "progress/<int:pk>/",
#         DailyProgressDetailView.as_view(),
#         name="daily-progress-detail",
#     ),

# ]
from django.urls import path

from .views import (
    TaskListCreateView,
    TaskDetailView,
    DailyProgressListCreateView,
    DailyProgressDetailView,
)

urlpatterns = [
    path(
        "",
        TaskListCreateView.as_view(),
        name="task-list-create"
    ),

    path(
        "<int:pk>/",
        TaskDetailView.as_view(),
        name="task-detail"
    ),

    path(
        "progress/",
        DailyProgressListCreateView.as_view(),
        name="daily-progress-list-create"
    ),

    path(
        "progress/<int:pk>/",
        DailyProgressDetailView.as_view(),
        name="daily-progress-detail"
    ),
]