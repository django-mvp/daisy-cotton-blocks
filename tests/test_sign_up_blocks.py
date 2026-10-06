"""The sign-up family: four layouts for the page that takes somebody on.

As with sign-in, each block owns the frame and takes the logo, the form and the
provider buttons as slots. A sign-up page also argues its case, so three of the
four have somewhere to put it, and the order that case is read in beside the
form is part of what is tested.
"""

import re

import pytest

EVERY_SIGN_UP = [
    "c-sign-up.pitch",
    "c-sign-up.showcase",
    "c-sign-up.bento",
    "c-sign-up.stepped",
]

# The layouts with a bar across the top holding the logo and the way across.
WITH_A_BAR = ["c-sign-up.pitch", "c-sign-up.showcase", "c-sign-up.bento"]

FORM = '<form id="the-form"></form>'


def page(tag: str, attributes: str = "", slots: str = "", form: str = FORM) -> str:
    """Return markup for a sign-up block holding a form and any named slots."""
    return f"<{tag} {attributes}>{slots}{form}</{tag}>"


def slot(name: str, content: str) -> str:
    """Return a named slot."""
    return f'<c-slot name="{name}">{content}</c-slot>'


class TestEverySignUpPage:
    @pytest.mark.parametrize("tag", EVERY_SIGN_UP)
    def test_the_form_is_rendered(self, render, tag) -> None:
        html = render(page(tag))

        assert html.count('<form id="the-form">') == 1

    @pytest.mark.parametrize("tag", EVERY_SIGN_UP)
    def test_the_logo_is_rendered_once(self, render, tag) -> None:
        html = render(page(tag, slots=slot("logo", '<img id="logo" alt="Acme">')))

        assert html.count('<img id="logo" alt="Acme">') == 1

    @pytest.mark.parametrize("tag", EVERY_SIGN_UP)
    def test_the_page_has_one_first_level_heading(self, render, tag) -> None:
        html = render(page(tag, 'title="Join" headline="Know what shipped"'))

        assert len(re.findall(r"<h1\b", html)) == 1

    @pytest.mark.parametrize("tag", EVERY_SIGN_UP)
    def test_a_page_given_no_words_has_no_empty_heading(self, render, tag) -> None:
        html = render(page(tag))

        assert re.search(r"<h\d\b", html) is None

    @pytest.mark.parametrize("tag", EVERY_SIGN_UP)
    def test_the_buttons_and_the_form_are_separated_without_being_told_how(
        self, render, tag
    ) -> None:
        html = render(page(tag, slots=slot("providers", "<a>Google</a>")))

        assert re.search(r'class="divider[^"]*"[^>]*>\s*\S', html)

    @pytest.mark.parametrize("tag", EVERY_SIGN_UP)
    def test_the_provider_buttons_come_before_the_form(self, render, tag) -> None:
        html = render(page(tag, slots=slot("providers", '<a id="google">Google</a>')))

        assert html.index('id="google"') < html.index('id="the-form"')

    @pytest.mark.parametrize("tag", EVERY_SIGN_UP)
    def test_a_word_separates_the_buttons_from_the_form(self, render, tag) -> None:
        html = render(
            page(tag, 'divider="otherwise"', slot("providers", "<a>Google</a>"))
        )

        assert re.search(r'class="divider[^"]*"[^>]*>\s*otherwise\s*<', html)

    @pytest.mark.parametrize("tag", EVERY_SIGN_UP)
    def test_no_divider_without_provider_buttons(self, render, tag) -> None:
        html = render(page(tag, 'divider="otherwise"'))

        assert "otherwise" not in html

    @pytest.mark.parametrize("tag", EVERY_SIGN_UP)
    def test_the_foot_follows_the_form(self, render, tag) -> None:
        html = render(page(tag, slots=slot("footer", '<a id="terms">Terms</a>')))

        assert html.index('id="the-form"') < html.index('id="terms"')

    @pytest.mark.parametrize("tag", EVERY_SIGN_UP)
    def test_extra_classes_reach_the_outer_element(self, render, tag) -> None:
        html = render(page(tag, 'class="bg-base-200"'))

        assert re.match(r'\s*<section[^>]*class="[^"]*\bbg-base-200\b', html)

    @pytest.mark.parametrize("tag", EVERY_SIGN_UP)
    def test_an_undeclared_attribute_reaches_the_outer_element(
        self, render, tag
    ) -> None:
        html = render(page(tag, 'id="entrance"'))

        assert re.match(r'\s*<section[^>]*\bid="entrance"', html)

    @pytest.mark.parametrize("tag", EVERY_SIGN_UP)
    def test_a_background_goes_in_a_layer_a_screen_reader_skips(
        self, render, tag
    ) -> None:
        html = render(page(tag, slots=slot("background", '<i id="backdrop"></i>')))

        assert re.search(
            r'<div aria-hidden="true"[^>]*>\s*<i id="backdrop"></i>\s*</div>', html
        )


