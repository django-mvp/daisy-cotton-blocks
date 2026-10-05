"""The background family: layers that go in another block's background slot.

A background is not part of a layout, so it is not part of a block. Each one is
its own block written into a hero's `background` slot, which is what lets any
background compose with any layout without either knowing about the other.

These blocks render a styled box and nothing else, so unlike the heroes there
is no structure to measure and the class attribute *is* the contract. What that
buys is checked twice over: `tests/test_stylesheet.py` proves the classes named
here resolve to real rules in the stylesheet this package ships, rather than
sitting in the DOM matching nothing.

An option that sets an amount is a number, and it reaches the page on the
layer's `style` attribute. That attribute is the one place a caller's value
lands in CSS, so what can be written there is tested for every such option.
"""

import re

import pytest

BACKGROUNDS = [
    "c-background.glow",
    "c-background.gradient",
    "c-background.grid",
    "c-background.image",
    "c-background.parallax",
    "c-background.aurora",
    "c-background.flow",
    "c-background.horizon",
    "c-background.particles",
    "c-background.hyperspace",
]

# The backgrounds that move by themselves, and the custom property their speed sets.
LOOPING = [
    ("c-background.aurora", "--aurora-speed"),
    ("c-background.flow", "--flow-speed"),
    ("c-background.horizon", "--horizon-speed"),
    ("c-background.particles", "--particles-speed"),
    ("c-background.hyperspace", "--hyperspace-speed"),
]

# Every option that takes a number: the declaration it sets and its default.
NUMBER_OPTIONS = [
    ("c-background.glow", "intensity", "opacity", 0.2),
    ("c-background.gradient", "opacity", "opacity", 0.2),
    ("c-background.grid", "intensity", "opacity", 0.1),
    ("c-background.grid", "size", "--grid-size", 3.5),
    ("c-background.image", "dim", "opacity", 0.7),
    ("c-background.parallax", "speed", "--parallax-speed", 0.8),
    ("c-background.aurora", "intensity", "opacity", 0.2),
    ("c-background.aurora", "speed", "--aurora-speed", 1),
    ("c-background.flow", "opacity", "opacity", 0.2),
    ("c-background.flow", "speed", "--flow-speed", 1),
    ("c-background.horizon", "intensity", "opacity", 0.2),
    ("c-background.horizon", "size", "--horizon-tile", 3.5),
    ("c-background.horizon", "speed", "--horizon-speed", 1),
    ("c-background.particles", "intensity", "opacity", 0.4),
    ("c-background.particles", "speed", "--particles-speed", 1),
    ("c-background.hyperspace", "intensity", "opacity", 0.6),
    ("c-background.hyperspace", "speed", "--hyperspace-speed", 1),
]


def declared(html: str, name: str) -> float:
    """Return the number the first `style` attribute in the markup gives a declaration."""
    found = re.search(rf'style="[^"]*?(?<![\w-]){re.escape(name)}: ([\d.]+)', html)
    assert found is not None, f"no {name} declaration in a style attribute"
    return float(found.group(1))


PALETTE = [
    "primary",
    "secondary",
    "accent",
    "neutral",
    "base-100",
    "base-200",
    "base-300",
]


class TestEveryBackgroundIsALayer:
    @pytest.mark.parametrize("tag", BACKGROUNDS)
    def test_it_roots_at_absolute_inset_zero(self, render, tag) -> None:
        html = render(f"<{tag} />")

        assert re.search(r'class="[^"]*\babsolute inset-0\b', html) is not None

    @pytest.mark.parametrize("tag", BACKGROUNDS)
    def test_extra_classes_reach_the_layer(self, render, tag) -> None:
        html = render(f'<{tag} class="rounded-3xl" />')

        assert "rounded-3xl" in html


