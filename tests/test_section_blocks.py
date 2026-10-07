"""The section shell and its columns: what a page author can pass in, and what comes out."""

import re

import pytest

COLUMNS = "<c-section.col>One</c-section.col><c-section.col>Two</c-section.col>"


class TestSection:
    def test_it_is_a_section(self, render) -> None:
        html = render('<c-section id="pricing">Body</c-section>')

        assert re.match(r'\s*<section[^>]*\bid="pricing"', html) is not None

    def test_extra_classes_reach_the_section(self, render) -> None:
        html = render('<c-section class="bg-base-200">Body</c-section>')

        assert re.match(r'\s*<section[^>]*class="[^"]*\bbg-base-200\b', html)

    def test_a_background_is_rendered_into_a_layer_hidden_from_readers(
        self, render
    ) -> None:
        html = render(
            '<c-section><c-slot name="background"><i id="wash"></i></c-slot>Body'
            "</c-section>"
        )

        layer = re.search(r'<div aria-hidden="true"[^>]*>(.*?)</div>', html, re.S)
        assert layer is not None
        assert 'id="wash"' in layer.group(1)

    def test_a_section_with_no_background_has_no_layer(self, render) -> None:
        html = render("<c-section>Body</c-section>")

        assert "aria-hidden" not in html

    def test_the_header_comes_before_the_columns(self, render) -> None:
        html = render(
            f'<c-section>{COLUMNS}<c-slot name="header"><h2 id="head">H</h2></c-slot>'
            "</c-section>"
        )

        assert html.index('id="head"') < html.index("data-section-col")

    def test_the_columns_stay_in_the_order_written_when_reversed(self, render) -> None:
        html = render(f"<c-section reverse>{COLUMNS}</c-section>")

        assert html.index("One") < html.index("Two")

    def test_reversing_moves_the_columns_only_at_the_wide_breakpoint(
        self, render
    ) -> None:
        html = render(f"<c-section reverse>{COLUMNS}</c-section>")

        moved = re.findall(r"[^\s\"]*order-\[[^\s\"]*", html)
        assert moved
        assert all(name.startswith("dce:lg:") for name in moved)

    def test_nothing_is_reordered_unless_asked(self, render) -> None:
        html = render(f"<c-section>{COLUMNS}</c-section>")

        assert "order-" not in html

    def test_a_screen_high_section_is_at_least_as_tall_as_the_window(
        self, render
    ) -> None:
        html = render('<c-section height="screen">Body</c-section>')

        assert "min-h-screen" in html

    def test_a_section_is_as_tall_as_its_content_by_default(self, render) -> None:
        html = render("<c-section>Body</c-section>")

        assert "min-h-screen" not in html

    def test_a_flush_section_adds_no_room_above_or_below(self, render) -> None:
        html = render("<c-section flush>Body</c-section>")

        assert re.search(r"\bpy-", html) is None

    @pytest.mark.parametrize(
        ("container", "width"),
        [("narrow", "max-w-2xl"), ("", "max-w-6xl"), ("wide", "max-w-7xl")],
    )
    def test_the_content_is_held_to_the_chosen_width(
        self, render, container, width
    ) -> None:
        html = render(f'<c-section container="{container}">Body</c-section>')

        body = re.search(r'<div data-section-body\s+class="([^"]*)"', html)
        assert f"dce:{width}" in body.group(1).split()

    def test_full_width_content_has_no_gutter(self, render) -> None:
        html = render('<c-section container="full">Body</c-section>')

        body = re.search(r'<div data-section-body\s+class="([^"]*)"', html)
        assert re.search(r"\bpx-", body.group(1)) is None

    def test_the_width_is_never_set_on_the_section_itself(self, render) -> None:
        html = render('<c-section container="narrow">Body</c-section>')

        section = re.match(r'\s*<section[^>]*class="([^"]*)"', html)
        assert "max-w-" not in section.group(1)


class TestColumn:
    def test_it_carries_the_hook_the_section_counts_columns_by(self, render) -> None:
        html = render("<c-section.col>One</c-section.col>")

        assert re.match(r"\s*<div data-section-col\b", html) is not None

    def test_extra_classes_and_attributes_reach_the_column(self, render) -> None:
        html = render('<c-section.col id="copy" class="bg-primary">One</c-section.col>')

        assert 'id="copy"' in html
        assert re.search(r'class="[^"]*\bbg-primary\b', html)

    def test_a_column_takes_one_share_of_the_width_by_default(self, render) -> None:
        html = render("<c-section.col>One</c-section.col>")

        assert 'style="--section-span: 1"' in html

    def test_the_span_is_passed_on(self, render) -> None:
        html = render('<c-section.col span="3">One</c-section.col>')

        assert 'style="--section-span: 3"' in html

    @pytest.mark.parametrize("span", ["", "wide", "2; color: red"])
    def test_nothing_but_a_number_is_a_span(self, render, span) -> None:
        html = render('<c-section.col :span="span">One</c-section.col>', span=span)

        assert 'style="--section-span: 1"' in html
        assert "color: red" not in html

    def test_a_background_is_rendered_into_a_layer_hidden_from_readers(
        self, render
    ) -> None:
        html = render(
            '<c-section.col><c-slot name="background"><i id="grid"></i></c-slot>One'
            "</c-section.col>"
        )

        layer = re.search(r'<div aria-hidden="true"[^>]*>(.*?)</div>', html, re.S)
        assert layer is not None
        assert 'id="grid"' in layer.group(1)

    def test_a_column_with_no_background_has_no_layer(self, render) -> None:
        html = render("<c-section.col>One</c-section.col>")

        assert "aria-hidden" not in html
