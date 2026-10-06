"""The demo: a front page, and a page per component the package ships.

The catalogue in ``example.blocks`` is the single declaration the sidebar, the
URLconf and these tests all read, so the failure worth guarding against is a
component named in one of them and missing from another.
"""

import re

import pytest
from django.urls import reverse, reverse_lazy

from example import blocks


class TestComponentPages:
    @pytest.mark.parametrize(("family", "component"), blocks.every_component())
    def test_every_component_has_a_reachable_page(
        self, client, family: blocks.Family, component: blocks.Component
    ) -> None:
        response = client.get(
            reverse(
                "component",
                kwargs={"family": family.slug, "component": component.slug},
            )
        )

        assert response.status_code == 200
        assert component.tag(family.slug).encode() in response.content

    def test_a_component_page_renders_its_block(self, client) -> None:
        response = client.get(
            reverse("component", kwargs={"family": "hero", "component": "centred"})
        )
        html = response.content.decode()

        assert re.search(r"<h2[^>]*>\s*Ship the page, not the CSS", html) is not None

    def test_an_unknown_component_is_not_found(self, client) -> None:
        response = client.get(
            reverse("component", kwargs={"family": "hero", "component": "nonexistent"})
        )
        assert response.status_code == 404

    def test_an_unknown_family_is_not_found(self, client) -> None:
        response = client.get(
            reverse(
                "component", kwargs={"family": "nonexistent", "component": "centred"}
            )
        )
        assert response.status_code == 404


class TestTheBrowserReloadEndpoint:
    def test_the_event_stream_is_routed(self) -> None:
        assert reverse("django_browser_reload:events") == "/__reload__/events/"


class TestEveryPageLoadsBothStylesheets:
    PAGES = [reverse_lazy("home")] + [
        reverse_lazy(
            "component",
            kwargs={"family": family.slug, "component": component.slug},
        )
        for family, component in blocks.every_component()
    ]

    @pytest.mark.parametrize("url", PAGES)
    def test_the_page_loads_this_packages_stylesheet(self, client, url: str) -> None:
        response = client.get(url)
        assert b'href="/static/css/daisy-cotton-ext.css"' in response.content

    @pytest.mark.parametrize("url", PAGES)
    def test_the_page_still_loads_its_hosts_stylesheet(self, client, url: str) -> None:
        response = client.get(url)
        assert b'href="/static/css/django-mvp.css"' in response.content

    def test_this_packages_stylesheet_is_linked_after_its_hosts(self, client) -> None:
        content = client.get(reverse("home")).content

        assert content.index(b"css/daisy-cotton-ext.css") > content.index(
            b"css/django-mvp.css"
        )


class TestCatalogue:
    def test_every_declared_family_has_at_least_one_component(self) -> None:
        assert all(family.components for family in blocks.FAMILIES)

    def test_every_component_names_its_cotton_tag(self) -> None:
        assert blocks.FAMILIES[0].components[0].tag("hero") == "c-hero.centred"

    def test_an_unknown_slug_resolves_to_nothing(self) -> None:
        assert blocks.find("hero", "nonexistent") is None
        assert blocks.find("nonexistent", "centred") is None


# Every state of every whole-page block, as (family, component, state).
PREVIEWS = [
    (family, component, state)
    for family, component in blocks.every_component()
    if family.page
    for state, label in component.states
]


class TestPreviews:
    @pytest.mark.parametrize(("family", "component", "state"), PREVIEWS)
    def test_every_state_of_a_whole_page_block_has_a_page_of_its_own(
        self, client, family: blocks.Family, component: blocks.Component, state: str
    ) -> None:
        response = client.get(preview_url(family, component), {"state": state})

        assert response.status_code == 200

    @pytest.mark.parametrize(("family", "component", "state"), PREVIEWS)
    def test_a_preview_has_no_demo_shell_around_it(
        self, client, family: blocks.Family, component: blocks.Component, state: str
    ) -> None:
        html = client.get(preview_url(family, component), {"state": state}).content

        assert re.search(rb"<body[^>]*>\s*<section\b", html) is not None

    @pytest.mark.parametrize(("family", "component", "state"), PREVIEWS)
    def test_a_preview_page_has_one_first_level_heading(
        self, client, family: blocks.Family, component: blocks.Component, state: str
    ) -> None:
        html = client.get(preview_url(family, component), {"state": state}).content

        assert len(re.findall(rb"<h1\b", html)) == 1

    @pytest.mark.parametrize(("family", "component", "state"), PREVIEWS)
    def test_every_field_on_a_preview_has_a_label(
        self, client, family: blocks.Family, component: blocks.Component, state: str
    ) -> None:
        html = client.get(preview_url(family, component), {"state": state}).content
        fields = set(re.findall(rb'<input[^>]*?\bid="([^"]+)"', html, re.DOTALL))
        labelled = set(re.findall(rb'<label[^>]*\bfor="([^"]+)"', html))

        assert fields <= labelled

    def test_a_preview_can_be_framed_by_its_own_demo_page(self, client) -> None:
        family, component = blocks.find("sign-in", "centred")

        response = client.get(preview_url(family, component))

        assert response.headers["X-Frame-Options"] == "SAMEORIGIN"

    def test_an_unknown_state_shows_the_first(self, client) -> None:
        family, component = blocks.find("sign-in", "stepped")

        response = client.get(preview_url(family, component), {"state": "nonsense"})

        assert response.context["state"] == component.states[0][0]

    def test_posting_the_stand_in_form_shows_the_state_it_names(self, client) -> None:
        family, component = blocks.find("sign-in", "centred")

        response = client.post(preview_url(family, component) + "?state=errors")

        assert response.status_code == 200
        assert response.context["state"] == "errors"
        assert b'role="alert"' in response.content

    def test_a_block_that_is_not_a_whole_page_has_no_preview(self, client) -> None:
        response = client.get(
            reverse("preview", kwargs={"family": "hero", "component": "centred"})
        )

        assert response.status_code == 404

    def test_an_unknown_component_has_no_preview(self, client) -> None:
        response = client.get(
            reverse("preview", kwargs={"family": "sign-in", "component": "nonexistent"})
        )

        assert response.status_code == 404

    def test_the_demo_page_frames_each_state(self, client) -> None:
        family, component = blocks.find("sign-up", "stepped")

        html = client.get(
            reverse(
                "component",
                kwargs={"family": family.slug, "component": component.slug},
            )
        ).content.decode()

        states = [state for state, label in component.states]
        for state in states:
            assert f'{preview_url(family, component)}?state={state}"' in html

    def test_the_demo_page_shows_the_markup_that_drew_the_previews(
        self, client
    ) -> None:
        html = client.get(
            reverse("component", kwargs={"family": "sign-in", "component": "centred"})
        ).content

        assert b"&lt;c-sign-in.centred" in html


