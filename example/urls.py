from django.urls import include, path

from example.views import GroupView, HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("components/<slug:slug>/", GroupView.as_view(), name="group"),
    # The endpoint an open page holds to hear that something on disk changed.
    path("__reload__/", include("django_browser_reload.urls")),
]

# Django reads these only from the module named by ROOT_URLCONF.
handler400 = "mvp.views.bad_request"
handler403 = "mvp.views.permission_denied"
handler404 = "mvp.views.not_found"
handler500 = "mvp.views.server_error"
