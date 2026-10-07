"""The reveal family: wrappers that bring content in as it is scrolled to or pointed at.

A reveal adds movement to something the page author wrote, so three things are
the contract. The content still renders when nothing moves. Every movement is
switched off for a reader who asked for reduced motion and in a browser that
cannot tie an animation to the scroll position. And an option that sets an
amount reaches the page as a number on the `style` attribute and as nothing
else.
"""

import re

import pytest

# The reveals driven by the scroll position.
SCROLL_DRIVEN = [
    "c-reveal.enter",
    "c-reveal.cascade",
    "c-reveal.wipe",
]

# The reveals that wrap whatever the author puts inside them.
WRAPPERS = [*SCROLL_DRIVEN, "c-reveal.stack", "c-reveal.hover"]

# Every option that takes a number: the declaration it sets and its default.
NUMBER_OPTIONS = [
    ("c-reveal.enter", "distance", "--reveal-distance", 2),
    ("c-reveal.enter", "over", "--reveal-over", 1),
    ("c-reveal.cascade", "distance", "--reveal-distance", 2),
    ("c-reveal.cascade", "step", "--reveal-step", 0.25),
    ("c-reveal.cascade", "per", "--reveal-per", 0),
    ("c-reveal.cascade", "over", "--reveal-over", 1),
    ("c-reveal.wipe", "zoom", "--reveal-scale", 1.1),
    ("c-reveal.wipe", "over", "--reveal-over", 1),
    ("c-reveal.words", "dim", "--words-dim", 0.25),
    ("c-reveal.words", "start", "--words-start", 0.1),
    ("c-reveal.words", "end", "--words-end", 0.5),
    ("c-reveal.hover", "zoom", "--hover-zoom", 1.05),
    ("c-reveal.stack", "top", "--stack-top", 0),
    ("c-reveal.stack", "step", "--stack-step", 0),
]

EFFECTS = ["up", "down", "left", "right", "zoom", "blur", "fade"]

SCROLL_TIMED = re.compile(
    r"[^\s\"]*(?:animate-\[|\[animation-timeline|\[animation-range)"
)


def tag_with(tag: str, attributes: str = "") -> str:
    """Return markup for a reveal, giving the one that needs words some words."""
    if tag == "c-reveal.words":
        return f'<{tag} text="Ship on a Friday" {attributes} />'
    return f"<{tag} {attributes}><b>inside</b></{tag}>"


def declared(html: str, name: str) -> float:
    """Return the number the first `style` attribute in the markup gives a declaration."""
    found = re.search(rf'style="[^"]*?(?<![\w-]){re.escape(name)}: ([\d.]+)', html)
    assert found is not None, f"no {name} declaration in a style attribute"
    return float(found.group(1))


class TestEveryWrapperCarriesItsContent:
    @pytest.mark.parametrize("tag", WRAPPERS)
    def test_what_it_wraps_is_rendered(self, render, tag) -> None:
        html = render(f"<{tag}><b>inside</b></{tag}>")

        assert "<b>inside</b>" in html

    @pytest.mark.parametrize("tag", [*WRAPPERS, "c-reveal.words"])
    def test_extra_classes_reach_the_outer_element(self, render, tag) -> None:
        html = render(tag_with(tag, 'class="rounded-3xl"'))

        assert re.match(r'\s*<\w+[^>]*class="[^"]*\brounded-3xl\b', html) is not None

    @pytest.mark.parametrize("tag", [*WRAPPERS, "c-reveal.words"])
    def test_an_undeclared_attribute_reaches_the_outer_element(
        self, render, tag
    ) -> None:
        html = render(tag_with(tag, 'id="pricing"'))

        assert re.match(r'\s*<\w+[^>]*\bid="pricing"', html) is not None


class TestNumberOptions:
    @pytest.mark.parametrize(("tag", "option", "name", "default"), NUMBER_OPTIONS)
    def test_a_number_is_written_into_the_style(
        self, render, tag, option, name, default
    ) -> None:
        html = render(tag_with(tag, f'{option}="0.375"'))

        assert declared(html, name) == 0.375

    @pytest.mark.parametrize(("tag", "option", "name", "default"), NUMBER_OPTIONS)
    def test_the_default_is_written_when_the_option_is_left_out(
        self, render, tag, option, name, default
    ) -> None:
        html = render(tag_with(tag))

        assert declared(html, name) == default

    @pytest.mark.parametrize(("tag", "option", "name", "default"), NUMBER_OPTIONS)
    def test_a_value_that_is_not_a_number_falls_back_to_the_default(
        self, render, tag, option, name, default
    ) -> None:
        html = render(tag_with(tag, f'{option}="plenty"'))

        assert declared(html, name) == default

    @pytest.mark.parametrize(("tag", "option", "name", "default"), NUMBER_OPTIONS)
    def test_a_value_carrying_a_declaration_cannot_reach_the_style(
        self, render, tag, option, name, default
    ) -> None:
        html = render(
            tag_with(tag, f'{option}="{{{{ value }}}}"'),
            value="1; background: url(//evil.example/x)",
        )

        assert "evil.example" not in html
        assert declared(html, name) == default


