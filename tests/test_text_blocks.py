"""The text family: effects applied to a few words inside a heading or a line.

Each one is a span, so it goes anywhere words go and inherits the size and
weight of whatever it sits in. As with the backgrounds, the class attribute is
the contract, and `tests/test_stylesheet.py` proves those classes resolve to
real rules in the stylesheet this package ships.

Two things are checked here that a stylesheet cannot be asked about. A number
a caller passes lands on the span's `style` attribute, so what can be written
there is tested for every such option. And an effect that draws the words more
than once, or a letter at a time, has to reach a screen reader as the words,
once.
"""

import re
from html.parser import HTMLParser

import pytest

# The effects that wrap words, and the ones that take a line to split up.
WRAPPING = [
    "c-text.glow",
    "c-text.outline",
    "c-text.depth",
    "c-text.gradient",
    "c-text.shimmer",
    "c-text.marker",
    "c-text.glitch",
]
SPLITTING = ["c-text.typewriter", "c-text.wave"]

# Every option that takes a number: the custom property it sets and its default.
NUMBER_OPTIONS = [
    ("c-text.glow", "intensity", "--glow-intensity", 0.7),
    ("c-text.glow", "spread", "--glow-spread", 1),
    ("c-text.glow", "pulse", "--glow-pulse", 0),
    ("c-text.outline", "weight", "--outline-weight", 1.5),
    ("c-text.depth", "depth", "--depth", 1),
    ("c-text.gradient", "speed", "--gradient-speed", 1),
    ("c-text.shimmer", "speed", "--shimmer-speed", 1),
    ("c-text.shimmer", "frequency", "--shimmer-frequency", 1),
    ("c-text.marker", "size", "--marker-size", 0.25),
    ("c-text.marker", "speed", "--marker-speed", 1),
    ("c-text.marker", "delay", "--marker-delay", 0.3),
    ("c-text.typewriter", "speed", "--type-speed", 1),
    ("c-text.typewriter", "delay", "--type-delay", 0.3),
    ("c-text.wave", "height", "--wave-height", 0.2),
    ("c-text.wave", "speed", "--wave-speed", 1),
    ("c-text.glitch", "intensity", "--glitch-intensity", 1),
    ("c-text.glitch", "frequency", "--glitch-frequency", 1),
]

# The effects that keep going, and the custom property that stops them.
LOOPING = [
    ("c-text.glow", 'pulse="1"', "--glow-repeat"),
    ("c-text.gradient", "", "--gradient-repeat"),
    ("c-text.shimmer", "", "--shimmer-repeat"),
    ("c-text.wave", "", "--wave-repeat"),
    ("c-text.glitch", "", "--glitch-repeat"),
]

# The option that sets an animation's length by dividing by it, per effect.
PACED = [
    ("c-text.glow", "pulse"),
    ("c-text.gradient", "speed"),
    ("c-text.shimmer", "frequency"),
    ("c-text.marker", "speed"),
    ("c-text.typewriter", "speed"),
    ("c-text.wave", "speed"),
    ("c-text.glitch", "frequency"),
]

PALETTE = [
    "primary",
    "secondary",
    "accent",
    "neutral",
    "base-100",
    "base-200",
    "base-300",
]


def markup(tag: str, attributes: str = "") -> str:
    """Return the markup that uses an effect on a short line."""
    if tag in SPLITTING:
        return f'<{tag} text="Ship it" {attributes} />'
    return f"<{tag} {attributes}>Ship it</{tag}>"


def declared(html: str, name: str) -> str:
    """Return what the first `style` attribute in the markup gives a declaration."""
    found = re.search(rf'style="[^"]*?(?<![\w-]){re.escape(name)}: ([^;"]+)', html)
    assert found is not None, f"no {name} declaration in a style attribute"
    return found.group(1)


