"""The demo's sidebar.

Home, the component gallery, then one collapsible section per block family with
a page per component inside it. The family and component entries are built from
the same declaration the pages are routed from, so a component is named in
exactly one place.
"""

from django.conf import settings
from django.urls import reverse_lazy
from flex_menu import MenuItem
from mvp.menus import AppMenu, MenuCollapse, MenuGroup

from example.blocks import FAMILIES

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
            name="content",
            extra_context={"label": "Content"},
            children=[
                # MenuCollapse rather than a nested MenuGroup: it sets the
                # `collapsible` flag the sidebar reads, which renders the family
                # through a <details>/<summary> pair and needs no JavaScript.
                MenuCollapse(
                    name=f"family-{family.slug}",
                    extra_context={"label": family.label, "icon": "block"},
                    children=[
                        MenuItem(
                            name=f"{family.slug}-{component.slug}",
                            url=reverse_lazy(
                                "component",
                                kwargs={
                                    "family": family.slug,
                                    "component": component.slug,
                                },
                            ),
                            extra_context={"label": component.label},
                        )
                        for component in family.components
                    ],
                )
                for family in FAMILIES
            ],
        ),
    ]
)
