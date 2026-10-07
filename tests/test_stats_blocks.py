"""The stats family: figures, how they have moved, and sections to set them in.

Every single-figure stat is daisy-cotton's stat with something added, so it sits
in a stat group beside plain ones. That, and what each one tells a screen reader,
is the contract. Where a part sits within a layout is design and is not tested.
"""

import re

import pytest

TRENDS = [
    "c-stats.trend",
    "c-stats.trend-inline",
    "c-stats.trend-corner",
    "c-stats.trend-centred",
    "c-stats.trend-footer",
    "c-stats.trend-row",
]

# The trend layouts with room for a chart between their tags.
WITH_CHART = [
    "c-stats.trend",
    "c-stats.trend-inline",
    "c-stats.trend-corner",
    "c-stats.trend-footer",
]

# The stats that take a picture in place of the icon.
WITH_PICTURE = [
    "c-stats.trend",
    "c-stats.trend-inline",
    "c-stats.trend-centred",
    "c-stats.trend-footer",
    "c-stats.progress",
    "c-stats.count",
]

EVERY_STAT = [*TRENDS, "c-stats.progress", "c-stats.count"]

SECTIONS = ["c-stats.band", "c-stats.split", "c-stats.headline"]

# The icon the example project knows as "deploys".
ICON = "bi-rocket-takeoff"


def badge(html: str) -> str:
    """Return the change badge's opening tag."""
    found = re.search(r'<\w+ class="badge\b[^>]*>', html)
    assert found is not None, "no change badge was rendered"
    return found.group(0)


class TestEveryStatIsAStat:
    @pytest.mark.parametrize("tag", EVERY_STAT)
    def test_it_is_a_daisy_cotton_stat(self, render, tag) -> None:
        html = render(f'<{tag} title="Deploys" value="31" to="31" />')

        assert re.match(r'\s*<div class="stat\b', html) is not None

    @pytest.mark.parametrize("tag", EVERY_STAT)
    def test_extra_classes_reach_the_outer_element(self, render, tag) -> None:
        html = render(f'<{tag} value="31" class="rounded-3xl" />')

        assert re.match(r'\s*<div class="[^"]*\brounded-3xl\b', html) is not None

    @pytest.mark.parametrize("tag", EVERY_STAT)
    def test_an_undeclared_attribute_reaches_the_outer_element(
        self, render, tag
    ) -> None:
        html = render(f'<{tag} value="31" id="deploys" />')

        assert re.match(r'\s*<div[^>]*\bid="deploys"', html) is not None

    @pytest.mark.parametrize("tag", [*TRENDS, "c-stats.progress"])
    def test_a_figure_of_nought_is_shown(self, render, tag) -> None:
        html = render(f'<{tag} value="0" />')

        assert re.search(r"stat-value.*>0<", html, re.DOTALL)

    @pytest.mark.parametrize("tag", [*TRENDS, "c-stats.progress"])
    @pytest.mark.parametrize("given", ["title", "value", "desc"])
    def test_what_the_page_author_writes_is_escaped(self, render, tag, given) -> None:
        html = render(f'<{tag} :{given}="text" />', text="<script>x</script>")

        assert "<script>" not in html
        assert "&lt;script&gt;" in html


class TestTrend:
    @pytest.mark.parametrize("tag", TRENDS)
    def test_every_layout_shows_the_same_parts(self, render, tag) -> None:
        html = render(
            f'<{tag} title="Deploys a day" value="31" change="12%" '
            'desc="since last month" />'
        )

        for part in ("Deploys a day", "31", "12%", "since last month"):
            assert part in html

    @pytest.mark.parametrize("tag", TRENDS)
    def test_no_change_means_no_badge(self, render, tag) -> None:
        html = render(f'<{tag} title="Services" value="14" desc="in production" />')

        assert "badge" not in html
        assert "sr-only" not in html

    @pytest.mark.parametrize("tag", TRENDS)
    def test_the_change_is_escaped(self, render, tag) -> None:
        html = render(f'<{tag} value="31" :change="text" />', text="<b>12</b>")

        assert "<b>12</b>" not in html