class TestMotion:
    @pytest.mark.parametrize("tag", [*SCROLL_DRIVEN, "c-reveal.words"])
    def test_nothing_is_tied_to_the_scroll_for_a_reader_who_asked_for_reduced_motion(
        self, render, tag
    ) -> None:
        html = render(tag_with(tag))

        timed = SCROLL_TIMED.findall(html)
        assert timed
        assert all(cls.startswith("dce:motion-safe:") for cls in timed)

    @pytest.mark.parametrize("tag", [*SCROLL_DRIVEN, "c-reveal.words"])
    def test_it_stays_put_where_the_browser_has_no_scroll_timeline(
        self, render, tag
    ) -> None:
        html = render(tag_with(tag))

        timed = SCROLL_TIMED.findall(html)
        assert all("supports-[animation-timeline:view()]:" in cls for cls in timed)

    @pytest.mark.parametrize("tag", [*WRAPPERS, "c-reveal.words"])
    def test_it_never_becomes_a_scroll_container(self, render, tag) -> None:
        # `overflow: hidden` makes a scroll container. A view timeline inside one
        # measures against it and never moves, and a sticky panel never sticks.
        html = render(tag_with(tag))

        assert "overflow-hidden" not in html

    def test_hover_does_not_slide_or_grow_under_reduced_motion(self, render) -> None:
        html = render("<c-reveal.hover><b>inside</b></c-reveal.hover>")

        moving = re.findall(r"[^\s\"]*(?:transition-|scale-\[)", html)
        assert moving
        assert all(cls.startswith("dce:motion-safe:") for cls in moving)


class TestEffect:
    @pytest.mark.parametrize("tag", ["c-reveal.enter", "c-reveal.cascade"])
    @pytest.mark.parametrize(
        ("effect", "axis", "sign"),
        [("up", "y", ""), ("down", "y", "-"), ("left", "x", ""), ("right", "x", "-")],
    )
    def test_a_direction_starts_the_content_on_the_side_it_travels_from(
        self, render, tag, effect, axis, sign
    ) -> None:
        html = render(f'<{tag} effect="{effect}"><b>inside</b></{tag}>')

        offsets = re.findall(r"\[--reveal-([xy]):([^\]]+)\]", html)
        assert len(offsets) == 1
        assert offsets[0][0] == axis
        assert offsets[0][1].endswith("*-1)") == (sign == "-")

    @pytest.mark.parametrize("tag", ["c-reveal.enter", "c-reveal.cascade"])
    @pytest.mark.parametrize("effect", ["zoom", "blur", "fade"])
    def test_an_effect_that_does_not_travel_sets_no_offset(
        self, render, tag, effect
    ) -> None:
        html = render(f'<{tag} effect="{effect}"><b>inside</b></{tag}>')

        assert "[--reveal-x:" not in html
        assert "[--reveal-y:" not in html

    @pytest.mark.parametrize("tag", ["c-reveal.enter", "c-reveal.cascade"])
    def test_zoom_starts_the_content_smaller(self, render, tag) -> None:
        html = render(f'<{tag} effect="zoom"><b>inside</b></{tag}>')

        assert "[--reveal-scale:" in html

    @pytest.mark.parametrize("tag", ["c-reveal.enter", "c-reveal.cascade"])
    @pytest.mark.parametrize("effect", EFFECTS)
    def test_only_blur_runs_the_blurring_animation(self, render, tag, effect) -> None:
        html = render(f'<{tag} effect="{effect}"><b>inside</b></{tag}>')

        assert ("dce-reveal-blur" in html) == (effect == "blur")
        assert len(re.findall(r"animate-\[", html)) == 1

    @pytest.mark.parametrize("tag", ["c-reveal.enter", "c-reveal.cascade"])
    def test_an_unrecognised_effect_falls_back_to_rising(self, render, tag) -> None:
        html = render(f'<{tag} effect="spin"><b>inside</b></{tag}>')

        assert html == render(f'<{tag} effect="up"><b>inside</b></{tag}>')


