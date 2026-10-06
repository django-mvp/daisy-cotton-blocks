"""The sign-in family: five layouts for the page that lets somebody back in.

Each block owns the frame and nothing behind it. The logo, the form and the
buttons that skip the form arrive as slots, because they are the application's.
What is tested here is that each slot lands, that the parts with nothing in
them are left out, and that the page keeps one heading.
"""

import re

import pytest

EVERY_SIGN_IN = [
    "c-sign-in.centred",
    "c-sign-in.split",
    "c-sign-in.floating",
    "c-sign-in.stepped",
    "c-sign-in.providers",
]

WITH_A_BACKGROUND = EVERY_SIGN_IN

# The layouts with a pane or a strip of copy beside the form.
WITH_AN_ASIDE = ["c-sign-in.split", "c-sign-in.floating", "c-sign-in.providers"]

# The layouts that draw a word between the provider buttons and the form.
WITH_A_DIVIDER = [
    "c-sign-in.centred",
    "c-sign-in.split",
    "c-sign-in.floating",
    "c-sign-in.stepped",
]

FORM = '<form id="the-form"></form>'


def page(tag: str, attributes: str = "", slots: str = "", form: str = FORM) -> str:
    """Return markup for a sign-in block holding a form and any named slots."""
    return f"<{tag} {attributes}>{slots}{form}</{tag}>"


def slot(name: str, content: str) -> str:
    """Return a named slot."""
    return f'<c-slot name="{name}">{content}</c-slot>'


class TestEverySignInPage:
    @pytest.mark.parametrize("tag", EVERY_SIGN_IN)
    def test_the_form_is_rendered(self, render, tag) -> None:
        html = render(page(tag))

        assert html.count('<form id="the-form">') == 1

    @pytest.mark.parametrize("tag", EVERY_SIGN_IN)
    def test_the_logo_is_rendered_once(self, render, tag) -> None:
        html = render(page(tag, slots=slot("logo", '<img id="logo" alt="Acme">')))

        assert html.count('<img id="logo" alt="Acme">') == 1

    @pytest.mark.parametrize("tag", EVERY_SIGN_IN)
    def test_the_page_has_one_first_level_heading(self, render, tag) -> None:
        html = render(page(tag, 'title="Come in"'))

        assert re.findall(r"<h(\d)[^>]*>\s*Come in\s*</h\d>", html) == ["1"]
        assert len(re.findall(r"<h\d\b", html)) == 1

    @pytest.mark.parametrize("tag", EVERY_SIGN_IN)
    def test_the_heading_level_is_the_page_authors_to_set(self, render, tag) -> None:
        html = render(page(tag, 'title="Come in" level="2"'))

        assert re.findall(r"<h(\d)[^>]*>\s*Come in\s*</h\d>", html) == ["2"]

    @pytest.mark.parametrize("tag", EVERY_SIGN_IN)
    def test_the_title_is_escaped(self, render, tag) -> None:
        html = render(page(tag, ':title="title"'), title="<script>x</script>")

        assert "<script>x</script>" not in html
        assert "&lt;script&gt;" in html

    @pytest.mark.parametrize("tag", EVERY_SIGN_IN)
    def test_the_provider_buttons_are_rendered(self, render, tag) -> None:
        html = render(page(tag, slots=slot("providers", '<a id="google">Google</a>')))

        assert html.count('<a id="google">Google</a>') == 1

    @pytest.mark.parametrize("tag", EVERY_SIGN_IN)
    def test_extra_classes_reach_the_outer_element(self, render, tag) -> None:
        html = render(page(tag, 'class="bg-base-200"'))

        assert re.match(r'\s*<section[^>]*class="[^"]*\bbg-base-200\b', html)

    @pytest.mark.parametrize("tag", EVERY_SIGN_IN)
    def test_an_undeclared_attribute_reaches_the_outer_element(
        self, render, tag
    ) -> None:
        html = render(page(tag, 'id="entrance"'))

        assert re.match(r'\s*<section[^>]*\bid="entrance"', html)


class TestWordsTheBlockSupplies:
    @pytest.mark.parametrize("tag", EVERY_SIGN_IN)
    def test_a_page_given_no_title_has_no_empty_heading(self, render, tag) -> None:
        html = render(page(tag))

        assert re.search(r"<h\d\b", html) is None

    @pytest.mark.parametrize("tag", WITH_A_DIVIDER)
    def test_the_buttons_and_the_form_are_separated_without_being_told_how(
        self, render, tag
    ) -> None:
        html = render(page(tag, slots=slot("providers", "<a>Google</a>")))

        assert re.search(r'class="divider[^"]*"[^>]*>\s*\S', html)

    def test_the_disclosure_is_named_without_being_told_how(self, render) -> None:
        html = render(page("c-sign-in.providers"))

        assert re.search(r"<summary[^>]*>\s*\S", html)


class TestBackground:
    @pytest.mark.parametrize("tag", WITH_A_BACKGROUND)
    def test_a_background_goes_in_a_layer_a_screen_reader_skips(
        self, render, tag
    ) -> None:
        html = render(page(tag, slots=slot("background", '<i id="backdrop"></i>')))

        assert re.search(
            r'<div aria-hidden="true"[^>]*>\s*<i id="backdrop"></i>\s*</div>', html
        )

    @pytest.mark.parametrize("tag", WITH_A_BACKGROUND)
    def test_no_background_layer_without_a_background(self, render, tag) -> None:
        html = render(page(tag))

        assert 'aria-hidden="true"' not in html


