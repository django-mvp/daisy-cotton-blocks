"""The demo shell: a home page and a placeholder page per planned block family.

There is nothing to discover yet. The package ships no blocks, so these tests
hold the two things that exist: the home page, and the family pages the
roadmap plans, each of which carries no template of its own and renders
django-mvp's packaged placeholder.
"""

import pytest
from django.urls import reverse, reverse_lazy

from example import blocks


class TestPlannedFamilyPages:
    """A page per family the roadmap plans, holding its place until it has blocks."""

    @pytest.mark.parametrize(("slug", "label"), blocks.PLANNED_FAMILIES)
    def test_every_planned_family_has_a_reachable_page(
        self, client, slug: str, label: str
    ) -> None:
        """Parametrised so adding a family without routing it fails here.

        The sidebar and the URLconf are both built from PLANNED_FAMILIES, so
        the failure this guards against is the declaration and the routing
        drifting apart — which shows up as a sidebar entry leading to a 404.
        """
        response = client.get(reverse("group", kwargs={"slug": slug}))

        assert response.status_code == 200
        assert label.encode() in response.content

    def test_a_family_page_carries_no_template_of_its_own(self, client) -> None:
        """They render the packaged placeholder, deliberately and visibly.

        Asserting the placeholder rather than the absence of content, because
        "this page has nothing on it" and "this page failed to render" look
        identical from a status code.
        """
        response = client.get(reverse("group", kwargs={"slug": "hero"}))
        assert b"have a template yet" in response.content

    def test_an_unknown_family_is_not_found(self, client) -> None:
        response = client.get(reverse("group", kwargs={"slug": "nonexistent"}))
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
        reverse_lazy("group", kwargs={"slug": slug})
        for slug, _ in blocks.PLANNED_FAMILIES
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


class TestHomePage:
    """The page somebody arriving at the demo cold lands on."""

    def test_home_renders(self, client) -> None:
        response = client.get(reverse("home"))
        assert response.status_code == 200

    def test_home_explains_what_the_package_is(self, client) -> None:
        response = client.get(reverse("home"))
        assert b"What this is" in response.content
        assert b"django-cotton" in response.content