class TestNumberOptions:
    @pytest.mark.parametrize(("tag", "option", "name", "default"), NUMBER_OPTIONS)
    def test_a_number_is_written_into_the_style(
        self, render, tag, option, name, default
    ) -> None:
        html = render(f'<{tag} {option}="0.375" />')

        assert declared(html, name) == 0.375

    @pytest.mark.parametrize(("tag", "option", "name", "default"), NUMBER_OPTIONS)
    def test_the_default_is_written_when_the_option_is_left_out(
        self, render, tag, option, name, default
    ) -> None:
        html = render(f"<{tag} />")

        assert declared(html, name) == default

    @pytest.mark.parametrize(("tag", "option", "name", "default"), NUMBER_OPTIONS)
    def test_a_value_that_is_not_a_number_falls_back_to_the_default(
        self, render, tag, option, name, default
    ) -> None:
        html = render(f'<{tag} {option}="blinding" />')

        assert declared(html, name) == default

    @pytest.mark.parametrize(("tag", "option", "name", "default"), NUMBER_OPTIONS)
    def test_a_value_carrying_a_declaration_cannot_reach_the_style(
        self, render, tag, option, name, default
    ) -> None:
        html = render(
            f'<{tag} {option}="{{{{ value }}}}" />',
            value="1; background: url(//evil.example/x)",
        )

        assert "evil.example" not in html
        assert declared(html, name) == default


class TestMotion:
    @pytest.mark.parametrize("tag", BACKGROUNDS)
    def test_nothing_animates_for_a_reader_who_asked_for_reduced_motion(
        self, render, tag
    ) -> None:
        html = render(f"<{tag} />")

        animated = re.findall(r"\S*animate-\[", html)
        assert all(cls.startswith("motion-safe:") for cls in animated)

    @pytest.mark.parametrize(("tag", "variable"), LOOPING)
    def test_the_animation_runs_at_the_speed_it_was_given(
        self, render, tag, variable
    ) -> None:
        html = render(f"<{tag} />")

        assert f"var({variable},1)" in html


class TestGlow:
    def test_it_draws_two_discs(self, render) -> None:
        html = render("<c-background.glow />")

        assert len(re.findall(r"rounded-full", html)) == 2

    def test_the_discs_default_to_the_first_two_palette_colours(self, render) -> None:
        html = render("<c-background.glow />")

        assert "bg-primary" in html
        assert "bg-secondary" in html

    @pytest.mark.parametrize("colour", PALETTE)
    def test_each_palette_colour_composes_a_fill(self, render, colour) -> None:
        html = render(f'<c-background.glow from="{colour}" to="{colour}" />')

        assert f"bg-{colour}" in html


class TestGradient:
    def test_it_runs_from_the_first_stop_to_the_last(self, render) -> None:
        html = render('<c-background.gradient from="accent" to="neutral" />')

        assert "from-accent" in html
        assert "to-neutral" in html

    def test_there_is_no_middle_stop_unless_one_was_asked_for(self, render) -> None:
        html = render("<c-background.gradient />")

        assert "via-" not in html

    def test_a_middle_stop_is_placed_when_it_is_given(self, render) -> None:
        html = render('<c-background.gradient via="accent" />')

        assert "via-accent" in html

    @pytest.mark.parametrize("direction", ["t", "tr", "r", "br", "b", "bl", "l", "tl"])
    def test_each_direction_composes_a_gradient(self, render, direction) -> None:
        html = render(f'<c-background.gradient direction="{direction}" />')

        assert f"bg-gradient-to-{direction}" in html


class TestGrid:
    def test_the_rules_are_drawn_in_the_inherited_text_colour(self, render) -> None:
        html = render("<c-background.grid />")

        assert "currentColor" in html

    def test_the_rules_are_spaced_by_the_size_it_was_given(self, render) -> None:
        html = render("<c-background.grid />")

        assert "bg-[size:var(--grid-size)_var(--grid-size)]" in html
        assert re.search(r"--grid-size: [\d.]+rem", html) is not None

    def test_the_grid_fades_out_down_the_block_by_default(self, render) -> None:
        html = render("<c-background.grid />")

        assert "mask-image" in html

    def test_flat_takes_the_fade_away(self, render) -> None:
        html = render("<c-background.grid flat />")

        assert "mask-image" not in html


class TestImage:
    def test_the_picture_is_a_real_image_element(self, render) -> None:
        html = render('<c-background.image src="/hero.jpg" />')

        assert '<img src="/hero.jpg"' in html

    def test_the_picture_carries_empty_alternative_text(self, render) -> None:
        html = render('<c-background.image src="/hero.jpg" />')

        assert 'alt=""' in html

    def test_a_url_carrying_a_quote_cannot_break_out_of_the_attribute(
        self, render
    ) -> None:
        html = render(
            '<c-background.image src="{{ url }}" />',
            url='/x.jpg" onerror="alert(1)',
        )

        assert '" onerror="' not in html
        assert "&quot; onerror=&quot;" in html

    def test_there_is_no_image_element_without_a_source(self, render) -> None:
        html = render("<c-background.image />")

        assert "<img" not in html

    def test_the_dimming_layer_is_there_whether_or_not_a_picture_is(
        self, render
    ) -> None:
        html = render("<c-background.image />")

        assert "bg-neutral" in html

    def test_dim_lands_on_the_dimming_layer_and_not_the_picture(self, render) -> None:
        html = render('<c-background.image src="/hero.jpg" dim="0.85" />')

        assert re.search(r'bg-neutral"\s+style="opacity: 0\.85', html) is not None

    @pytest.mark.parametrize("position", ["center", "top", "bottom", "left", "right"])
    def test_position_places_the_picture_in_its_frame(self, render, position) -> None:
        html = render(f'<c-background.image src="/hero.jpg" position="{position}" />')

        assert f"object-{position}" in html


