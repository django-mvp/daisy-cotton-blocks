"""URL routes for the example project."""

from django.conf import settings
from django.urls import include, path

from example.views import ComponentView, HomeView, PreviewView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "components/<slug:family>/<slug:component>/",
        ComponentView.as_view(),
        name="component",
    ),
    path(
        "components/<slug:family>/<slug:component>/preview/",
        PreviewView.as_view(),
        name="preview",
    ),
    path("__reload__/", include("django_browser_reload.urls")),
]

# Under DEBUG only: the gallery serves the source of every component it indexes.
if settings.DEBUG:
    urlpatterns += [path("", include("django_cotton_gallery.urls"))]

# Django reads these only from the module named by ROOT_URLCONF.
handler400 = "mvp.views.bad_request"
handler403 = "mvp.views.permission_denied"
handler404 = "mvp.views.not_found"
handler500 = "mvp.views.server_error"
