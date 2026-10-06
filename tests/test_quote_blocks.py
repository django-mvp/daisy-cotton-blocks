"""The quote family: what somebody said, and who said it.

Every quote is a `figure` holding a `blockquote` and, when there is anybody to
name, a caption. That structure is the contract: it is what a screen reader
announces and what a host's own CSS is written against. The caption comes from
one component, `c-quote.byline`, which the other seven share.
"""

import re

import pytest

# The quotes that take the person's details and write the caption themselves.
ATTRIBUTED = [
    "c-quote.pull",
    "c-quote.mark",
    "c-quote.card",
    "c-quote.bubble",
    "c-quote.centred",
    "c-quote.split",
]

# The attributed quotes that show a small portrait beside the name.
WITH_PORTRAIT = [tag for tag in ATTRIBUTED if tag != "c-quote.split"]

# Where each coloured quote puts its colour.
VARIANTS = [
    ("c-quote.pull", "border-secondary"),
    ("c-quote.mark", "text-secondary"),
    ("c-quote.card", "text-secondary"),
    ("c-quote.bubble", "bg-secondary"),
]

EVERY_QUOTE = [*ATTRIBUTED, "c-quote.wall", "c-quote.byline"]


def quote(tag: str, attributes: str = "") -> str:
    """Return markup for a quote, giving the one with nothing inside it a name."""
    if tag == "c-quote.byline":
        return f'<{tag} name="Mei Tanaka" {attributes} />'
    return f"<{tag} {attributes}><b>inside</b></{tag}>"


class TestEveryQuoteIsAFigure:
    @pytest.mark.parametrize("tag", ATTRIBUTED)
    def test_what_was_said_is_a_blockquote_inside_a_figure(self, render, tag) -> None:
        html = render(quote(tag))

        assert re.search(
            r"<figure\b.*<blockquote\b[^>]*>\s*<b>inside</b>\s*.*</blockquote>"
            r".*</figure>",
            html,
            re.DOTALL,
        )

    @pytest.mark.parametrize("tag", EVERY_QUOTE)
    def test_extra_classes_reach_the_outer_element(self, render, tag) -> None:
        html = render(quote(tag, 'class="rounded-3xl"'))

        assert re.match(r'\s*<\w+[^>]*class="[^"]*\brounded-3xl\b', html) is not None

    @pytest.mark.parametrize("tag", EVERY_QUOTE)
    def test_an_undeclared_attribute_reaches_the_outer_element(
        self, render, tag
    ) -> None:
        html = render(quote(tag, 'id="praise"'))

        assert re.match(r'\s*<\w+[^>]*\bid="praise"', html) is not None


class TestTheCaption:
    @pytest.mark.parametrize("tag", ATTRIBUTED)
    def test_a_quote_from_nobody_has_no_caption(self, render, tag) -> None:
        html = render(quote(tag))

        assert "<figcaption" not in html

    @pytest.mark.parametrize("tag", ATTRIBUTED)
    @pytest.mark.parametrize("given", ["name", "role", "source"])
    def test_any_one_detail_is_enough_for_a_caption(self, render, tag, given) -> None:
        html = render(quote(tag, f'{given}="Harbour Bank"'))

        assert re.search(
            r"</blockquote>.*<figcaption\b.*Harbour Bank.*</figcaption>\s*</figure>",
            html,
            re.DOTALL,
        )

    @pytest.mark.parametrize("tag", ATTRIBUTED)
    def test_the_persons_details_are_escaped(self, render, tag) -> None:
        html = render(
            quote(tag, 'name="{{ name }}" role="{{ role }}" source="{{ source }}"'),
            name="<script>n</script>",
            role="<script>r</script>",
            source="<script>s</script>",
        )

        assert "<script>" not in html
        assert html.count("&lt;script&gt;") == 3

    def test_the_work_is_a_citation_and_the_person_is_not(self, render) -> None:
        html = render('<c-quote.byline name="Mei Tanaka" source="Field Notes" />')

        assert re.search(r"<cite\b[^>]*>Field Notes</cite>", html)
        assert not re.search(r"<cite\b[^>]*>[^<]*Mei Tanaka", html)

    def test_a_work_with_an_address_links_to_it(self, render) -> None:
        html = render(
            '<c-quote.byline source="Field Notes" href="https://example.com/notes" />'
        )

        assert re.search(
            r'<cite\b[^>]*><a\b[^>]*href="https://example.com/notes"[^>]*>'
            r"Field Notes</a></cite>",
            html,
        )

    def test_a_work_with_no_address_is_not_a_link(self, render) -> None:
        html = render('<c-quote.byline source="Field Notes" />')

        assert "<a" not in html

    @pytest.mark.parametrize("tag", ATTRIBUTED)
    def test_the_address_is_recorded_on_the_quotation(self, render, tag) -> None:
        html = render(quote(tag, 'source="Notes" href="https://example.com/notes"'))

        assert re.search(r'<blockquote\b[^>]*cite="https://example.com/notes"', html)

    @pytest.mark.parametrize("tag", ATTRIBUTED)
    def test_a_quotation_with_no_address_claims_none(self, render, tag) -> None:
        html = render(quote(tag, 'name="Mei Tanaka"'))

        assert not re.search(r"<blockquote\b[^>]*\bcite=", html)


