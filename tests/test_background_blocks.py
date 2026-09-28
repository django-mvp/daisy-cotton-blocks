"""The background family: layers that go in another block's background slot.

A background is not part of a layout, so it is not part of a block. Each one is
its own block written into a hero's `background` slot, which is what lets any
background compose with any layout without either knowing about the other.

These blocks render a styled box and nothing else, so unlike the heroes there
is no structure to measure and the class attribute *is* the contract. What that
buys is checked twice over: `tests/test_stylesheet.py` proves the classes named
here resolve to real rules in the stylesheet this package ships, rather than
sitting in the DOM matching nothing.
"""

import re

import pytest

BACKGROUNDS = [
    "c-background.glow",
    "c-background.gradient",
    "c-background.grid",
    "c-background.image",
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


class TestEveryBackgroundIsALayer:
    @pytest.mark.parametrize("tag", BACKGROUNDS)
    def test_it_roots_at_absolute_inset_zero(self, render, tag) -> None:
        html = render(f"<{tag} />")

        assert re.search(r'class="[^"]*\babsolute inset-0\b', html) is not None

    @pytest.mark.parametrize("tag", BACKGROUNDS)
    def test_it_carries_no_inline_style_attribute(self, render, tag) -> None:
        html = render(f'<{tag} src="/photo.jpg" />')

        assert "style=" not in html

    @pytest.mark.parametrize("tag", BACKGROUNDS)
    def test_extra_classes_reach_the_layer(self, render, tag) -> None:
        html = render(f'<{tag} class="rounded-3xl" />')

        assert "rounded-3xl" in html


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

    @pytest.mark.parametrize(
        ("intensity", "opacity"),
        [("faint", "opacity-10"), ("soft", "opacity-20"), ("bold", "opacity-30")],
    )
    def test_intensity_sets_how_far_the_discs_come_through(
        self, render, intensity, opacity
    ) -> None:
        html = render(f'<c-background.glow intensity="{intensity}" />')

        assert opacity in html

    def test_an_unrecognised_intensity_falls_back_to_the_default(self, render) -> None:
        html = render('<c-background.glow intensity="blinding" />')

        assert "opacity-20" in html


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

    @pytest.mark.parametrize(
        ("opacity", "expected"),
        [("faint", "opacity-10"), ("soft", "opacity-20"), ("full", "opacity-100")],
    )
    def test_opacity_sets_how_much_of_the_surface_shows_through(
        self, render, opacity, expected
    ) -> None:
        html = render(f'<c-background.gradient opacity="{opacity}" />')

        assert expected in html


class TestGrid:
    def test_the_rules_are_drawn_in_the_inherited_text_colour(self, render) -> None:
        html = render("<c-background.grid />")

        assert "currentColor" in html

    @pytest.mark.parametrize(
        ("size", "expected"),
        [
            ("sm", "bg-[size:2rem_2rem]"),
            ("md", "bg-[size:3.5rem_3.5rem]"),
            ("lg", "bg-[size:5rem_5rem]"),
        ],
    )
    def test_size_sets_the_spacing_of_the_rules(self, render, size, expected) -> None:
        html = render(f'<c-background.grid size="{size}" />')

        assert expected in html

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

    @pytest.mark.parametrize(
        ("dim", "expected"),
        [("soft", "opacity-50"), ("medium", "opacity-70"), ("strong", "opacity-85")],
    )
    def test_dim_is_three_named_steps(self, render, dim, expected) -> None:
        html = render(f'<c-background.image src="/hero.jpg" dim="{dim}" />')

        assert expected in html

    @pytest.mark.parametrize("position", ["center", "top", "bottom", "left", "right"])
    def test_position_places_the_picture_in_its_frame(self, render, position) -> None:
        html = render(f'<c-background.image src="/hero.jpg" position="{position}" />')

        assert f"object-{position}" in html
