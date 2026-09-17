from django.urls import path

from example.views import LandingView

urlpatterns = [
    path("", LandingView.as_view(), name="landing"),
]
