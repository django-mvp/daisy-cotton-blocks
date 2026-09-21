"""The demo's sidebar.

Home first, then the component gallery, then one entry per block family. The
family entries are built from the same declaration the pages are routed from,
so a family is named in exactly one place.
"""

from django.conf import settings
from django.urls import reverse_lazy
from flex_menu import MenuItem
from mvp.menus import AppMenu, MenuGroup

from example.blocks import PLANNED_FAMILIES

# The gallery is routed under DEBUG only, so reversing its URL raises outside
# development. The entry is built on the same condition rather than guarded at
# render time, because a sidebar link to a route that does not exist is a 500
# waiting for somebody to click it.
gallery_entries = (
    [
        MenuItem(
            name="gallery",
            url=reverse_lazy("django_cotton_gallery:index"),
            extra_context={"label": "Component gallery", "icon": "gallery"},
        )
    ]
    if settings.DEBUG
    else []
)

AppMenu.extend(
    [
        MenuItem(
            name="home",
            view_name="home",
            extra_context={"label": "Home", "icon": "home"},
        ),
        *gallery_entries,
        MenuGroup(
            name="families",
            extra_context={"label": "Block families"},
            children=[
                MenuItem(
                    name=f"family-{slug}",
                    url=reverse_lazy("group", kwargs={"slug": slug}),
                    extra_context={"label": label, "icon": "block"},
                )
                for slug, label in PLANNED_FAMILIES
            ],
        ),
    ]
)
