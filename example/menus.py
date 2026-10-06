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

from example.blocks import FAMILIES, Component, Family


def component_entry(family: Family, component: Component) -> MenuItem:
    """Return the sidebar link to one component's demo page."""
    return MenuItem(
        name=f"{family.slug}-{component.slug}",
        url=reverse_lazy(
            "component",
            kwargs={"family": family.slug, "component": component.slug},
        ),
        extra_context={"label": component.label},
    )


def family_entries(family: Family) -> list[MenuItem]:
    """Return a family's entries, under a heading per group where it has any."""
    entries: list[MenuItem] = []
    for heading, components in family.groups():
        links = [component_entry(family, component) for component in components]
        if not heading:
            entries.extend(links)
            continue
        entries.append(
            MenuGroup(
                name=f"family-{family.slug}-{heading.lower().replace(' ', '-')}",
                extra_context={"label": heading},
                children=links,
            )
        )
    return entries


# The gallery is routed under DEBUG only, so reversing its URL raises elsewhere.
# The entry is built on the same condition, or its link would be a 500.
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
                # `collapsible` flag the sidebar reads, so no JavaScript is needed.
                MenuCollapse(
                    name=f"family-{family.slug}",
                    extra_context={"label": family.label, "icon": "block"},
                    children=family_entries(family),
                )
                for family in FAMILIES
            ],
        ),
    ]
)
