from django.urls import path

from .views import AskAICoachView

urlpatterns = [

    path(
        "ask/",
        AskAICoachView.as_view(),
        name="ai-coach"
    ),

]