class TestThePortrait:
    @pytest.mark.parametrize("tag", [*WITH_PORTRAIT, "c-quote.byline"])
    def test_a_portrait_is_shown_in_an_avatar(self, render, tag) -> None:
        html = render(quote(tag, 'name="Mei Tanaka" src="/people/mei.jpg"'))

        assert re.search(
            r'<div class="avatar\b[^"]*"[^>]*>\s*<div[^>]*>\s*'
            r'<img\b[^>]*src="/people/mei.jpg"',
            html,
        )

    @pytest.mark.parametrize("tag", [*WITH_PORTRAIT, "c-quote.byline"])
    def test_the_portrait_says_nothing_the_name_beside_it_does_not(
        self, render, tag
    ) -> None:
        html = render(quote(tag, 'name="Mei Tanaka" src="/people/mei.jpg"'))

        assert re.search(r'<img\b[^>]*\balt=""', html)

    @pytest.mark.parametrize("tag", [*WITH_PORTRAIT, "c-quote.byline"])
    def test_nobody_is_drawn_when_there_is_no_portrait(self, render, tag) -> None:
        html = render(quote(tag, 'name="Mei Tanaka"'))

        assert "avatar" not in html
        assert "<img" not in html

    @pytest.mark.parametrize("tag", [*WITH_PORTRAIT, "c-quote.byline"])
    def test_classes_meant_for_the_quote_stay_off_the_avatar(self, render, tag) -> None:
        html = render(
            quote(tag, 'name="Mei Tanaka" src="/people/mei.jpg" class="rounded-3xl"')
        )

        avatar = re.search(r'<div class="(avatar\b[^"]*)"', html)
        assert avatar is not None
        assert "rounded-3xl" not in avatar.group(1)


class TestVariant:
    @pytest.mark.parametrize(("tag", "painted"), VARIANTS)
    def test_the_variant_is_the_colour_it_is_drawn_in(
        self, render, tag, painted
    ) -> None:
        html = render(quote(tag, 'variant="secondary" rating="3"'))

        assert painted in html

    def test_words_in_a_coloured_bubble_take_the_colour_paired_with_it(
        self, render
    ) -> None:
        html = render(quote("c-quote.bubble", 'variant="primary"'))

        assert "text-primary-content" in html

    @pytest.mark.parametrize("surface", ["base-100", "base-200", "base-300"])
    def test_words_in_a_surface_bubble_keep_the_page_colour(
        self, render, surface
    ) -> None:
        html = render(quote("c-quote.bubble", f'variant="{surface}"'))

        assert f"bg-{surface}" in html
        assert "text-base-content" in html
        assert f"text-{surface}-content" not in html


class TestCardRating:
    @pytest.mark.parametrize("rating", ["1", "2", "3", "4", "5"])
    def test_the_stars_are_read_out_as_one_score(self, render, rating) -> None:
        html = render(quote("c-quote.card", f'rating="{rating}"'))

        assert re.search(rf'role="img"[^>]*aria-label="{rating} out of 5"', html)

    @pytest.mark.parametrize("rating", ["1", "2", "3", "4", "5"])
    def test_as_many_stars_are_filled_as_were_given(self, render, rating) -> None:
        html = render(quote("c-quote.card", f'rating="{rating}" variant="neutral"'))

        assert html.count("text-neutral") == int(rating)
        assert html.count("&#9733;") == 5

    def test_a_number_passed_as_a_number_counts_the_same(self, render) -> None:
        html = render(
            quote("c-quote.card", ':rating="score" variant="neutral"'), score=4
        )

        assert html.count("text-neutral") == 4

    def test_no_rating_means_no_stars(self, render) -> None:
        html = render(quote("c-quote.card"))

        assert 'role="img"' not in html
        assert "&#9733;" not in html

    @pytest.mark.parametrize("rating", ["0", "6", "12", "4.5", "plenty", "-1"])
    def test_a_rating_off_the_scale_shows_no_stars(self, render, rating) -> None:
        html = render(quote("c-quote.card", f'rating="{rating}"'))

        assert 'role="img"' not in html
        assert "&#9733;" not in html

    def test_each_star_is_hidden_from_a_screen_reader(self, render) -> None:
        html = render(quote("c-quote.card", 'rating="3"'))

        assert len(re.findall(r'<span aria-hidden="true"[^>]*>&#9733;', html)) == 5