class TestChange:
    @pytest.mark.parametrize(
        ("direction", "spoken"),
        [("up", "Up"), ("down", "Down"), ("flat", "No change")],
    )
    def test_the_direction_is_said_in_words_a_screen_reader_reads(
        self, render, direction, spoken
    ) -> None:
        html = render(f'<c-stats.change change="4" direction="{direction}" />')

        assert re.search(rf'<span class="dce:sr-only">{spoken}</span>', html)

    def test_a_change_with_no_direction_given_is_a_rise(self, render) -> None:
        html = render('<c-stats.change change="4" />')

        assert '<span class="dce:sr-only">Up</span>' in html

    def test_the_arrow_is_hidden_from_a_screen_reader(self, render) -> None:
        html = render('<c-stats.change change="4" />')

        assert re.search(r'<svg[^>]*aria-hidden="true"', html)

    @pytest.mark.parametrize(
        ("attributes", "marked"),
        [
            ('direction="up"', "badge-success"),
            ('direction="down"', "badge-error"),
            ('direction="down" inverse', "badge-success"),
            ('direction="up" inverse', "badge-error"),
            ('direction="flat"', "badge-neutral"),
            ('direction="flat" inverse', "badge-neutral"),
        ],
    )
    def test_whether_a_move_is_welcome_is_the_page_authors_to_say(
        self, render, attributes, marked
    ) -> None:
        html = render(f'<c-stats.change change="4" {attributes} />')

        assert marked in badge(html)

    @pytest.mark.parametrize("tag", TRENDS)
    def test_a_trend_states_its_move_the_way_the_badge_does(self, render, tag) -> None:
        html = render(f'<{tag} value="18m" change="26m" direction="down" inverse />')

        assert "badge-success" in badge(html)
        assert '<span class="dce:sr-only">Down</span>' in html

    def test_extra_classes_reach_the_badge(self, render) -> None:
        html = render('<c-stats.change change="4" class="ms-2" />')

        assert "ms-2" in badge(html)


class TestIcon:
    @pytest.mark.parametrize("tag", EVERY_STAT)
    def test_a_named_icon_is_drawn_by_the_projects_icon_component(
        self, render, tag
    ) -> None:
        html = render(f'<{tag} value="31" icon="deploys" />')

        assert ICON in html

    @pytest.mark.parametrize("tag", [*EVERY_STAT, "c-stats.headline"])
    def test_the_icon_is_hidden_from_a_screen_reader(self, render, tag) -> None:
        html = render(f'<{tag} value="31" icon="deploys" />')

        assert re.search(rf'<i[^>]*{ICON}[^>]*aria-hidden="true"', html)

    @pytest.mark.parametrize("tag", [*EVERY_STAT, "c-stats.headline"])
    def test_no_icon_is_drawn_unless_one_is_named(self, render, tag) -> None:
        html = render(f'<{tag} title="Deploys" value="31" />')

        assert "<i " not in html
        assert "stat-figure" not in html

    @pytest.mark.parametrize("tag", [*WITH_PICTURE, "c-stats.headline"])
    def test_a_picture_takes_the_place_of_the_icon(self, render, tag) -> None:
        html = render(
            f'<{tag} value="31" icon="deploys">'
            '<c-slot name="figure"><img src="north.png" alt="" /></c-slot>'
            f"</{tag}>"
        )

        assert 'src="north.png"' in html
        assert ICON not in html


class TestRoomForAChart:
    @pytest.mark.parametrize("tag", WITH_CHART)
    def test_what_goes_between_the_tags_is_placed_in_the_stat(
        self, render, tag
    ) -> None:
        html = render(f'<{tag} value="31"><canvas id="run"></canvas></{tag}>')

        assert re.search(
            r'<div class="stat\b.*<canvas id="run">.*</div>\s*$', html, re.S
        )

    @pytest.mark.parametrize("tag", WITH_CHART)
    def test_nothing_between_the_tags_leaves_no_room(self, render, tag) -> None:
        bare = render(f'<{tag} value="31" desc="since May" />')
        spaced = render(f'<{tag} value="31" desc="since May">\n   \n</{tag}>')

        assert spaced.split() == bare.split()


