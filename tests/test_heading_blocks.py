"""The heading: the short line, the heading itself and the sentence under it."""

import re

import pytest


class TestHeading:
    def test_the_title_is_a_second_level_heading_by_default(self, render) -> None:
        html = render('<c-heading title="In numbers" />')

        assert re.search(r"<h2\b.*In numbers.*</h2>", html, re.S)

    def test_the_heading_level_is_the_page_authors_to_set(self, render) -> None:
        html = render('<c-heading title="In numbers" level="1" />')

        assert re.search(r"<h1\b.*In numbers.*</h1>", html, re.S)
        assert "<h2" not in html

    @pytest.mark.parametrize("size", ["md", "lg", "xl"])
    def test_the_size_never_changes_the_heading_level(self, render, size) -> None:
        html = render(f'<c-heading title="In numbers" size="{size}" />')

        assert re.search(r"<h2\b", html)

    def test_a_title_can_carry_markup(self, render) -> None:
        html = render(
            '<c-heading><c-slot name="title">Ship <em id="word">it</em></c-slot>'
            "</c-heading>"
        )

        assert re.search(r'<h2\b[^>]*>Ship <em id="word">it</em></h2>', html)

    def test_the_three_lines_come_in_reading_order(self, render) -> None:
        html = render('<c-heading eyebrow="Above" title="Middle" lead="Below" />')

        assert html.index("Above") < html.index("Middle") < html.index("Below")

    def test_with_no_title_there_is_no_heading_element(self, render) -> None:
        html = render('<c-heading eyebrow="Above" lead="Below" />')

        assert not re.search(r"<h[1-6]\b", html)
        assert "Above" in html
        assert "Below" in html

    def test_with_nothing_to_say_it_renders_nothing(self, render) -> None:
        html = render("<c-heading />")

        assert html.strip() == ""

    def test_extra_classes_and_attributes_reach_the_wrapper(self, render) -> None:
        html = render('<c-heading title="T" id="intro" class="mb-8" />')

        assert re.match(r'\s*<div[^>]*class="[^"]*\bmb-8\b[^>]*\bid="intro"', html, re.S)

    def test_text_passed_as_data_is_escaped(self, render) -> None:
        html = render('<c-heading :title="title" />', title="<script>x</script>")

        assert "<script>" not in html
