from django.urls import path

from .views import ChatbotAPIView

urlpatterns = [

    path(
        "message/",
        ChatbotAPIView.as_view(),
        name="chatbot"
    ),

]