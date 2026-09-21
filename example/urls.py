from django.urls import path

from example.views import GroupView, HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("components/<slug:slug>/", GroupView.as_view(), name="group"),
]

# Django reads these only from the module named by ROOT_URLCONF.
handler400 = "mvp.views.bad_request"
handler403 = "mvp.views.permission_denied"
handler404 = "mvp.views.not_found"
handler500 = "mvp.views.server_error"
