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
    """The heading tags in ``html``, in document order."""
    return re.findall(r"<(h[1-6])\b", html)


class TestTheSharedVocabulary:
    """What every arrangement does with the same attributes and slots."""

    @pytest.mark.parametrize("tag", ARRANGEMENTS)
    def test_the_title_is_a_first_level_heading_by_default(self, render, tag) -> None:
        """Right for a landing page, where the hero is the page's subject."""
        html = render(f'<{tag} title="Ship it on Friday" />')

        assert headings(html) == ["h1"]
        assert "Ship it on Friday" in html

    @pytest.mark.parametrize("tag", ARRANGEMENTS)
    def test_the_heading_level_is_the_page_authors_to_set(self, render, tag) -> None:
        """A page carrying a second hero still needs one h1 and a real order."""
        html = render(f'<{tag} title="Further down the page" level="2" />')

        assert headings(html) == ["h2"]
        assert "</h2>" in html

    @pytest.mark.parametrize("tag", ARRANGEMENTS)
    def test_copy_that_was_not_given_is_absent_rather_than_empty(
        self, render, tag
    ) -> None:
        """An empty paragraph still takes its gap in the column.

        A block that rendered one for an eyebrow nobody passed would leave a
        hole above the heading that no attribute could close.
        """
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
        """A block attribute is untrusted input, per constitution Article V."""
        html = render(f'<{tag} title="<script>alert(1)</script>" />')

        assert "<script>" not in html
        assert "&lt;script&gt;" in html

    @pytest.mark.parametrize("tag", ARRANGEMENTS)
    def test_an_undeclared_attribute_reaches_the_section(self, render, tag) -> None:
        """Anything the block does not name is the page author's to use."""
        html = render(f'<{tag} title="T" id="lede" data-role="opener" />')

        assert 'id="lede"' in html
        assert 'data-role="opener"' in html

    @pytest.mark.parametrize("tag", ARRANGEMENTS)
    def test_the_actions_slot_renders_the_authors_own_markup(self, render, tag) -> None:
        """Why the actions are a slot and not a label and href pair.

        A call to action is where a project needs full control — a form submit,
        an hx-post, a target, a tracking attribute — and none of that survives
        being passed as two strings. It would also put an author-supplied URL
        inside an href this package is then responsible for escaping.
        """
        html = render(
            f'<{tag} title="T">'
            '<c-slot name="actions">'
            '<button type="submit" name="go">Start</button>'
            "</c-slot>"
            f"</{tag}>"
        )

        assert '<button type="submit" name="go">Start</button>' in html


class TestTheBackgroundSlot:
    """The layer a background block is rendered into, and who can see it."""

    @pytest.mark.parametrize("tag", ARRANGEMENTS)
    def test_a_background_is_hidden_from_assistive_technology(
        self, render, tag
    ) -> None:
        """Which is what makes a background decoration by definition.

        An image that carries meaning belongs in the media slot of the split or
        the showcase arrangement, where it is a real img with an alt.
        """
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


class TestTheContrastDecisions:
    """The dimming rules, which are measurements rather than taste.

    This is the one place a class name is the subject of an assertion instead
    of the markup around it, because here the decision *is* a class. Both
    numbers were computed from daisyUI's own values across the ten themes the
    demo offers, and an edit that reads as a small aesthetic change is exactly
    what would quietly undo one.

    `base-content` at 80% over `base-100` bottoms out at 4.95:1 on winter,
    clearing WCAG 1.4.3's 4.5:1 for body text. At 70% winter falls to 3.86:1.

    Under `invert` the copy is full strength instead, because `neutral-content`
    at 80% over `neutral` drops to 4.09:1 on synthwave. The dimming that is
    safe on the default surface is not safe there.
    """

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
        """`text-primary` on `base-100` fails on four of the ten themes.

        cupcake 1.40:1, business 1.90:1, emerald 1.99:1 and dark 3.40:1. The
        theme-safe way to mark words is the inline highlight, which paints a
        filled surface and puts daisyUI's matching foreground on it.
        """
        html = render(f'<{tag} title="T" eyebrow="E" lead="L" />')

        assert "text-primary" not in html
        assert "bg-clip-text" not in html


