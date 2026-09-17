"""The contract between this package's stylesheet and django-mvp's.

This package ships a supplement, not a second stylesheet. Every rule it emits
must be one django-mvp does not already emit, because a project loads both and
duplicated rules are pure page weight.

Stating that in a comment does not keep it true. django-mvp's utility surface
moves for reasons that have nothing to do with this package: it scans daisyUI's
component sources for class tokens, so upgrading daisyUI silently adds and
removes classes from its build. These tests measure the result instead of
trusting it.

Both files are located through the staticfiles finders rather than by walking up
from a module's ``__file__``, because that is how a project actually reaches
them — and because ``mvp`` is a namespace package, whose ``__file__`` is None.

The companion check — that the committed build still matches assets/mvp-bits.css
— needs the Node toolchain. It runs in the Stylesheet workflow, and locally via
`npm test`, which `forge verify` picks up through the node adapter.
"""

import re
from pathlib import Path

import pytest
from django.contrib.staticfiles import finders

MVP_STYLESHEET = "css/django-mvp.css"
BITS_STYLESHEET = "css/mvp-bits.css"

CLASS_TOKEN = re.compile(r"\.((?:[A-Za-z0-9_-]|\\.)+)")

# Anchored to the repo root rather than the working directory, so the scan
# finds the same templates however pytest was invoked.
REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_ROOTS = (
    REPO_ROOT / "mvp_bits" / "templates",
    REPO_ROOT / "example" / "templates",
)

CLASS_ATTRIBUTE = re.compile(r"""\bclass\s*=\s*["']([^"']*)["']""")


def locate(static_path: str) -> Path:
    """Resolve a static file the way a project's template tag would."""
    found = finders.find(static_path)
    assert found is not None, (
        f"{static_path} is not discoverable through the staticfiles finders"
    )
    return Path(found)


def class_selectors(stylesheet: Path) -> set[str]:
    """Return every class name the stylesheet defines a rule for.

    Walks the character stream rather than matching line by line, because
    Tailwind's CLI minifies by default and the whole file arrives on a handful
    of lines. The text before each `{` is a prelude: an at-rule when it starts
    with `@` (skipped, its inner selectors are visited on their own), otherwise
    a selector list to read class tokens out of.
    """
    css = re.sub(r"/\*.*?\*/", "", stylesheet.read_text(encoding="utf-8"), flags=re.S)
    found: set[str] = set()
    start = 0
    for index, char in enumerate(css):
        if char == "{":
            prelude = css[start:index].strip()
            start = index + 1
            if prelude and not prelude.startswith("@"):
                found |= {
                    re.sub(r"\\(.)", r"\1", match.group(1))
                    for match in CLASS_TOKEN.finditer(prelude)
                }
        elif char == "}":
            start = index + 1
    return found


def template_classes() -> dict[str, set[str]]:
    """Every static class token this package's own templates ask for.

    Keyed by class, valued by the templates using it, so a failure names the
    file to go and look at. Tokens carrying Django template syntax are skipped:
    a class composed at render time cannot be resolved by reading the source,
    which is the same reason the whitelist in assets/mvp-bits.css has to name
    those by hand.
    """
    used: dict[str, set[str]] = {}
    for root in TEMPLATE_ROOTS:
        for template in root.rglob("*.html"):
            markup = template.read_text(encoding="utf-8")
            for attribute in CLASS_ATTRIBUTE.findall(markup):
                if "{{" in attribute or "{%" in attribute:
                    continue
                for token in attribute.split():
                    used.setdefault(token, set()).add(
                        str(template.relative_to(REPO_ROOT))
                    )
    return used


@pytest.fixture(scope="module")
def mvp_classes() -> set[str]:
    return class_selectors(locate(MVP_STYLESHEET))


@pytest.fixture(scope="module")
def bits_classes() -> set[str]:
    return class_selectors(locate(BITS_STYLESHEET))


class TestSupplementIsAdditive:
    """The supplement adds to django-mvp's stylesheet and restates none of it."""

    def test_both_stylesheets_are_discoverable(self) -> None:
        """A missing file would make every assertion below vacuously true."""
        assert locate(MVP_STYLESHEET).is_file()
        assert locate(BITS_STYLESHEET).is_file()

    def test_stylesheets_are_not_empty(
        self, mvp_classes: set[str], bits_classes: set[str]
    ) -> None:
        """Guards the parser, not the stylesheets.

        An extractor that silently returned nothing would make the overlap test
        pass no matter how much the two files duplicated.
        """
        assert len(mvp_classes) > 1000, (
            f"only parsed {len(mvp_classes)} classes out of django-mvp's stylesheet"
        )
        assert len(bits_classes) > 100, (
            f"only parsed {len(bits_classes)} classes out of this package's stylesheet"
        )

    def test_no_selector_is_defined_by_both_stylesheets(
        self, mvp_classes: set[str], bits_classes: set[str]
    ) -> None:
        """The whole contract, in one assertion."""
        overlap = sorted(mvp_classes & bits_classes)
        assert not overlap, (
            f"{len(overlap)} class(es) are defined by both stylesheets: {', '.join(overlap)}. "
            "django-mvp already ships these, so remove them from the whitelist in "
            "assets/mvp-bits.css and rebuild with `npm run build:css`."
        )

    def test_stylesheet_carries_no_theme_or_preflight(self) -> None:
        """The supplement must not restate what django-mvp defines.

        Re-emitting the theme layer would put a second `:root` block on the page
        and let this package silently win a cascade it has no business entering;
        a second preflight would reset elements django-mvp has already styled.
        """
        css = locate(BITS_STYLESHEET).read_text(encoding="utf-8")
        assert ":root" not in css, "the stylesheet re-emits Tailwind's theme layer"
        assert "box-sizing" not in css, "the stylesheet re-emits Tailwind's preflight"


class TestWhitelistCoversTemplates:
    """Every class the templates ask for is one of the two stylesheets emits."""

    def test_every_class_used_in_a_template_actually_exists(
        self, mvp_classes: set[str], bits_classes: set[str]
    ) -> None:
        """A whitelisted class that emits no rule is invisible without this test.

        The failure it catches looks like nothing at all: the page renders, the
        class sits in the DOM, and no rule matches it. That is how the gradient
        on the example page shipped dead — `bg-gradient-to-br` built, while
        `from-primary` and `to-secondary` did not, because daisyUI's palette is
        not in the theme this stylesheet references.

        This is about whether our own whitelist is right, not about whether
        django-mvp is stable. Losing a class because django-mvp stopped emitting
        it is a supported outcome: this package does not work without
        django-mvp's stylesheet and has never pretended otherwise.
        """
        available = mvp_classes | bits_classes
        used = template_classes()
        assert used, "no template classes were found to check — the scanner is broken"

        missing = {
            token: sorted(templates)
            for token, templates in used.items()
            if token not in available
        }
        assert not missing, "\n".join(
            [f"{len(missing)} class(es) resolve to no rule in either stylesheet:"]
            + [
                f"  {token} — used in {', '.join(templates)}"
                for token, templates in sorted(missing.items())
            ]
        )
