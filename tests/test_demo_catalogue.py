"""The demo shell: a home page and a placeholder page per planned block family.

There is nothing to discover yet. The package ships no blocks, so these tests
hold the two things that exist: the home page, and the family pages the
roadmap plans, each of which carries no template of its own and renders
django-mvp's packaged placeholder.
"""

import pytest
from django.urls import reverse

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


class TestHomePage:
    """The page somebody arriving at the demo cold lands on."""

    def test_home_renders(self, client) -> None:
        response = client.get(reverse("home"))
        assert response.status_code == 200

    def test_home_explains_what_the_package_is(self, client) -> None:
        response = client.get(reverse("home"))
        assert b"What this is" in response.content
        assert b"django-cotton" in response.content
