"""The hero family: what each arrangement renders, and what it never renders.

Three arrangements and one inline helper, sharing a single attribute and slot
vocabulary so that moving a page between them is a tag change and nothing else.
The assertions here are about the markup that reaches the browser. Where a
class name is the subject instead, it is because the decision under test *is* a
class — the dimming rules in `TestTheContrastDecisions` are measurements, and
the comment above that class says what was measured.
"""

import re

import pytest

# The three arrangements. The inline highlight shares none of this vocabulary
# and is tested on its own below.
ARRANGEMENTS = ["c-hero.centred", "c-hero.split", "c-hero.showcase"]


def headings(html: str) -> list[str]:
    return re.findall(r"<(h[1-6])\b", html)


class TestTheSharedVocabulary:
    @pytest.mark.parametrize("tag", ARRANGEMENTS)
    def test_the_title_is_a_first_level_heading_by_default(self, render, tag) -> None:
        html = render(f'<{tag} title="Ship it on Friday" />')

        assert headings(html) == ["h1"]
        assert "Ship it on Friday" in html

    @pytest.mark.parametrize("tag", ARRANGEMENTS)
    def test_the_heading_level_is_the_page_authors_to_set(self, render, tag) -> None:
        html = render(f'<{tag} title="Further down the page" level="2" />')

        assert headings(html) == ["h2"]
        assert "</h2>" in html

    @pytest.mark.parametrize("tag", ARRANGEMENTS)
    def test_copy_that_was_not_given_is_absent_rather_than_empty(
        self, render, tag
    ) -> None:
        html = render(f'<{tag} title="Just the words" />')

        assert "<p" not in html

    @pytest.mark.parametrize("tag", ARRANGEMENTS)
    def test_the_eyebrow_and_the_lead_render_when_they_are_given(
        self, render, tag
    ) -> None:
        html = render(
            f'<{tag} eyebrow="Version 2" title="T" lead="The sentence under it." />'
        )

        assert "Version 2" in html
        assert "The sentence under it." in html

    @pytest.mark.parametrize("tag", ARRANGEMENTS)
    def test_a_title_carrying_markup_is_escaped(self, render, tag) -> None:
        html = render(f'<{tag} title="<script>alert(1)</script>" />')

        assert "<script>" not in html
        assert "&lt;script&gt;" in html

    @pytest.mark.parametrize("tag", ARRANGEMENTS)
    def test_an_undeclared_attribute_reaches_the_section(self, render, tag) -> None:
        html = render(f'<{tag} title="T" id="lede" data-role="opener" />')

        assert 'id="lede"' in html
        assert 'data-role="opener"' in html

    @pytest.mark.parametrize("tag", ARRANGEMENTS)
    def test_the_actions_slot_renders_the_authors_own_markup(self, render, tag) -> None:
        html = render(
            f'<{tag} title="T">'
            '<c-slot name="actions">'
            '<button type="submit" name="go">Start</button>'
            "</c-slot>"
            f"</{tag}>"
        )

        assert '<button type="submit" name="go">Start</button>' in html


class TestTheBackgroundSlot:
    @pytest.mark.parametrize("tag", ARRANGEMENTS)
    def test_a_background_is_hidden_from_assistive_technology(
        self, render, tag
    ) -> None:
        html = render(
            f'<{tag} title="T">'
            '<c-slot name="background"><span id="painted"></span></c-slot>'
            f"</{tag}>"
        )

        layer = re.search(r'<div aria-hidden="true"[^>]*>(.*?)</div>', html, re.S)
        assert layer is not None, "the background slot rendered outside a hidden layer"
        assert 'id="painted"' in layer.group(1)

    @pytest.mark.parametrize("tag", ARRANGEMENTS)
    def test_there_is_no_hidden_layer_when_no_background_was_given(
        self, render, tag
    ) -> None:
        html = render(f'<{tag} title="T" />')

        assert "aria-hidden" not in html

    @pytest.mark.parametrize("tag", ARRANGEMENTS)
    def test_the_block_clips_without_becoming_a_scroll_container(
        self, render, tag
    ) -> None:
        # A parallax background measures its block crossing the screen, and
        # `overflow: hidden` would make the block the thing it measures against.
        html = render(f'<{tag} title="T" />')
        section = re.search(r"<section[^>]*>", html)

        assert section is not None
        assert "overflow-clip" in section.group(0)
        assert "overflow-hidden" not in section.group(0)


