"""The demo's reference tags, which build a page from a component's own comments.

Every block carries `@description`, `@prop` and `@slot` annotations. The tags
under test read those and render them into that component's page, so a prop is
declared in exactly one place — next to the markup it configures — rather than
restated by hand on a page that then drifts from it.

The parsing itself belongs to django-cotton-gallery and is not retested here.
What is tested is the three places this can be wrong: turning a Cotton tag into
a template path, a tag naming a template that does not exist, and a component
carrying no annotations at all.
"""

import pytest
from django.test import override_settings

from example.templatetags.component_docs import template_name

# Demo scaffolding, and deliberately unannotated: it is a component of the
# example project rather than one of the blocks this package documents.
UNANNOTATED = "c-demo.tile"


def docs(render, tag: str) -> str:
    return render(f'{{% load component_docs %}}{{% component_docs "{tag}" %}}')


def description(render, tag: str) -> str:
    return render(f'{{% load component_docs %}}{{% component_description "{tag}" %}}')


class TestTheTemplateAPathIsReadFrom:
    """A Cotton tag names a template, and this is the same rule Cotton uses."""

    @pytest.mark.parametrize(
        "tag", ["c-hero.centred", "<c-hero.centred>", " c-hero.centred "]
    )
    def test_every_spelling_of_a_tag_reaches_one_template(self, tag: str) -> None:
        """The bracketed form because that is how a tag is written everywhere
        else on these pages, and requiring one spelling would be a detail for
        the page author to get wrong."""
        assert template_name(tag) == "cotton/hero/centred.html"

    def test_a_family_becomes_a_directory(self) -> None:
        assert template_name("c-background.image") == "cotton/background/image.html"


class TestTheAttributeAndSlotTables:
    """What a component's page shows about how to configure it."""

    def test_every_attribute_a_block_declares_is_listed(self, render) -> None:
        html = docs(render, "c-hero.centred")

        for attribute in ["eyebrow", "title", "lead", "level", "invert", "size"]:
            assert f">{attribute}</code>" in html

    def test_an_attributes_accepted_values_are_listed(self, render) -> None:
        """A `select` prop is the set of values that block was designed for, so
        the page shows them rather than the word "select"."""
        html = docs(render, "c-hero.centred")

        assert ">sm</code>" in html
        assert ">screen</code>" in html

    def test_an_attributes_default_is_shown(self, render) -> None:
        html = docs(render, "c-hero.centred")

        assert "Default" in html
        assert ">1</code>" in html

    def test_the_slots_are_listed_too(self, render) -> None:
        html = docs(render, "c-hero.centred")

        assert "Slots" in html
        for slot in ["background", "announcement", "actions", "footnote"]:
            assert f">{slot}</code>" in html

    def test_a_block_with_no_slots_gets_no_slots_table(self, render) -> None:
        html = docs(render, "c-background.glow")

        assert "Attributes" in html
        assert "Slots" not in html

    def test_the_panel_links_to_the_gallery_where_it_is_mounted(self, render) -> None:
        html = docs(render, "c-hero.centred")

        assert "component gallery" in html

    def test_the_panel_still_renders_where_the_gallery_is_not_mounted(
        self, render
    ) -> None:
        """The gallery is routed under DEBUG only, so its route is often absent.

        The link is built with the `as` form of the url tag, the form that does
        not raise when a route is missing. A bare reverse would take the whole
        reference panel down everywhere the gallery is not.
        """
        with override_settings(ROOT_URLCONF="tests.urls"):
            html = docs(render, "c-hero.centred")

        assert "Attributes" in html
        assert "component gallery" not in html


class TestAComponentWithNothingToShow:
    """Undocumented should read as undocumented, not as documented and empty."""

    def test_a_component_with_no_annotations_renders_nothing(self, render) -> None:
        assert docs(render, UNANNOTATED).strip() == ""

    def test_a_tag_naming_no_template_renders_nothing(self, render) -> None:
        """Rather than raising. A page is a reference, and a typo in one tag on
        it should cost that panel and not the whole page."""
        assert docs(render, "c-hero.nonexistent").strip() == ""

    def test_a_component_with_no_annotations_has_no_description(self, render) -> None:
        assert description(render, UNANNOTATED).strip() == ""

    def test_a_tag_naming_no_template_has_no_description(self, render) -> None:
        assert description(render, "c-hero.nonexistent").strip() == ""


class TestThePageSummary:
    """The one-line description a page leads with."""

    def test_it_is_the_components_own_description(self, render) -> None:
        html = description(render, "c-hero.centred")

        assert "One column, centred" in html

    def test_it_is_read_from_the_component_rather_than_the_page(self, render) -> None:
        """Two pages describing one component is one source too many, and the
        one that drifts is always the one being read."""
        assert description(render, "c-background.grid").strip()
        assert description(render, "c-background.grid") != description(
            render, "c-background.glow"
        )