class Spoken(HTMLParser):
    """Collect the text a screen reader is given, skipping `aria-hidden` subtrees.

    Attributes:
        words: The text nodes outside any hidden subtree, in document order.
    """

    def __init__(self) -> None:
        super().__init__()
        self.words: list[str] = []
        self.open: list[bool] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Note whether this element, or one it sits in, is hidden."""
        hidden = ("aria-hidden", "true") in attrs
        self.open.append(hidden or (bool(self.open) and self.open[-1]))

    def handle_endtag(self, tag: str) -> None:
        """Leave the element."""
        self.open.pop()

    def handle_data(self, data: str) -> None:
        """Keep text that sits outside every hidden element."""
        if not (self.open and self.open[-1]):
            self.words.append(data)


def spoken(html: str) -> str:
    """Return the words left once everything hidden from a screen reader is cut."""
    parser = Spoken()
    parser.feed(html)
    return " ".join("".join(parser.words).split())


class TestEveryEffectIsASpan:
    @pytest.mark.parametrize("tag", WRAPPING + SPLITTING)
    def test_it_roots_at_a_span(self, render, tag) -> None:
        html = render(markup(tag))

        assert html.strip().startswith("<span")
        assert html.strip().endswith("</span>")

    @pytest.mark.parametrize("tag", WRAPPING + SPLITTING)
    def test_extra_classes_reach_the_span(self, render, tag) -> None:
        html = render(markup(tag, 'class="tracking-wide"'))

        assert re.match(r'<span class="[^"]*\btracking-wide\b', html.strip())

    @pytest.mark.parametrize("tag", WRAPPING + SPLITTING)
    def test_other_attributes_are_forwarded_to_the_span(self, render, tag) -> None:
        html = render(markup(tag, 'id="headline"'))

        assert re.match(r'<span [^>]*\bid="headline"', html.strip())

    @pytest.mark.parametrize("tag", WRAPPING + SPLITTING)
    def test_a_screen_reader_is_given_the_words_once(self, render, tag) -> None:
        html = render(markup(tag))

        assert spoken(html) == "Ship it"


class TestNumberOptions:
    @pytest.mark.parametrize(("tag", "option", "name", "default"), NUMBER_OPTIONS)
    def test_a_number_is_written_into_the_style(
        self, render, tag, option, name, default
    ) -> None:
        html = render(markup(tag, f'{option}="0.375"'))

        assert float(declared(html, name)) == 0.375

    @pytest.mark.parametrize(("tag", "option", "name", "default"), NUMBER_OPTIONS)
    def test_the_default_is_written_when_the_option_is_left_out(
        self, render, tag, option, name, default
    ) -> None:
        html = render(markup(tag))

        assert float(declared(html, name)) == default

    @pytest.mark.parametrize(("tag", "option", "name", "default"), NUMBER_OPTIONS)
    def test_a_value_that_is_not_a_number_falls_back_to_the_default(
        self, render, tag, option, name, default
    ) -> None:
        html = render(markup(tag, f'{option}="blinding"'))

        assert float(declared(html, name)) == default

    @pytest.mark.parametrize(("tag", "option", "name", "default"), NUMBER_OPTIONS)
    def test_a_value_carrying_a_declaration_cannot_reach_the_style(
        self, render, tag, option, name, default
    ) -> None:
        html = render(
            markup(tag, f'{option}="{{{{ value }}}}"'),
            value="1; background: url(//evil.example/x)",
        )

        assert "evil.example" not in html
        assert float(declared(html, name)) == default


class TestMotion:
    @pytest.mark.parametrize("tag", WRAPPING + SPLITTING)
    def test_nothing_animates_for_a_reader_who_asked_for_reduced_motion(
        self, render, tag
    ) -> None:
        html = render(markup(tag, 'pulse="1"' if tag == "c-text.glow" else ""))

        animated = re.findall(r'[^\s"]*animate-\[', html)
        assert all(cls.startswith("dce:motion-safe:") for cls in animated)

    @pytest.mark.parametrize(("tag", "option"), PACED)
    def test_an_effect_given_a_pace_is_animated(self, render, tag, option) -> None:
        html = render(markup(tag, f'{option}="2"'))

        assert "animate-[" in html

    @pytest.mark.parametrize(("tag", "option"), PACED)
    def test_a_pace_of_nothing_leaves_the_words_at_rest(
        self, render, tag, option
    ) -> None:
        # An animation's length is a division by its pace, and one of no length
        # either never ends or never starts. Neither may reach the page.
        html = render(markup(tag, f'{option}="0"'))

        assert "animate-[" not in html

    @pytest.mark.parametrize(("tag", "attributes", "variable"), LOOPING)
    def test_it_never_stops_unless_it_is_told_how_many_times_to_run(
        self, render, tag, attributes, variable
    ) -> None:
        html = render(markup(tag, attributes))

        assert declared(html, variable) == "infinite"
        assert f"var({variable},infinite)" in html

    @pytest.mark.parametrize(("tag", "attributes", "variable"), LOOPING)
    def test_repeat_sets_how_many_times_it_runs(
        self, render, tag, attributes, variable
    ) -> None:
        html = render(markup(tag, f'{attributes} repeat="3"'))

        assert declared(html, variable) == "3"

    @pytest.mark.parametrize(("tag", "attributes", "variable"), LOOPING)
    def test_a_repeat_that_is_not_a_number_cannot_reach_the_style(
        self, render, tag, attributes, variable
    ) -> None:
        html = render(
            markup(tag, f'{attributes} repeat="{{{{ value }}}}"'),
            value="1; background: url(//evil.example/x)",
        )

        assert "evil.example" not in html
        assert declared(html, variable) == "infinite"


class TestGlow:
    def test_the_halo_is_a_copy_of_the_words_behind_them(self, render) -> None:
        html = render("<c-text.glow>Ship it</c-text.glow>")

        assert html.count("Ship it") == 2
        assert re.search(r'<span aria-hidden="true"[^>]*>Ship it</span>', html)

    def test_a_steady_halo_carries_no_animation(self, render) -> None:
        html = render("<c-text.glow>Ship it</c-text.glow>")

        assert "animate-[" not in html

    @pytest.mark.parametrize("colour", PALETTE)
    def test_each_palette_colour_lights_the_words(self, render, colour) -> None:
        html = render(f'<c-text.glow variant="{colour}">Ship it</c-text.glow>')

        assert f"text-{colour}" in html


class TestOutline:
    def test_the_letters_are_emptied_and_the_line_takes_their_colour(
        self, render
    ) -> None:
        html = render("<c-text.outline>Ship it</c-text.outline>")

        assert "[-webkit-text-fill-color:transparent]" in html
        assert "[-webkit-text-stroke-color:currentColor]" in html

    def test_the_line_is_the_text_colour_of_the_page_by_default(self, render) -> None:
        html = render("<c-text.outline>Ship it</c-text.outline>")

        assert "text-base-content" in html

    @pytest.mark.parametrize("colour", ["primary", "secondary", "accent", "neutral"])
    def test_each_colour_draws_the_line(self, render, colour) -> None:
        html = render(f'<c-text.outline variant="{colour}">Ship it</c-text.outline>')

        assert f"text-{colour}" in html


class TestDepth:
    @pytest.mark.parametrize("colour", PALETTE)
    def test_each_palette_colour_colours_the_edge(self, render, colour) -> None:
        html = render(f'<c-text.depth variant="{colour}">Ship it</c-text.depth>')

        assert f"text-shadow-{colour}" in html


class TestGradient:
    def test_it_runs_through_three_stops_clipped_to_the_letters(self, render) -> None:
        html = render(
            '<c-text.gradient from="accent" via="neutral" to="primary">Ship it'
            "</c-text.gradient>"
        )

        assert "from-accent" in html
        assert "via-neutral" in html
        assert "to-primary" in html
        assert "bg-clip-text" in html


class TestShimmer:
    def test_the_words_keep_their_own_colour(self, render) -> None:
        html = render("<c-text.shimmer>Ship it</c-text.shimmer>")

        assert "from-current" in html
        assert "to-current" in html
        assert "text-transparent" not in html

    @pytest.mark.parametrize("colour", PALETTE)
    def test_each_palette_colour_colours_the_band(self, render, colour) -> None:
        html = render(f'<c-text.shimmer variant="{colour}">Ship it</c-text.shimmer>')

        assert f"via-{colour}" in html

    def test_how_far_the_band_travels_follows_its_speed_and_its_frequency(
        self, render
    ) -> None:
        html = render("<c-text.shimmer>Ship it</c-text.shimmer>")

        assert "var(--shimmer-speed,1)/var(--shimmer-frequency,1)" in html

    def test_a_band_that_never_crosses_still_has_somewhere_to_rest(
        self, render
    ) -> None:
        # The width of the background is a division by the frequency as well.
        html = render('<c-text.shimmer frequency="0">Ship it</c-text.shimmer>')

        assert float(declared(html, "--shimmer-frequency")) != 0


class TestMarker:
    @pytest.mark.parametrize("colour", PALETTE)
    def test_each_palette_colour_draws_the_stroke(self, render, colour) -> None:
        html = render(f'<c-text.marker variant="{colour}">Ship it</c-text.marker>')

        assert f"from-{colour}" in html
        assert f"to-{colour}" in html

    def test_the_stroke_is_there_before_and_after_it_is_drawn(self, render) -> None:
        # At rest the stroke is full width, so it shows with no animation at all.
        html = render("<c-text.marker>Ship it</c-text.marker>")

        assert "[background-size:100%_calc(var(--marker-size,0.25)*1em)]" in html


class TestTypewriter:
    def test_every_letter_carries_its_own_number(self, render) -> None:
        html = render('<c-text.typewriter text="Ship" />')

        assert re.findall(r"--i: (\d+)", html) == ["0", "1", "2", "3"]

    def test_the_line_is_given_whole_to_a_screen_reader(self, render) -> None:
        html = render('<c-text.typewriter text="Ship it" />')

        assert '<span class="dce:sr-only">Ship it</span>' in html

    def test_the_caret_stops_blinking(self, render) -> None:
        html = render('<c-text.typewriter text="Ship" />')

        assert "infinite" not in html

    def test_markup_in_the_line_is_escaped_letter_by_letter(self, render) -> None:
        html = render('<c-text.typewriter text="{{ line }}" />', line="a<b>&c")

        assert "<b>" not in html
        assert ">&lt;</span>" in html
        assert ">&amp;</span>" in html

    def test_a_line_passed_as_a_variable_is_typed_as_it_stands(self, render) -> None:
        html = render('<c-text.typewriter :text="line" />', line="R&D")

        assert re.findall(r'style="--i: \d+">([^<]+)<', html) == ["R", "&amp;", "D"]

    def test_a_line_written_into_the_markup_is_typed_as_it_stands(self, render) -> None:
        html = render('<c-text.typewriter text="R&D" />')

        assert re.findall(r'style="--i: \d+">([^<]+)<', html) == ["R", "&amp;", "D"]


class TestWave:
    def test_every_word_is_kept_whole(self, render) -> None:
        html = render('<c-text.wave text="Ship it now" />')

        assert html.count("dce:inline-block dce:whitespace-nowrap") == 3

    def test_a_letter_takes_its_turn_from_its_word_and_its_place_in_it(
        self, render
    ) -> None:
        html = render('<c-text.wave text="Go on" />')

        assert re.findall(r"--w: (\d+)", html) == ["0", "1"]
        assert re.findall(r"--i: (\d+)", html) == ["0", "1", "0", "1"]

    def test_the_line_is_given_whole_to_a_screen_reader(self, render) -> None:
        html = render('<c-text.wave text="Ship it" />')

        assert '<span class="dce:sr-only">Ship it</span>' in html

    def test_markup_in_the_line_is_escaped_letter_by_letter(self, render) -> None:
        html = render('<c-text.wave text="{{ line }}" />', line="a<b>")

        assert "<b>" not in html
        assert ">&lt;</span>" in html


class TestGlitch:
    def test_the_slices_are_two_copies_laid_over_the_words(self, render) -> None:
        html = render("<c-text.glitch>Ship it</c-text.glitch>")

        assert html.count("Ship it") == 3
        assert len(re.findall(r'<span aria-hidden="true"', html)) == 2

    def test_the_slices_are_out_of_sight_until_a_break(self, render) -> None:
        html = render("<c-text.glitch>Ship it</c-text.glitch>")

        assert html.count("opacity-0") == 2

    @pytest.mark.parametrize("colour", PALETTE)
    def test_each_palette_colour_colours_the_slices(self, render, colour) -> None:
        html = render(
            f'<c-text.glitch from="{colour}" to="{colour}">Ship it</c-text.glitch>'
        )

        assert html.count(f"text-{colour}") == 2