class TestSplitHero:
    """Copy beside a visual, stacking to one column on a narrow screen."""

    MEDIA = '<c-slot name="media"><img src="/shot.png" alt="The editor" /></c-slot>'

    @pytest.mark.parametrize("reverse", ["", "reverse"])
    def test_the_copy_precedes_the_media_in_the_document_either_way_round(
        self, render, reverse
    ) -> None:
        """`reverse` mirrors the columns at width, never in the source.

        Reading order and tab order both follow the document, so a block that
        moved the picture ahead of the heading to put it on the left would
        change what a screen reader announces first and what the keyboard
        reaches first.
        """
        html = render(
            f'<c-hero.split title="Copy first" {reverse}>{self.MEDIA}</c-hero.split>'
        )

        assert html.index("Copy first") < html.index("/shot.png")

    def test_reversing_moves_the_columns_only_at_the_wide_breakpoint(
        self, render
    ) -> None:
        """Below `lg` the block is one column, so there is nothing to mirror."""
        html = render(f'<c-hero.split title="T" reverse>{self.MEDIA}</c-hero.split>')

        assert "lg:order-1" in html
        assert "lg:order-2" in html
        assert re.search(r"(?<!lg:)\border-[12]\b", html) is None

    def test_the_media_slot_renders_the_authors_own_markup(self, render) -> None:
        html = render(f'<c-hero.split title="T">{self.MEDIA}</c-hero.split>')

        assert '<img src="/shot.png" alt="The editor" />' in html


class TestShowcaseHero:
    """Centred copy over a wide, lifted product panel."""

    MEDIA = '<c-slot name="media"><img src="/panel.png" alt="The dashboard" /></c-slot>'

    def test_the_panel_follows_the_copy(self, render) -> None:
        html = render(
            f'<c-hero.showcase title="Look at this">{self.MEDIA}</c-hero.showcase>'
        )

        assert html.index("Look at this") < html.index("/panel.png")

    def test_there_is_no_panel_without_media(self, render) -> None:
        """An empty frame reads as a picture that failed to load."""
        html = render('<c-hero.showcase title="T" />')

        assert "ring-1" not in html
        assert "shadow-2xl" not in html

    def test_the_panel_is_lifted_by_an_edge_as_well_as_a_shadow(self, render) -> None:
        """A shadow alone reads as flat on a dark theme, where shadows are hard
        to perceive, so the elevation is carried by a surface edge too."""
        html = render(f'<c-hero.showcase title="T">{self.MEDIA}</c-hero.showcase>')

        assert "shadow-2xl" in html
        assert "ring-1" in html


class TestHighlight:
    """The inline span that fills the words it wraps with a daisyUI pair."""

    def test_it_wraps_the_words_it_is_given(self, render) -> None:
        html = render("<c-hero.highlight>rebuilt</c-hero.highlight>")

        assert ">rebuilt</span>" in html

    @pytest.mark.parametrize("colour", ["primary", "secondary", "accent"])
    def test_each_colour_paints_a_fill_and_its_matching_foreground(
        self, render, colour
    ) -> None:
        """daisyUI's pairs are chosen against each other, per theme.

        A fill without its `-content` partner is the failure this block exists
        to prevent: the marked words disappear into the fill on every theme
        whose colour is light.
        """
        html = render(f'<c-hero.highlight color="{colour}">now</c-hero.highlight>')

        assert f"bg-{colour}" in html
        assert f"text-{colour}-content" in html

    def test_an_unrecognised_colour_falls_back_to_the_default_pair(
        self, render
    ) -> None:
        """Never a bare fill with no foreground on it, whatever it is handed."""
        html = render('<c-hero.highlight color="chartreuse">now</c-hero.highlight>')

        assert "bg-primary" in html
        assert "text-primary-content" in html

    def test_it_is_inline_so_it_can_sit_inside_a_heading(self, render) -> None:
        """Documented headings-only, and the reason is the contrast bar.

        The colour pairs clear 3:1 for large text — winter is the worst at
        3.64:1 — and do not clear the 4.5:1 that body copy needs.
        """
        html = render("<h1>Ship <c-hero.highlight>faster</c-hero.highlight></h1>")

        assert "<span" in html
        assert "<div" not in html

    def test_the_words_it_wraps_are_escaped(self, render) -> None:
        html = render("<c-hero.highlight>{{ words }}</c-hero.highlight>", words="<b>x")

        assert "<b>x" not in html
        assert "&lt;b&gt;x" in html
