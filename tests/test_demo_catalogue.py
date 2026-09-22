"""The demo shell: a home page, and a page per component the package ships.

The catalogue in ``example.blocks`` is the single declaration the sidebar, the
URLconf and these tests all read, so the failure worth guarding against is a
component named in one of them and missing from another.
"""

import pytest
from django.urls import reverse

from example import blocks


class TestComponentPages:
    """A page per component, built from the same declaration as the sidebar."""

    @pytest.mark.parametrize(("family", "component"), blocks.every_component())
    def test_every_component_has_a_reachable_page(
        self, client, family: blocks.Family, component: blocks.Component
    ) -> None:
        """Parametrised so declaring a component without a page fails here.

        The sidebar and the URLconf are both built from the catalogue, so the
        drift this catches shows up as a sidebar entry leading to a 404, or a
        route with no template behind it.
        """
        response = client.get(
            reverse(
                "component",
                kwargs={"family": family.slug, "component": component.slug},
            )
        )

        assert response.status_code == 200
        assert component.tag(family.slug).encode() in response.content

    def test_a_component_page_renders_its_block(self, client) -> None:
        """Asserting rendered output, not the presence of a tag name.

        A page that failed to compile its Cotton tags would still contain the
        tag text in its own code sample, so the check has to be something only
        a rendered block produces.
        """
        response = client.get(
            reverse("component", kwargs={"family": "hero", "component": "centred"})
        )

        assert b"Ship the page, not the CSS" in response.content
        assert b"relative isolate overflow-hidden" in response.content

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


class TestCatalogue:
    """What the sidebar and the URLconf are both built from."""

    def test_only_families_with_blocks_are_declared(self) -> None:
        """The placeholder pages are gone, and stay gone.

        A family without blocks used to hold a page that said so. Nothing is
        served by a sidebar full of entries leading to that message, so a
        family arrives here when it has something to show.
        """
        assert [family.slug for family in blocks.FAMILIES] == ["hero", "background"]

    def test_every_component_names_its_cotton_tag(self) -> None:
        assert blocks.FAMILIES[0].components[0].tag("hero") == "c-hero.centred"

    def test_an_unknown_slug_resolves_to_nothing(self) -> None:
        assert blocks.find("hero", "nonexistent") is None
        assert blocks.find("nonexistent", "centred") is None


class TestHomePage:
    """The page somebody arriving at the demo cold lands on."""

    def test_home_renders(self, client) -> None:
        response = client.get(reverse("home"))
        assert response.status_code == 200

    def test_home_explains_what_the_package_is(self, client) -> None:
        response = client.get(reverse("home"))
        assert b"What this is" in response.content
        assert b"django-cotton" in response.content