class TestProgress:
    def test_the_bar_is_a_progress_element_out_of_a_hundred(self, render) -> None:
        html = render('<c-stats.progress title="Raised" value="€42k" percent="70" />')

        assert re.search(r'<progress[^>]*value="70"[^>]*max="100"', html)

    def test_the_bar_is_named_by_the_title(self, render) -> None:
        html = render('<c-stats.progress title="Raised" value="€42k" percent="70" />')

        assert re.search(r'<progress[^>]*aria-label="Raised"', html)

    def test_a_bar_with_no_title_is_named_by_the_description(self, render) -> None:
        html = render('<c-stats.progress value="12" percent="50" desc="of 24 seats" />')

        assert re.search(r'<progress[^>]*aria-label="of 24 seats"', html)

    def test_the_percentage_is_written_out_as_well(self, render) -> None:
        html = render('<c-stats.progress value="€42k" percent="70" />')

        assert ">70%<" in html

    def test_a_part_percentage_reaches_the_bar_unrounded(self, render) -> None:
        html = render('<c-stats.progress value="3 of 8" percent="37.5" />')

        assert 'value="37.5' in html

    def test_a_number_passed_as_a_number_counts_the_same(self, render) -> None:
        html = render('<c-stats.progress value="x" :percent="share" />', share=70)

        assert 'value="70"' in html

    def test_more_than_the_whole_is_passed_on_as_given(self, render) -> None:
        html = render('<c-stats.progress value="13,800" percent="138" />')

        assert 'value="138"' in html
        assert ">138%<" in html

    @pytest.mark.parametrize("percent", ["", "most", '70" onfocus="x'])
    def test_nothing_but_a_number_reaches_the_bar(self, render, percent) -> None:
        html = render('<c-stats.progress value="x" :percent="share" />', share=percent)

        assert re.search(r'<progress[^>]*value="0"', html)
        assert "onfocus" not in html

    def test_the_bar_is_primary_unless_told_otherwise(self, render) -> None:
        html = render('<c-stats.progress value="x" percent="70" />')

        assert "progress-primary" in html

    def test_the_variant_is_the_colour_of_the_bar(self, render) -> None:
        html = render('<c-stats.progress value="x" percent="94" variant="warning" />')

        assert "progress-warning" in html
        assert "progress-primary" not in html


class TestCount:
    def test_the_finished_number_is_there_to_be_read(self, render) -> None:
        html = render('<c-stats.count to="31" />')

        assert re.search(r"<span[^>]*sr-only[^>]*>31</span>", html)

    def test_the_counting_figure_is_hidden_from_a_screen_reader(self, render) -> None:
        html = render('<c-stats.count to="31" />')

        assert re.search(r'<span aria-hidden="true"[^>]*--count-to: 31;', html, re.S)

    def test_what_is_written_before_and_after_goes_round_the_number(
        self, render
    ) -> None:
        html = render('<c-stats.count to="48" prefix="€" suffix="k" />')

        assert re.search(r"€<span[^>]*>48</span><span[^>]*></span>k", html, re.S)

    def test_a_number_that_is_not_whole_is_rounded(self, render) -> None:
        html = render('<c-stats.count to="1.3" />')

        assert "--count-to: 1;" in html
        assert ">1</span>" in html

    @pytest.mark.parametrize("to", ["", "many", "31; color: red"])
    def test_nothing_but_a_number_is_counted_to(self, render, to) -> None:
        html = render('<c-stats.count :to="to" />', to=to)

        assert "--count-to: 0;" in html
        assert "color: red" not in html

    def test_how_long_the_count_takes_is_passed_on(self, render) -> None:
        html = render('<c-stats.count to="31" time="0.6" />')

        assert "--count-time: 0.6" in html

    def test_a_time_that_is_no_number_falls_back_to_two_seconds(self, render) -> None:
        html = render('<c-stats.count to="31" :time="time" />', time="2s; x: y")

        assert "--count-time: 2" in html
        assert "x: y" not in html

    def test_nothing_counts_for_anyone_who_asked_for_less_motion(self, render) -> None:
        html = render('<c-stats.count to="31" />')

        moving = re.findall(r"[\w:\[\]()-]*(?:animate-|transition:)[^\s\"]*", html)
        assert moving
        assert all(name.startswith("dce:motion-safe:") for name in moving)


