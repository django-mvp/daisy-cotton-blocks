"""The demo's sidebar.

Home, the component gallery, then a "Components" and a "Sections" section, each
holding one collapsible entry per family with a page per component inside it.
A family with both kinds is listed in both sections, each with its own half. The family and component entries are built from
the same declaration the pages are routed from, so a component is named in
exactly one place.
"""

from django.conf import settings
from django.urls import reverse_lazy
from flex_menu import MenuItem
from mvp.menus import AppMenu, MenuCollapse, MenuGroup

from example.blocks import FAMILIES, SECTIONS, Component, Family


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


def family_entries(family: Family, kind: str, section: str) -> list[MenuItem]:
    """Return a family's entries for one sidebar section.

    Entries sit under a heading per group, unless the section holds only one
    group of the family or the heading would repeat the section's own name.

    Args:
        family: The family whose components are listed.
        kind: The kind of component the section holds.
        section: The section's label, as shown in the sidebar.

    Returns:
        The links, and the headed groups of links, in declaration order.
    """
    groups = family.groups(kind)
    entries: list[MenuItem] = []
    for heading, components in groups:
        links = [component_entry(family, component) for component in components]
        if not heading or heading == section or len(groups) == 1:
            entries.extend(links)
            continue
        entries.append(
            MenuGroup(
                name=f"family-{family.slug}-{kind}-{heading.lower()}",
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
        *[
            MenuGroup(
                name=f"section-{kind}",
                extra_context={"label": label},
                children=[
                    # MenuCollapse rather than a nested MenuGroup: it sets the
                    # `collapsible` flag the sidebar reads, so no JavaScript is needed.
                    MenuCollapse(
                        name=f"family-{family.slug}-{kind}",
                        extra_context={"label": family.label, "icon": kind},
                        children=family_entries(family, kind, label),
                    )
                    for family in FAMILIES
                    if family.groups(kind)
                ],
            )
            for kind, label in SECTIONS
        ],
    ]
)
