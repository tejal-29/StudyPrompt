from django.urls import path

from .views import (
    ProfileView,
    CreateProfileView,
)

urlpatterns = [

    path(
        "",
        ProfileView.as_view(),
        name="profile",
    ),

    path(
        "create/",
        CreateProfileView.as_view(),
        name="create-profile",
    ),
]