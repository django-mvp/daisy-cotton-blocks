import pytest
from django.utils.safestring import SafeData, mark_safe

from daisy_cotton_ext.templatetags.text_effects import plain


class TestPlain:
    def test_a_line_that_was_already_escaped_is_given_back_as_written(self) -> None:
        assert plain(mark_safe("R&amp;D &lt;3")) == "R&D <3"

    def test_a_line_that_was_never_escaped_is_left_alone(self) -> None:
        assert plain("R&amp;D") == "R&amp;D"

    def test_the_result_is_escaped_again_when_a_template_writes_it(self) -> None:
        assert not isinstance(plain(mark_safe("&lt;b&gt;")), SafeData)

    @pytest.mark.parametrize(("value", "line"), [(None, "None"), (42, "42")])
    def test_anything_else_becomes_its_string(self, value, line) -> None:
        assert plain(value) == line