def component_url(family: blocks.Family, component: blocks.Component) -> str:
    """Return the address of a component's demo page."""
    return reverse(
        "component", kwargs={"family": family.slug, "component": component.slug}
    )


def preview_url(family: blocks.Family, component: blocks.Component) -> str:
    """Return the address of a whole-page block's bare preview."""
    return reverse(
        "preview", kwargs={"family": family.slug, "component": component.slug}
    )


class TestSidebarSections:
    def test_every_component_is_listed_in_exactly_one_section(self) -> None:
        kinds = [kind for kind, label in blocks.SECTIONS]

        for family, component in blocks.every_component():
            assert family.kind_of(component) in kinds

    def test_a_component_takes_its_familys_section_unless_it_names_one(self) -> None:
        family = blocks.Family(
            slug="mixed",
            label="Mixed",
            components=(
                blocks.Component("piece", "Piece"),
                blocks.Component("region", "Region", kind="block"),
            ),
        )

        assert family.kind_of(family.components[0]) == "component"
        assert family.kind_of(family.components[1]) == "block"

    def test_a_family_of_both_kinds_gives_each_section_its_own_half(self) -> None:
        family = blocks.Family(
            slug="mixed",
            label="Mixed",
            components=(
                blocks.Component("piece", "Piece", group="Pieces"),
                blocks.Component("region", "Region", group="Regions", kind="block"),
            ),
        )

        assert family.groups("component") == [("Pieces", [family.components[0]])]
        assert family.groups("block") == [("Regions", [family.components[1]])]
        assert len(family.groups()) == 2

    def test_a_family_with_nothing_of_a_kind_is_left_out_of_that_section(
        self,
    ) -> None:
        family, component = blocks.find("hero", "centred")

        assert family.groups("component") == []

    @pytest.mark.parametrize(("kind", "label"), blocks.SECTIONS)
    def test_the_sidebar_names_each_section(self, client, kind, label) -> None:
        html = client.get(component_url(*blocks.every_component()[0])).content.decode()
        sidebar = html[html.index("<aside") : html.index("</aside>")]

        assert re.search(rf">\s*{label}\s*<", sidebar) is not None

    def test_a_component_with_a_tag_of_its_own_is_documented_under_it(self) -> None:
        family, component = blocks.find("parts", "panel")

        assert component.tag(family.slug) == "c-auth.panel"


class TestFrontPage:
    def test_it_renders(self, client) -> None:
        response = client.get(reverse("home"))

        assert response.status_code == 200

    def test_it_has_no_demo_shell_around_it(self, client) -> None:
        html = client.get(reverse("home")).content

        assert b"<aside" not in html

    def test_it_has_one_first_level_heading(self, client) -> None:
        html = client.get(reverse("home")).content

        assert len(re.findall(rb"<h1\b", html)) == 1

    @pytest.mark.parametrize(("kind", "label"), blocks.SECTIONS)
    def test_it_links_to_every_family_of_each_kind(self, client, kind, label) -> None:
        html = client.get(reverse("home")).content.decode()

        for family in blocks.FAMILIES:
            groups = family.groups(kind)
            if groups:
                assert f'href="{component_url(family, groups[0][1][0])}"' in html

    def test_it_counts_the_components_the_catalogue_declares(self, client) -> None:
        html = client.get(reverse("home")).content.decode()

        assert f"--count-to: {len(blocks.every_component())}" in html
        assert f"--count-to: {len(blocks.FAMILIES)}" in html

    def test_it_links_to_the_gallery_in_development(self, client, settings) -> None:
        settings.DEBUG = True

        html = client.get(reverse("home")).content.decode()

        assert f'href="{reverse("django_cotton_gallery:index")}"' in html

    def test_it_leaves_the_gallery_out_elsewhere(self, client, settings) -> None:
        settings.DEBUG = False

        html = client.get(reverse("home")).content.decode()

        assert f'href="{reverse("django_cotton_gallery:index")}"' not in html