class TestParallax:
    def test_it_carries_whatever_background_it_wraps(self, render) -> None:
        html = render(
            '<c-background.parallax><c-background.image src="/hero.jpg" />'
            "</c-background.parallax>"
        )

        assert '<img src="/hero.jpg"' in html

    def test_the_layer_is_tied_to_its_own_frame_crossing_the_screen(
        self, render
    ) -> None:
        html = render("<c-background.parallax />")

        assert "[view-timeline-name:--parallax]" in html
        assert "[animation-timeline:--parallax]" in html

    def test_it_clips_without_becoming_a_scroll_container(self, render) -> None:
        # `overflow: hidden` makes a scroll container, the view timeline binds to
        # the nearest one, and the layer then never moves.
        html = render("<c-background.parallax />")

        assert "overflow-clip" in html
        assert "overflow-hidden" not in html

    def test_it_stays_still_where_the_browser_has_no_scroll_timeline(
        self, render
    ) -> None:
        html = render("<c-background.parallax />")

        timed = re.findall(r"\S*(?:animate-\[|\[animation-timeline)", html)
        assert timed
        assert all("supports-[animation-timeline:view()]:" in cls for cls in timed)


class TestAurora:
    def test_it_draws_three_discs(self, render) -> None:
        html = render("<c-background.aurora />")

        assert len(re.findall(r"rounded-full", html)) == 3

    @pytest.mark.parametrize("colour", PALETTE)
    def test_each_palette_colour_composes_a_fill(self, render, colour) -> None:
        html = render(
            f'<c-background.aurora from="{colour}" via="{colour}" to="{colour}" />'
        )

        assert html.count(f"bg-{colour}") == 3


class TestFlow:
    def test_it_runs_through_three_stops(self, render) -> None:
        html = render('<c-background.flow from="accent" via="neutral" to="primary" />')

        assert "from-accent" in html
        assert "via-neutral" in html
        assert "to-primary" in html


class TestHorizon:
    def test_the_rules_are_drawn_in_the_inherited_text_colour(self, render) -> None:
        html = render("<c-background.horizon />")

        assert "currentColor" in html

    def test_the_floor_is_ruled_in_the_square_it_advances_by(self, render) -> None:
        html = render("<c-background.horizon />")

        assert "bg-[size:var(--horizon-tile)_var(--horizon-tile)]" in html
        assert re.search(r"--horizon-tile: [\d.]+rem", html) is not None


class TestParticles:
    @pytest.mark.parametrize("colour", PALETTE)
    def test_each_palette_colour_fills_the_dots(self, render, colour) -> None:
        html = render(f'<c-background.particles color="{colour}" />')

        assert f"bg-{colour}" in html


class TestHyperspace:
    @pytest.mark.parametrize(
        ("density", "streaks"),
        [
            ("1", 40),
            ("2", 80),
            ("0.5", 20),
            ("0", 0),
            ("-1", 0),
            ("100", 300),
            ("1e12", 300),
            ("lots", 40),
        ],
    )
    def test_density_sets_how_many_streaks_there_are(
        self, render, density, streaks
    ) -> None:
        html = render(f'<c-background.hyperspace density="{density}" />')

        assert html.count("--i:") == streaks

    def test_every_streak_carries_its_own_number(self, render) -> None:
        html = render('<c-background.hyperspace density="0.1" />')

        assert re.findall(r"--i: (\d+)", html) == ["0", "1", "2", "3"]

    @pytest.mark.parametrize("colour", PALETTE)
    def test_each_palette_colour_colours_the_streaks(self, render, colour) -> None:
        html = render(f'<c-background.hyperspace color="{colour}" />')

        assert f"text-{colour}" in html