class TestCascade:
    def test_the_animation_lands_on_the_children_and_not_the_wrapper(
        self, render
    ) -> None:
        html = render("<c-reveal.cascade><b>inside</b></c-reveal.cascade>")

        timed = SCROLL_TIMED.findall(html)
        assert all(":*:" in cls for cls in timed)

    def test_each_of_the_first_twelve_children_is_given_its_number(
        self, render
    ) -> None:
        html = render("<c-reveal.cascade><b>inside</b></c-reveal.cascade>")

        numbered = re.findall(r"\*:nth-(\d+):\[--reveal-i:(\d+)\]", html)
        assert [(int(nth), int(i)) for nth, i in numbered] == [
            (n, n - 1) for n in range(2, 13)
        ]

    def test_children_are_counted_straight_through_by_default(self, render) -> None:
        html = render("<c-reveal.cascade><b>inside</b></c-reveal.cascade>")

        assert "mod(" not in html

    def test_per_restarts_the_count_on_each_row(self, render) -> None:
        html = render('<c-reveal.cascade per="3"><b>inside</b></c-reveal.cascade>')

        assert "*:[--reveal-n:mod(var(--reveal-i,0),var(--reveal-per))]" in html

    @pytest.mark.parametrize("per", ["0", "-2", "2.5", "three"])
    def test_a_per_that_is_not_a_whole_row_never_divides_by_it(
        self, render, per
    ) -> None:
        html = render(f'<c-reveal.cascade per="{per}"><b>inside</b></c-reveal.cascade>')

        assert "mod(" not in html


class TestWipe:
    @pytest.mark.parametrize(
        ("edge", "covered"),
        [
            ("left", ["right"]),
            ("right", ["left"]),
            ("top", ["bottom"]),
            ("bottom", ["top"]),
            ("centre", ["left", "right"]),
        ],
    )
    def test_the_picture_starts_covered_from_the_far_side(
        self, render, edge, covered
    ) -> None:
        html = render(f'<c-reveal.wipe from="{edge}"><b>inside</b></c-reveal.wipe>')

        assert re.findall(r"\[--wipe-(\w+):", html) == covered

    def test_an_unrecognised_edge_falls_back_to_the_left(self, render) -> None:
        html = render('<c-reveal.wipe from="corner"><b>inside</b></c-reveal.wipe>')

        assert re.findall(r"\[--wipe-(\w+):", html) == ["right"]

    def test_the_frame_clips_the_zoomed_picture(self, render) -> None:
        # `clip-path` hides what is outside the frame without stopping it widening the page.
        html = render("<c-reveal.wipe><b>inside</b></c-reveal.wipe>")

        assert re.match(r'\s*<div class="[^"]*\boverflow-clip\b', html) is not None


class TestWords:
    def test_each_word_is_its_own_numbered_element(self, render) -> None:
        html = render('<c-reveal.words text="Ship on a Friday" />')

        assert re.findall(r'style="--i: (\d+)">([^<]*)</span>', html) == [
            ("0", "Ship"),
            ("1", "on"),
            ("2", "a"),
            ("3", "Friday"),
        ]

    def test_the_paragraph_is_told_how_many_words_it_holds(self, render) -> None:
        html = render('<c-reveal.words text="Ship on a Friday" />')

        assert declared(html, "--words-n") == 4

    def test_the_words_still_read_as_a_sentence(self, render) -> None:
        html = render('<c-reveal.words text="Ship on a Friday" />')

        assert re.sub(r"<[^>]+>", "", html).split() == ["Ship", "on", "a", "Friday"]
        assert "</span> <span" in html

    def test_runs_of_whitespace_do_not_make_empty_words(self, render) -> None:
        html = render('<c-reveal.words text="  Ship   on\n a  Friday " />')

        assert html.count("<span") == 4

    def test_the_words_share_the_paragraphs_timeline(self, render) -> None:
        html = render('<c-reveal.words text="Ship" />')

        assert re.match(r'\s*<p class="dce:\[view-timeline-name:--words\]', html)
        assert "[animation-timeline:--words]" in html

    def test_markup_in_the_text_is_escaped(self, render) -> None:
        html = render(
            '<c-reveal.words text="{{ text }}" />',
            text="<script>alert(1)</script> now",
        )

        assert "<script>" not in html
        assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html

    def test_text_handed_over_as_an_object_is_escaped_too(self, render) -> None:
        html = render(
            '<c-reveal.words :text="text" />', text="<script>alert(1)</script> now"
        )

        assert "<script>" not in html
        assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html

    def test_an_ampersand_is_escaped_once(self, render) -> None:
        html = render('<c-reveal.words text="{{ text }}" />', text="Fish & chips")

        assert ">&amp;</span>" in html

    @pytest.mark.parametrize("text", ["", "   "])
    def test_text_with_no_words_in_it_renders_none(self, render, text) -> None:
        html = render(f'<c-reveal.words text="{text}" />')

        assert "<span" not in html
        assert declared(html, "--words-n") == 0


