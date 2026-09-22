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
    """The route an open page holds to hear that something on disk changed.

    The middleware that puts the listening script on the page is left out of
    the suite deliberately, so what is asserted here is the half that breaks
    quietly: a route that stops resolving takes the reload with it and looks
    like nothing more than a page that has gone still.
    """

    def test_the_event_stream_is_routed(self) -> None:
        assert reverse("django_browser_reload:events") == "/__reload__/events/"


class TestEveryPageLoadsBothStylesheets:
    """The demo is a host project, and performs a host project's install step.

    django-mvp's build scans django-mvp's own source, so the plain utilities
    used inside this package's templates are absent from it however complete
    that build is. Without this package's own stylesheet on the page a block
    puts its classes in the DOM and no rule matches them, which looks like
    nothing at all rather than like an error.

    Parametrised over every route the demo serves, because the link lives in
    one base template and a page that extends something else bypasses it
    without any sign that it has.
    """

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
        """Both of them, not one in place of the other.

        The host's carries daisyUI, its themes and the page reset. Overriding
        the block that holds it without calling `block.super` would take those
        away and leave a page styled by loose utilities.
        """
        response = client.get(url)
        assert b'href="/static/css/django-mvp.css"' in response.content

    def test_this_packages_stylesheet_is_linked_after_its_hosts(self, client) -> None:
        """Where the two builds overlap on a utility, the later link wins.

        This package's build is the one written against this package's markup,
        so it is the one that should carry a disagreement.
        """
        content = client.get(reverse("home")).content

        assert content.index(b"css/daisy-cotton-blocks.css") > content.index(
            b"css/django-mvp.css"
        )


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
