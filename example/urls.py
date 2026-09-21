from django.conf import settings
from django.urls import include, path

from example.views import GroupView, HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("components/<slug:slug>/", GroupView.as_view(), name="group"),
    # The endpoint the browser holds open to hear about a reload.
    path("__reload__/", include("django_browser_reload.urls")),
]

# The component gallery, under DEBUG only. It serves the source of every
# component it indexes, so it is a development tool and never a public route —
# which is also why it is a dev dependency rather than a runtime one. Its own
# routes are all under the /django-cotton-gallery/ prefix, so including it at
# the root adds nothing else.
if settings.DEBUG:
    urlpatterns += [path("", include("django_cotton_gallery.urls"))]

# Django reads these only from the module named by ROOT_URLCONF.
handler400 = "mvp.views.bad_request"
handler403 = "mvp.views.permission_denied"
handler404 = "mvp.views.not_found"
handler500 = "mvp.views.server_error"
