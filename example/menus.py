"""The demo's sidebar.

Home first, then one entry per block family the roadmap plans. The family
entries are built from the same declaration the pages are routed from, so a
family is named in exactly one place.
"""

from django.urls import reverse_lazy
from flex_menu import MenuItem
from mvp.menus import AppMenu, MenuGroup

from example.blocks import PLANNED_FAMILIES

AppMenu.extend(
    [
        MenuItem(
            name="home",
            view_name="home",
            extra_context={"label": "Home", "icon": "home"},
        ),
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