class TestDecoration:
    def test_the_oversized_mark_is_hidden_from_a_screen_reader(self, render) -> None:
        html = render(quote("c-quote.mark"))

        assert re.search(r'<span aria-hidden="true"[^>]*>&ldquo;</span>', html)

    def test_the_tail_of_the_bubble_is_hidden_from_a_screen_reader(
        self, render
    ) -> None:
        html = render(quote("c-quote.bubble"))

        assert re.search(r'<span aria-hidden="true"[^>]*></span>\s*</blockquote>', html)


class TestBlocks:
    @pytest.mark.parametrize("tag", ["c-quote.centred", "c-quote.split"])
    def test_a_background_goes_in_a_layer_a_screen_reader_skips(
        self, render, tag
    ) -> None:
        html = render(
            f'<{tag}>said<c-slot name="background"><i>sky</i></c-slot></{tag}>'
        )

        assert re.search(r'<div aria-hidden="true"[^>]*>\s*<i>sky</i>\s*</div>', html)

    @pytest.mark.parametrize("tag", ["c-quote.centred", "c-quote.split"])
    def test_no_background_layer_without_a_background(self, render, tag) -> None:
        html = render(quote(tag))

        assert 'aria-hidden="true"' not in html

    @pytest.mark.parametrize("tag", ["c-quote.centred", "c-quote.split"])
    def test_a_logo_sits_above_the_words(self, render, tag) -> None:
        html = render(f'<{tag}>said<c-slot name="logo"><i>mark</i></c-slot></{tag}>')

        assert html.index("<i>mark</i>") < html.index("<blockquote")

    def test_the_picture_beside_the_words_carries_its_description(self, render) -> None:
        html = render(
            '<c-quote.split src="/people/mei.jpg" alt="Mei at her desk">said'
            "</c-quote.split>"
        )

        assert re.search(
            r'<img\b[^>]*src="/people/mei.jpg"[^>]*alt="Mei at her desk"', html
        )

    def test_the_picture_sits_outside_the_figure(self, render) -> None:
        html = render('<c-quote.split src="/people/mei.jpg">said</c-quote.split>')

        assert html.index("<img") < html.index("<figure")

    def test_media_takes_the_place_of_the_picture(self, render) -> None:
        html = render(
            '<c-quote.split src="/people/mei.jpg">said'
            '<c-slot name="media"><video></video></c-slot></c-quote.split>'
        )

        assert "<video>" in html
        assert "<img" not in html

    def test_the_caption_beside_a_picture_has_no_portrait_of_its_own(
        self, render
    ) -> None:
        html = render(
            '<c-quote.split name="Mei Tanaka" src="/people/mei.jpg">said'
            "</c-quote.split>"
        )

        assert html.count("<img") == 1
        assert "avatar" not in html


class TestWall:
    def test_the_quotations_are_rendered(self, render) -> None:
        html = render("<c-quote.wall><b>inside</b></c-quote.wall>")

        assert "<b>inside</b>" in html

    def test_a_wall_with_no_title_has_no_heading(self, render) -> None:
        html = render('<c-quote.wall eyebrow="Praise" lead="From people who ship" />')

        assert not re.search(r"<h[1-6]\b", html)
        assert "Praise" not in html

    def test_the_title_is_a_second_level_heading_by_default(self, render) -> None:
        html = render('<c-quote.wall title="What people say" />')

        assert re.search(r"<h2\b[^>]*>What people say</h2>", html)

    def test_the_heading_level_is_the_page_authors_to_set(self, render) -> None:
        html = render('<c-quote.wall title="What people say" level="3" />')

        assert re.search(r"<h3\b[^>]*>What people say</h3>", html)

    @pytest.mark.parametrize("columns", ["2", "3", "4"])
    def test_the_column_count_applies_at_wide_widths(self, render, columns) -> None:
        html = render(f'<c-quote.wall columns="{columns}" />')

        assert f"lg:columns-{columns}" in html

    def test_no_quotation_is_split_across_two_columns(self, render) -> None:
        html = render("<c-quote.wall />")

        assert "*:break-inside-avoid" in html