class TestSections:
    @pytest.mark.parametrize("tag", SECTIONS)
    def test_it_is_a_section(self, render, tag) -> None:
        html = render(f'<{tag} value="99%" id="numbers"></{tag}>')

        assert re.match(r'\s*<section[^>]*\bid="numbers"', html) is not None

    @pytest.mark.parametrize("tag", SECTIONS)
    def test_extra_classes_reach_the_section(self, render, tag) -> None:
        html = render(f'<{tag} value="99%" class="bg-base-200"></{tag}>')

        assert re.match(r'\s*<section class="[^"]*\bbg-base-200\b', html) is not None

    @pytest.mark.parametrize("tag", SECTIONS)
    def test_the_title_is_a_second_level_heading_by_default(self, render, tag) -> None:
        html = render(f'<{tag} value="99%" title="In numbers"></{tag}>')

        assert re.search(r"<h2\b.*In numbers.*</h2>", html, re.S)

    @pytest.mark.parametrize("tag", SECTIONS)
    def test_the_heading_level_is_the_page_authors_to_set(self, render, tag) -> None:
        html = render(f'<{tag} value="99%" title="In numbers" level="3"></{tag}>')

        assert re.search(r"<h3\b.*In numbers.*</h3>", html, re.S)
        assert "<h2" not in html

    @pytest.mark.parametrize("tag", ["c-stats.band", "c-stats.split"])
    def test_a_section_with_no_title_has_no_heading(self, render, tag) -> None:
        html = render(f'<{tag}><c-stat value="14" /></{tag}>')

        assert not re.search(r"<h[1-6]\b", html)

    @pytest.mark.parametrize("tag", ["c-stats.band", "c-stats.split"])
    def test_the_figures_come_after_the_copy(self, render, tag) -> None:
        html = render(
            f'<{tag} title="In numbers" lead="Last month.">'
            '<c-stats.trend value="31" id="figure" /></'
            f"{tag}>"
        )

        assert html.index("Last month.") < html.index('id="figure"')

    @pytest.mark.parametrize("tag", ["c-stats.split", "c-stats.headline"])
    def test_actions_come_after_the_copy(self, render, tag) -> None:
        html = render(
            f'<{tag} value="99%" title="In numbers">'
            '<c-slot name="actions"><a href="/report/">Report</a></c-slot>'
            f"</{tag}>"
        )

        assert html.index("In numbers") < html.index('href="/report/"')


class TestBand:
    def test_a_background_goes_in_a_layer_a_screen_reader_skips(self, render) -> None:
        html = render(
            "<c-stats.band>"
            '<c-slot name="background"><i id="layer"></i></c-slot>'
            '<c-stat value="14" /></c-stats.band>'
        )

        assert re.search(r'<div aria-hidden="true"[^>]*>\s*<i id="layer">', html)

    def test_no_background_layer_without_a_background(self, render) -> None:
        html = render('<c-stats.band><c-stat value="14" /></c-stats.band>')

        assert "aria-hidden" not in html

    def test_nothing_moves_unless_asked(self, render) -> None:
        html = render('<c-stats.band><c-stat value="14" /></c-stats.band>')

        assert "animate-" not in html

    def test_the_figures_can_arrive_one_after_another(self, render) -> None:
        html = render('<c-stats.band cascade><c-stat value="14" /></c-stats.band>')

        assert "dce-reveal" in html

    def test_inverted_copy_takes_the_colour_paired_with_a_dark_surface(
        self, render
    ) -> None:
        html = render(
            '<c-stats.band invert title="A year" lead="In numbers."></c-stats.band>'
        )

        assert "text-neutral-content" in html
        assert "text-base-content" not in html


class TestHeadline:
    def test_the_figure_and_its_title_are_one_heading(self, render) -> None:
        html = render('<c-stats.headline value="99.98%" title="Uptime" />')

        assert re.search(r"<h2\b.*99\.98%.*Uptime.*</h2>", html, re.S)

    def test_the_figure_alone_is_still_the_heading(self, render) -> None:
        html = render('<c-stats.headline value="41" />')

        assert re.search(r"<h2\b.*41.*</h2>", html, re.S)

    def test_the_colours_hold_still_unless_given_a_speed(self, render) -> None:
        html = render('<c-stats.headline value="41" />')

        assert "animate-" not in html

    def test_a_speed_sets_the_colours_moving(self, render) -> None:
        html = render('<c-stats.headline value="41" speed="1" />')

        assert "dce-text-slide" in html

    def test_the_figure_is_escaped(self, render) -> None:
        html = render('<c-stats.headline :value="text" />', text="<b>41</b>")

        assert "<b>41</b>" not in html