class TestDivider:
    @pytest.mark.parametrize("tag", WITH_A_DIVIDER)
    def test_a_word_separates_the_buttons_from_the_form(self, render, tag) -> None:
        html = render(
            page(tag, 'divider="otherwise"', slot("providers", "<a>Google</a>"))
        )

        assert re.search(r'class="divider[^"]*"[^>]*>\s*otherwise\s*<', html)

    @pytest.mark.parametrize("tag", WITH_A_DIVIDER)
    def test_no_divider_without_provider_buttons(self, render, tag) -> None:
        html = render(page(tag, 'divider="otherwise"'))

        assert "otherwise" not in html

    @pytest.mark.parametrize(
        "tag", [tag for tag in WITH_A_DIVIDER if tag != "c-sign-in.stepped"]
    )
    def test_no_divider_when_the_buttons_are_all_there_is(self, render, tag) -> None:
        html = render(
            page(
                tag, 'divider="otherwise"', slot("providers", "<a>Google</a>"), form=""
            )
        )

        assert "otherwise" not in html


class TestAside:
    @pytest.mark.parametrize("tag", WITH_AN_ASIDE)
    def test_what_the_pane_says_is_rendered(self, render, tag) -> None:
        html = render(page(tag, slots=slot("aside", '<p id="said">Hello</p>')))

        assert html.count('<p id="said">Hello</p>') == 1

    def test_the_line_on_the_background_is_not_a_second_heading(self, render) -> None:
        html = render(page("c-sign-in.floating", 'title="In" headline="Every release"'))

        assert re.search(r"<p[^>]*>\s*Every release\s*</p>", html)
        assert len(re.findall(r"<h\d\b", html)) == 1

    @pytest.mark.parametrize("tag", ["c-sign-in.split", "c-sign-in.providers"])
    def test_the_pane_takes_the_surface_it_is_given(self, render, tag) -> None:
        html = render(page(tag, 'surface="bg-accent text-accent-content"'))

        assert "bg-accent text-accent-content" in html
        assert "bg-neutral" not in html
        assert "bg-primary" not in html


class TestStepped:
    def test_where_the_reader_is_sits_above_the_question(self, render) -> None:
        html = render(page("c-sign-in.stepped", 'eyebrow="Step 1 of 2" title="Who?"'))

        assert html.index("Step 1 of 2") < html.index("<h1")

    def test_the_question_can_be_the_label_of_its_field(self, render) -> None:
        html = render(
            page(
                "c-sign-in.stepped",
                slots=slot("title", '<label for="id_login">Your email</label>'),
            )
        )

        assert re.search(
            r'<h1[^>]*>\s*<label for="id_login">Your email</label>\s*</h1>', html
        )

    def test_the_way_across_sits_in_the_bar_with_the_logo(self, render) -> None:
        html = render(
            page(
                "c-sign-in.stepped",
                'title="Who?"',
                slot("logo", '<img id="logo" alt="">')
                + slot("nav", '<a id="across">Sign up</a>'),
            )
        )

        assert html.index('id="logo"') < html.index('id="across"') < html.index("<h1")

    def test_the_buttons_come_after_the_answer(self, render) -> None:
        html = render(
            page("c-sign-in.stepped", slots=slot("providers", '<a id="google">G</a>'))
        )

        assert html.index('id="the-form"') < html.index('id="google"')


class TestProvidersFirst:
    def test_the_form_waits_behind_a_disclosure(self, render) -> None:
        html = render(page("c-sign-in.providers", 'disclosure="Use a password"'))

        assert re.search(
            r"<details\b[^>]*>\s*<summary[^>]*>\s*Use a password\s*</summary>"
            r'.*<form id="the-form">.*</details>',
            html,
            re.DOTALL,
        )

    def test_the_disclosure_starts_closed(self, render) -> None:
        html = render(page("c-sign-in.providers"))

        assert re.search(r"<details\b[^>]*\bopen\b", html) is None

    def test_a_form_with_errors_can_start_open(self, render) -> None:
        html = render(page("c-sign-in.providers", "open"))

        assert re.search(r"<details\b[^>]*\bopen\b", html)

    def test_no_disclosure_without_a_form(self, render) -> None:
        html = render(page("c-sign-in.providers", form=""))

        assert "<details" not in html

    def test_the_buttons_come_before_the_form(self, render) -> None:
        html = render(
            page("c-sign-in.providers", slots=slot("providers", '<a id="google">G</a>'))
        )

        assert html.index('id="google"') < html.index('id="the-form"')


class TestSplit:
    def test_the_logo_stays_with_the_form_when_the_pane_goes(self, render) -> None:
        html = render(
            page(
                "c-sign-in.split",
                slots=slot("logo", '<img id="logo" alt="">')
                + slot("aside", '<p id="said">Hello</p>'),
            )
        )

        assert (
            html.index('id="logo"') < html.index('id="the-form"') < html.index("said")
        )

    def test_the_foot_follows_the_form(self, render) -> None:
        html = render(
            page("c-sign-in.split", slots=slot("footer", '<a id="across">Sign up</a>'))
        )

        assert html.index('id="the-form"') < html.index('id="across"')