class TestTopBar:
    @pytest.mark.parametrize("tag", WITH_A_BAR)
    def test_the_way_across_follows_the_logo_and_precedes_the_form(
        self, render, tag
    ) -> None:
        html = render(
            page(
                tag,
                slots=slot("logo", '<img id="logo" alt="">')
                + slot("nav", '<a id="across">Sign in</a>'),
            )
        )

        assert (
            html.index('id="logo"')
            < html.index('id="across"')
            < html.index('id="the-form"')
        )


class TestPitch:
    def test_the_case_is_the_heading_and_the_form_sits_a_level_below(
        self, render
    ) -> None:
        html = render(
            page("c-sign-up.pitch", 'headline="Know what shipped" title="Join"')
        )

        assert re.search(r"<h1[^>]*>\s*Know what shipped\s*</h1>", html)
        assert re.search(r"<h2[^>]*>\s*Join\s*</h2>", html)

    def test_the_form_heading_follows_the_headline_down_a_level(self, render) -> None:
        html = render(
            page("c-sign-up.pitch", 'level="2" headline="Know what shipped" title="J"')
        )

        assert re.search(r"<h2[^>]*>\s*Know what shipped\s*</h2>", html)
        assert re.search(r"<h3[^>]*>\s*J\s*</h3>", html)

    def test_the_page_reads_headline_then_form_then_the_rest_of_the_case(
        self, render
    ) -> None:
        html = render(
            page(
                "c-sign-up.pitch",
                'headline="Know what shipped"',
                slot("points", '<ul id="points"></ul>'),
            )
        )

        assert (
            html.index("Know what shipped")
            < html.index('id="the-form"')
            < html.index('id="points"')
        )


class TestShowcase:
    def test_the_picture_is_hidden_from_a_screen_reader(self, render) -> None:
        html = render(
            page("c-sign-up.showcase", slots=slot("media", '<img id="shot" alt="">'))
        )

        assert re.search(
            r'<div aria-hidden="true"[^>]*>\s*<img id="shot" alt="">\s*</div>', html
        )

    def test_the_line_above_the_picture_is_not_a_second_heading(self, render) -> None:
        html = render(page("c-sign-up.showcase", 'title="Join" caption="What you get"'))

        assert re.search(r"<p[^>]*>\s*What you get\s*</p>", html)
        assert len(re.findall(r"<h\d\b", html)) == 1

    def test_the_pane_takes_the_surface_it_is_given(self, render) -> None:
        html = render(page("c-sign-up.showcase", 'surface="bg-accent"'))

        assert "bg-accent" in html
        assert "bg-base-200" not in html


class TestBento:
    def test_the_tiles_follow_the_form(self, render) -> None:
        html = render(
            page("c-sign-up.bento", slots=slot("tiles", '<div id="tile"></div>'))
        )

        assert html.index('id="the-form"') < html.index('id="tile"')

    def test_each_tile_is_a_cell_of_the_same_grid_as_the_form(self, render) -> None:
        html = render(
            page("c-sign-up.bento", slots=slot("tiles", '<div id="tile"></div>'))
        )

        assert re.search(
            r'</div>\s*</div>\s*<div id="tile"></div>\s*</div>\s*</section>', html
        )


class TestStepped:
    def test_the_run_of_steps_sits_between_the_logo_and_the_form(self, render) -> None:
        html = render(
            page(
                "c-sign-up.stepped",
                slots=slot("logo", '<img id="logo" alt="">')
                + slot("steps", '<ol id="steps"></ol>'),
            )
        )

        assert (
            html.index('id="logo"')
            < html.index('id="steps"')
            < html.index('id="the-form"')
        )
