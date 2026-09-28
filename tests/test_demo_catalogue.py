"""The demo shell: a home page, and a page per component the package ships.

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
        assert b'href="/static/css/daisy-cotton-blocks.css"' in response.content

    @pytest.mark.parametrize("url", PAGES)
    def test_the_page_still_loads_its_hosts_stylesheet(self, client, url: str) -> None:
        response = client.get(url)
        assert b'href="/static/css/django-mvp.css"' in response.content

    def test_this_packages_stylesheet_is_linked_after_its_hosts(self, client) -> None:
        content = client.get(reverse("home")).content

        assert content.index(b"css/daisy-cotton-blocks.css") > content.index(
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


class TestHomePage:
    def test_home_renders(self, client) -> None:
        response = client.get(reverse("home"))
        assert response.status_code == 200