# The subject is a class name because the decision is one: contrast measured across
# the demo's ten themes, which a small aesthetic edit would quietly undo (#21).
class TestTheContrastDecisions:
    @pytest.mark.parametrize("tag", ARRANGEMENTS)
    def test_dimmed_copy_is_never_dimmer_than_eighty_percent(self, render, tag) -> None:
        html = render(f'<{tag} title="T" eyebrow="E" lead="L" />')

        assert "text-base-content/80" in html
        assert re.search(r"text-base-content/(?!80\b)\d+", html) is None

    @pytest.mark.parametrize("tag", ARRANGEMENTS)
    def test_inverted_copy_is_set_at_full_strength(self, render, tag) -> None:
        html = render(f'<{tag} title="T" eyebrow="E" lead="L" invert />')

        assert "text-neutral-content" in html
        assert "text-base-content" not in html

    @pytest.mark.parametrize("tag", ARRANGEMENTS)
    def test_no_theme_colour_is_painted_onto_the_copy(self, render, tag) -> None:
        html = render(f'<{tag} title="T" eyebrow="E" lead="L" />')

        assert "text-primary" not in html
        assert "bg-clip-text" not in html


class TestSplitHero:
    MEDIA = '<c-slot name="media"><img src="/shot.png" alt="The editor" /></c-slot>'

    @pytest.mark.parametrize("reverse", ["", "reverse"])
    def test_the_copy_precedes_the_media_in_the_document_either_way_round(
        self, render, reverse
    ) -> None:
        html = render(
            f'<c-hero.split title="Copy first" {reverse}>{self.MEDIA}</c-hero.split>'
        )

        assert html.index("Copy first") < html.index("/shot.png")

    def test_reversing_moves_the_columns_only_at_the_wide_breakpoint(
        self, render
    ) -> None:
        html = render(f'<c-hero.split title="T" reverse>{self.MEDIA}</c-hero.split>')

        assert "lg:order-1" in html
        assert "lg:order-2" in html
        assert re.search(r"(?<!lg:)\border-[12]\b", html) is None

    def test_the_media_slot_renders_the_authors_own_markup(self, render) -> None:
        html = render(f'<c-hero.split title="T">{self.MEDIA}</c-hero.split>')

        assert '<img src="/shot.png" alt="The editor" />' in html


class TestShowcaseHero:
    MEDIA = '<c-slot name="media"><img src="/panel.png" alt="The dashboard" /></c-slot>'

    def test_the_panel_follows_the_copy(self, render) -> None:
        html = render(
            f'<c-hero.showcase title="Look at this">{self.MEDIA}</c-hero.showcase>'
        )

        assert html.index("Look at this") < html.index("/panel.png")

    def test_there_is_no_panel_without_media(self, render) -> None:
        html = render('<c-hero.showcase title="T" />')

        assert "ring-1" not in html
        assert "shadow-2xl" not in html


class TestHighlight:
    def test_it_wraps_the_words_it_is_given(self, render) -> None:
        html = render("<c-hero.highlight>rebuilt</c-hero.highlight>")

        assert ">rebuilt</span>" in html

    @pytest.mark.parametrize("colour", ["primary", "secondary", "accent"])
    def test_each_colour_paints_a_fill_and_its_matching_foreground(
        self, render, colour
    ) -> None:
        html = render(f'<c-hero.highlight variant="{colour}">now</c-hero.highlight>')

        assert f"bg-{colour}" in html
        assert f"text-{colour}-content" in html

    def test_an_unrecognised_colour_falls_back_to_the_default_pair(
        self, render
    ) -> None:
        html = render('<c-hero.highlight variant="chartreuse">now</c-hero.highlight>')

        assert "bg-primary" in html
        assert "text-primary-content" in html

    def test_it_is_inline_so_it_can_sit_inside_a_heading(self, render) -> None:
        html = render("<h1>Ship <c-hero.highlight>faster</c-hero.highlight></h1>")

        assert "<span" in html
        assert "<div" not in html

    def test_the_words_it_wraps_are_escaped(self, render) -> None:
        html = render("<c-hero.highlight>{{ words }}</c-hero.highlight>", words="<b>x")

        assert "<b>x" not in html
        assert "&lt;b&gt;x" in html
