"""Every packaged block documents itself in its own template, per Article XVII.

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

import daisy_cotton_blocks

COMPONENTS = Path(daisy_cotton_blocks.__file__).parent / "templates" / "cotton"

# `{{ name }}` where the template renders a slot rather than a prop. Cotton
# fills a named slot whether or not it is declared, so the only way to find one
# is to read what the template renders and subtract what it declares.
RENDERED_VARIABLE = re.compile(r"\{\{\s*([a-z_][a-z0-9_]*)\s*\}\}")

# Rendered by Cotton itself, or by the template's own loop and block syntax.
NOT_A_SLOT = frozenset({"attrs", "slot"})


def blocks() -> list[Path]:
    """Every packaged component, as the path to its template."""
    return sorted(COMPONENTS.rglob("*.html"))


def block_ids() -> list[str]:
    return [f"c-{path.parent.name}.{path.stem}" for path in blocks()]


@pytest.fixture(params=blocks(), ids=block_ids())
def block(request) -> Path:
    return request.param


class TestEveryBlockLintsClean:
    """The gallery's own rules, run over what this package ships."""

    def test_there_are_blocks_to_check(self) -> None:
        """A rename or a moved directory would make every case below vacuous."""
        assert len(blocks()) >= 8

    def test_the_component_reports_no_issues(self, block: Path) -> None:
        """At any severity, including the heuristic ones.

        The gallery weighs hints at zero because a project's context processors
        can trip them. Nothing here has a context processor: a block's content
        arrives through attributes and slots and nowhere else, so a variable
        this package renders and does not declare is a real finding rather than
        a false one.
        """
        report = lint_component(str(block), block.read_text(encoding="utf-8"))

        assert not report.issues, "\n".join(
            f"[{issue.severity}] {issue.rule}: {issue.message}"
            for issue in report.issues
        )


class TestEveryBlockSaysWhatItIs:
    """The two rules the gallery has no opinion about."""

    def test_the_component_has_a_description(self, block: Path) -> None:
        """A block cannot be chosen from its name.

        The description is what the gallery lists it by and what its page in
        the example project leads with, so a block without one is browsable and
        still unchoosable.
        """
        component = AnnotationParser().parse(block.read_text(encoding="utf-8"))

        assert component.description.strip()

    def test_every_slot_the_block_renders_is_documented(self, block: Path) -> None:
        """A slot is invisible from the declaration, so it has to be read off
        the markup. Cotton fills a named slot whether or not anything declares
        it, which means an undocumented slot works perfectly and is findable
        only by reading the template — exactly what these annotations exist to
        save a reader from.
        """
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
    """Each check above, run against the defect it exists to catch.

    A gate nobody has watched fail is not yet evidence of anything, and every
    block in the package is expected to keep all three green.
    """

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
        """Without this, every case above could be passing on a broken fixture."""
        component = AnnotationParser().parse(self.SOURCE)
        report = lint_component("cotton/demo/card.html", self.SOURCE)

        assert not report.issues
        assert component.description.strip()
        assert {slot.name for slot in component.slots} == {"footer"}
