"""Points: a short list of reasons, each a few bold words and a sentence."""

import re

POINT = '<c-points.point title="Quick.">Ten minutes.</c-points.point>'


class TestPoints:
    def test_the_points_are_items_of_one_list(self, render) -> None:
        html = render(f"<c-points>{POINT}{POINT}</c-points>")

        assert re.match(r"\s*<ul\b", html)
        assert len(re.findall(r"<li\b", html)) == 2

    def test_extra_classes_reach_the_list(self, render) -> None:
        html = render(f'<c-points class="max-w-xl">{POINT}</c-points>')

        assert re.match(r'\s*<ul[^>]*class="[^"]*\bmax-w-xl\b', html)

    def test_an_undeclared_attribute_reaches_the_list(self, render) -> None:
        html = render(f'<c-points id="why">{POINT}</c-points>')

        assert re.match(r'\s*<ul[^>]*\bid="why"', html)


class TestPoint:
    def test_the_bold_words_lead_into_the_sentence(self, render) -> None:
        html = render(POINT)

        assert re.search(r"<strong>Quick\.</strong>\s*Ten minutes\.", html)

    def test_a_point_with_no_bold_words_is_just_the_sentence(self, render) -> None:
        html = render("<c-points.point>Ten minutes.</c-points.point>")

        assert "<strong" not in html

    def test_the_bold_words_are_escaped(self, render) -> None:
        html = render(
            '<c-points.point :title="title">x</c-points.point>',
            title="<script>x</script>",
        )

        assert "<script>x</script>" not in html
        assert "&lt;script&gt;" in html

    def test_the_tick_is_hidden_from_a_screen_reader(self, render) -> None:
        html = render(POINT)

        assert re.search(r'<span aria-hidden="true"[^>]*>\s*<svg\b', html)

    def test_a_mark_takes_the_place_of_the_tick(self, render) -> None:
        html = render(
            '<c-points.point title="Quick.">'
            '<c-slot name="mark"><i id="mark"></i></c-slot>Ten minutes.'
            "</c-points.point>"
        )

        assert re.search(r'<span aria-hidden="true"[^>]*>\s*<i id="mark"></i>', html)
        assert "<svg" not in html

    def test_extra_classes_reach_the_item(self, render) -> None:
        html = render('<c-points.point class="py-2" title="Quick." />')

        assert re.match(r'\s*<li[^>]*class="[^"]*\bpy-2\b', html)
