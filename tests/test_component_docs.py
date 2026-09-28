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

UNANNOTATED = "c-unannotated"


def docs(render, tag: str) -> str:
    return render(f'{{% load component_docs %}}{{% component_docs "{tag}" %}}')


def description(render, tag: str) -> str:
    return render(f'{{% load component_docs %}}{{% component_description "{tag}" %}}')


class TestTheTemplateAPathIsReadFrom:
    @pytest.mark.parametrize(
        "tag", ["c-hero.centred", "<c-hero.centred>", " c-hero.centred "]
    )
    def test_every_spelling_of_a_tag_reaches_one_template(self, tag: str) -> None:
        assert template_name(tag) == "cotton/hero/centred.html"

    def test_a_family_becomes_a_directory(self) -> None:
        assert template_name("c-background.image") == "cotton/background/image.html"


class TestTheAttributeAndSlotTables:
    def test_every_attribute_a_block_declares_is_listed(self, render) -> None:
        html = docs(render, "c-hero.centred")

        for attribute in ["eyebrow", "title", "lead", "level", "invert", "size"]:
            assert f">{attribute}</code>" in html

    def test_an_attributes_accepted_values_are_listed(self, render) -> None:
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
        with override_settings(ROOT_URLCONF="tests.urls"):
            html = docs(render, "c-hero.centred")

        assert "Attributes" in html
        assert "component gallery" not in html


class TestAComponentWithNothingToShow:
    def test_a_component_with_no_annotations_renders_nothing(self, render) -> None:
        assert docs(render, UNANNOTATED).strip() == ""

    def test_a_tag_naming_no_template_renders_nothing(self, render) -> None:
        assert docs(render, "c-hero.nonexistent").strip() == ""

    def test_a_component_with_no_annotations_has_no_description(self, render) -> None:
        assert description(render, UNANNOTATED).strip() == ""

    def test_a_tag_naming_no_template_has_no_description(self, render) -> None:
        assert description(render, "c-hero.nonexistent").strip() == ""


class TestThePageSummary:
    def test_it_is_the_components_own_description(self, render) -> None:
        html = description(render, "c-hero.centred")

        assert "One column, centred" in html

    def test_it_is_read_from_the_component_rather_than_the_page(self, render) -> None:
        assert description(render, "c-background.grid").strip()
        assert description(render, "c-background.grid") != description(
            render, "c-background.glow"
        )
