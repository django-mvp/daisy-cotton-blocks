"""The sign-in panel: the structure every sign-in and sign-up form is drawn in.

A heading, the buttons that skip the form, a word between, the form, and a
foot. Seven page blocks draw their form through it, so its order and what it
leaves out when a part is missing are theirs too.
"""

import re

FORM = '<form id="the-form"></form>'
PROVIDERS = '<c-slot name="providers"><a id="google">Google</a></c-slot>'
FOOTER = '<c-slot name="footer"><a id="across">Sign up</a></c-slot>'


def panel(attributes: str = "", content: str = FORM) -> str:
    """Return markup for a panel."""
    return f"<c-auth.panel {attributes}>{content}</c-auth.panel>"


class TestPanel:
    def test_the_parts_are_read_in_order(self, render) -> None:
        html = render(panel('title="Come in"', PROVIDERS + FORM + FOOTER))

        assert (
            html.index("Come in")
            < html.index('id="google"')
            < html.index('id="the-form"')
            < html.index('id="across"')
        )

    def test_the_heading_level_is_the_page_authors_to_set(self, render) -> None:
        html = render(panel('title="Come in" level="3"'))

        assert re.search(r"<h3[^>]*>\s*Come in\s*</h3>", html)

    def test_a_panel_given_no_title_has_no_heading(self, render) -> None:
        html = render(panel())

        assert re.search(r"<h\d\b", html) is None

    def test_the_sentence_under_the_heading_is_left_out_when_empty(
        self, render
    ) -> None:
        html = render(panel('title="Come in"'))

        assert "<p" not in html

    def test_the_sentence_under_the_heading_is_escaped(self, render) -> None:
        html = render(panel(':lead="lead"'), lead="<script>x</script>")

        assert "<script>x</script>" not in html
        assert "&lt;script&gt;" in html

    def test_a_word_separates_the_buttons_from_the_form(self, render) -> None:
        html = render(panel('divider="otherwise"', PROVIDERS + FORM))

        assert re.search(r'class="divider[^"]*"[^>]*>\s*otherwise\s*<', html)

    def test_no_divider_without_provider_buttons(self, render) -> None:
        html = render(panel('divider="otherwise"'))

        assert "otherwise" not in html

    def test_no_divider_without_a_form(self, render) -> None:
        html = render(panel('divider="otherwise"', PROVIDERS))

        assert "otherwise" not in html


class TestCard:
    def test_a_bare_panel_is_not_a_card(self, render) -> None:
        html = render(panel())

        assert "card" not in html

    def test_a_card_wraps_the_whole_panel(self, render) -> None:
        html = render(panel('card title="Come in"', FORM + FOOTER))

        assert re.match(
            r'\s*<div class="card\b[^"]*"[^>]*>\s*<div class="card-body', html
        )
        assert html.rstrip().endswith("</div></div>")

    def test_the_card_takes_the_surface_it_is_given(self, render) -> None:
        html = render(panel('card surface="bg-base-200"'))

        assert re.match(r'\s*<div class="card bg-base-200\b', html)
        assert "bg-base-100" not in html

    def test_a_bare_panel_ignores_the_surface(self, render) -> None:
        html = render(panel('surface="bg-base-200"'))

        assert "bg-base-200" not in html

    def test_extra_classes_reach_the_outer_element_either_way(self, render) -> None:
        for attributes in ('class="mx-auto"', 'card class="mx-auto"'):
            html = render(panel(attributes))

            assert re.match(r'\s*<div[^>]*class="[^"]*\bmx-auto\b', html)

    def test_an_undeclared_attribute_reaches_the_outer_element(self, render) -> None:
        for attributes in ('id="entrance"', 'card id="entrance"'):
            html = render(panel(attributes))

            assert re.match(r'\s*<div[^>]*\bid="entrance"', html)
