"""Every packaged block documents itself in its own template, per Article XVI.

The annotations at the head of each component are the only description of what
it accepts. The component gallery builds its live controls from them and each
block's page in the example project builds its tables from the same comments,
so a block that drops one, mis-spells a default or documents an attribute it no
longer takes breaks two readers at once and neither of them loudly.

The linting is django-cotton-gallery's rather than ours. A second implementation
of the annotation format would drift from the one that actually has to parse it,
and the first symptom would be a page describing an attribute that is gone. What
this module adds on top are the two rules the gallery has no opinion about: that
a component says what it is, and that a slot it renders is a slot it documents.
"""

import re
from pathlib import Path

import pytest
from django_cotton_gallery.core.annotations import AnnotationParser
from django_cotton_gallery.core.linter import lint_component

import daisy_cotton_ext

COMPONENTS = Path(daisy_cotton_ext.__file__).parent / "templates" / "cotton"

# Cotton fills a named slot whether or not it is declared, so a slot is found by
# reading what the template renders and subtracting what it declares.
RENDERED_VARIABLE = re.compile(r"\{\{\s*([a-z_][a-z0-9_]*)\s*\}\}")

# Rendered by Cotton itself, or by the template's own loop and block syntax.
NOT_A_SLOT = frozenset({"attrs", "slot"})


def blocks() -> list[Path]:
    return sorted(COMPONENTS.rglob("*.html"))


def block_ids() -> list[str]:
    return [f"c-{path.parent.name}.{path.stem}" for path in blocks()]


@pytest.fixture(params=blocks(), ids=block_ids())
def block(request) -> Path:
    return request.param


class TestEveryBlockLintsClean:
    def test_there_are_blocks_to_check(self) -> None:
        assert len(blocks()) >= 8

    def test_the_component_reports_no_issues(self, block: Path) -> None:
        report = lint_component(str(block), block.read_text(encoding="utf-8"))

        assert not report.issues, "\n".join(
            f"[{issue.severity}] {issue.rule}: {issue.message}"
            for issue in report.issues
        )


class TestEveryBlockSaysWhatItIs:
    def test_the_component_has_a_description(self, block: Path) -> None:
        component = AnnotationParser().parse(block.read_text(encoding="utf-8"))

        assert component.description.strip()

    def test_every_slot_the_block_renders_is_documented(self, block: Path) -> None:
        source = block.read_text(encoding="utf-8")
        component = AnnotationParser().parse(source)

        declared = {prop.clean_name for prop in component.props}
        documented = {slot.name for slot in component.slots}
        rendered = {
            name
            for name in RENDERED_VARIABLE.findall(source)
            if name not in declared and name not in NOT_A_SLOT
        }

        assert rendered <= documented, (
            f"{sorted(rendered - documented)} rendered but not documented with @slot"
        )


class TestTheGateGoesRed:
    SOURCE = (
        "{# @description A card. #}\n"
        '{# @prop title:text | description:"The heading" #}\n'
        "{# @slot:footer — Under the body #}\n"
        "<c-vars title />\n"
        "<div>{{ title }}{{ footer }}</div>\n"
    )

    def test_an_undocumented_attribute_is_caught(self) -> None:
        source = self.SOURCE.replace("<c-vars title />", "<c-vars title tone />")

        report = lint_component("cotton/demo/card.html", source)

        assert {issue.rule for issue in report.issues} == {"missing-annotation"}

    def test_an_attribute_documented_but_not_declared_is_caught(self) -> None:
        source = self.SOURCE.replace(
            "<c-vars title />", "<c-vars title />\n{# @prop tone:text #}"
        )

        report = lint_component("cotton/demo/card.html", source)

        assert "orphan-annotation" in {issue.rule for issue in report.issues}

    def test_a_missing_description_is_caught(self) -> None:
        source = self.SOURCE.replace("{# @description A card. #}\n", "")

        component = AnnotationParser().parse(source)

        assert not component.description.strip()

    def test_an_undocumented_slot_is_caught(self) -> None:
        source = self.SOURCE.replace("{# @slot:footer — Under the body #}\n", "")

        component = AnnotationParser().parse(source)
        declared = {prop.clean_name for prop in component.props}
        documented = {slot.name for slot in component.slots}
        rendered = {
            name
            for name in RENDERED_VARIABLE.findall(source)
            if name not in declared and name not in NOT_A_SLOT
        }

        assert rendered - documented == {"footer"}

    def test_the_clean_source_passes_all_three(self) -> None:
        component = AnnotationParser().parse(self.SOURCE)
        report = lint_component("cotton/demo/card.html", self.SOURCE)

        assert not report.issues
        assert component.description.strip()
        assert {slot.name for slot in component.slots} == {"footer"}