class TestHover:
    def test_the_caption_is_rendered_alongside_what_is_always_showing(
        self, render
    ) -> None:
        html = render(
            "<c-reveal.hover><b>inside</b>"
            '<c-slot name="caption"><a href="/site/14/">Site 14</a></c-slot>'
            "</c-reveal.hover>"
        )

        assert html.index("<b>inside</b>") < html.index(
            '<a href="/site/14/">Site 14</a>'
        )

    def test_the_frame_takes_keyboard_focus(self, render) -> None:
        html = render("<c-reveal.hover><b>inside</b></c-reveal.hover>")

        assert re.match(r'\s*<div[^>]*\btabindex="0"', html) is not None

    def test_the_caption_opens_on_focus_as_well_as_on_hover(self, render) -> None:
        html = render("<c-reveal.hover><b>inside</b></c-reveal.hover>")

        on_hover = set(re.findall(r"(?<![\w:-])dce:group-hover:([\w-]+)", html))
        on_focus = set(re.findall(r"(?<![\w:-])dce:group-focus-within:([\w-]+)", html))
        assert on_hover
        assert on_hover == on_focus

    @pytest.mark.parametrize("effect", ["slide", "cover"])
    def test_the_caption_is_always_showing_where_there_is_no_hover(
        self, render, effect
    ) -> None:
        html = render(
            f'<c-reveal.hover effect="{effect}"><b>inside</b></c-reveal.hover>'
        )

        on_hover = set(re.findall(r"(?<![\w:-])dce:group-hover:([\w-]+)", html))
        without_hover = set(re.findall(r"\[@media\(hover:none\)\]:([\w-]+)", html))
        assert on_hover == without_hover

    def test_a_label_names_the_frame(self, render) -> None:
        html = render('<c-reveal.hover label="Site 14"><b>inside</b></c-reveal.hover>')

        assert re.match(r'\s*<div[^>]*\baria-label="Site 14"', html) is not None

    def test_there_is_no_empty_name_without_a_label(self, render) -> None:
        html = render("<c-reveal.hover><b>inside</b></c-reveal.hover>")

        assert "aria-label" not in html

    def test_a_label_carrying_a_quote_cannot_break_out_of_the_attribute(
        self, render
    ) -> None:
        html = render(
            '<c-reveal.hover :label="label"><b>inside</b></c-reveal.hover>',
            label='Site" onfocus="alert(1)',
        )

        assert '" onfocus="' not in html

    def test_slide_and_cover_hide_the_caption_differently(self, render) -> None:
        slide = render('<c-reveal.hover effect="slide"><b>inside</b></c-reveal.hover>')
        cover = render('<c-reveal.hover effect="cover"><b>inside</b></c-reveal.hover>')

        assert "translate-y-full" in slide
        assert "translate-y-full" not in cover
        assert "opacity-0" in cover

    def test_an_unrecognised_effect_falls_back_to_slide(self, render) -> None:
        html = render('<c-reveal.hover effect="spin"><b>inside</b></c-reveal.hover>')

        assert "translate-y-full" in html


class TestStack:
    def test_every_panel_sticks(self, render) -> None:
        html = render("<c-reveal.stack><b>inside</b></c-reveal.stack>")

        assert re.search(r'class="[^"]*(?<!\S)dce:\*:sticky\b', html) is not None

    def test_each_of_the_first_twelve_panels_is_given_its_number(self, render) -> None:
        html = render("<c-reveal.stack><b>inside</b></c-reveal.stack>")

        numbered = re.findall(r"\*:nth-(\d+):\[--stack-i:(\d+)\]", html)
        assert [(int(nth), int(i)) for nth, i in numbered] == [
            (n, n - 1) for n in range(2, 13)
        ]

    def test_a_panel_stops_lower_by_its_number_of_steps(self, render) -> None:
        html = render("<c-reveal.stack><b>inside</b></c-reveal.stack>")

        assert "var(--stack-i,0)*var(--stack-step,0)" in html
