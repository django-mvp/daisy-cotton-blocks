"""The contract between this package's stylesheet and the host project's.

The blocks here are daisyUI markup. daisyUI, its themes and Tailwind's preflight
all come from the host. What the host cannot supply is the plain Tailwind
utilities this package's own templates ask for, because a host's build scans the
host's source and never reaches site-packages.

So the stylesheet shipped here has to be self-sufficient for those utilities, and
that is what these tests measure. Overlap with a host's own build is expected and
deliberately not tested: a project running django-mvp loads two stylesheets that
both define ``py-20``, which costs bytes and nothing else.

django-mvp appears below only as a stand-in host. The example project runs on it,
so its stylesheet is what the example's markup is checked against.

Stylesheets are located through the staticfiles finders rather than by walking up
from a module's ``__file__``, because that is how a project actually reaches them
-- and because ``mvp`` is a namespace package, whose ``__file__`` is None.

The companion check -- that the committed build still matches
assets/daisy-cotton-blocks.css -- needs the Node toolchain. It runs in the
Stylesheet workflow, and locally via ``npm test``.
"""

import re
from pathlib import Path

import pytest
from django.contrib.staticfiles import finders

BLOCKS_STYLESHEET = "css/daisy-cotton-blocks.css"
HOST_STYLESHEET = "css/django-mvp.css"

CLASS_TOKEN = re.compile(r"\.((?:[A-Za-z0-9_-]|\\.)+)")

# Anchored to the repo root rather than the working directory, so the scan
# finds the same templates however pytest was invoked.
REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_TEMPLATES = REPO_ROOT / "daisy_cotton_blocks" / "templates"
EXAMPLE_TEMPLATES = REPO_ROOT / "example" / "templates"

CLASS_ATTRIBUTE = re.compile(r"""\bclass\s*=\s*["']([^"']*)["']""")

# The daisyUI classes a block may use without this package emitting a rule for
# them. This list is the host contract, written out: a project installing this
# package is already running daisyUI, and these are the parts of it blocks reach
# for.
#
# It is deliberately explicit rather than inferred. Reaching for a daisyUI class
# that is not listed here fails the coverage test below, which is the prompt to
# decide whether the host really should be expected to provide it.
HOST_PROVIDED_CLASSES = frozenset(
    {
        "avatar",
        "badge",
        "btn",
        "btn-accent",
        "btn-ghost",
        "btn-lg",
        "btn-link",
        "btn-neutral",
        "btn-outline",
        "btn-primary",
        "btn-secondary",
        "btn-sm",
        "card",
        "card-actions",
        "card-body",
        "card-title",
        "collapse",
        "collapse-arrow",
        "collapse-content",
        "collapse-title",
        "divider",
        "hero",
        "hero-content",
        "hero-overlay",
        "link",
        "mockup-browser",
        "mockup-phone",
        "mockup-window",
        "stat",
        "stat-desc",
        "stat-title",
        "stat-value",
        "stats",
    }
)


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


def template_classes(root: Path) -> dict[str, set[str]]:
    """Every static class token the templates under ``root`` ask for.

    Keyed by class, valued by the templates using it, so a failure names the
    file to go and look at. Tokens carrying Django template syntax are skipped:
    a class composed at render time cannot be resolved by reading the source,
    which is why assets/daisy-cotton-blocks.css names those inline.
    """
    used: dict[str, set[str]] = {}
    if not root.is_dir():
        return used
    for template in root.rglob("*.html"):
        markup = template.read_text(encoding="utf-8")
        for attribute in CLASS_ATTRIBUTE.findall(markup):
            if "{{" in attribute or "{%" in attribute:
                continue
            for token in attribute.split():
                used.setdefault(token, set()).add(str(template.relative_to(REPO_ROOT)))
    return used


def report_missing(missing: dict[str, set[str]]) -> str:
    return "\n".join(
        [f"{len(missing)} class(es) resolve to no rule:"]
        + [
            f"  {token} — used in {', '.join(sorted(templates))}"
            for token, templates in sorted(missing.items())
        ]
    )


@pytest.fixture(scope="module")
def blocks_classes() -> set[str]:
    return class_selectors(locate(BLOCKS_STYLESHEET))


@pytest.fixture(scope="module")
def host_classes() -> set[str]:
    return class_selectors(locate(HOST_STYLESHEET))


class TestStylesheetStaysOutOfTheHostsWay:
    """What this package ships, and what it leaves to the host."""

    def test_stylesheet_is_discoverable(self) -> None:
        """A missing file would make every assertion below vacuously true."""
        assert locate(BLOCKS_STYLESHEET).is_file()

    def test_stylesheet_is_not_empty(self, blocks_classes: set[str]) -> None:
        """Guards the parser, not the stylesheet.

        An extractor that silently returned nothing would make the coverage test
        pass however little the stylesheet actually emitted.
        """
        assert len(blocks_classes) > 100, (
            f"only parsed {len(blocks_classes)} classes out of the stylesheet"
        )

    def test_stylesheet_carries_no_theme_or_preflight(self) -> None:
        """Both belong to the host, and emitting them here would fight it.

        Re-emitting the theme layer would put a second `:root` block on the page
        and let this package silently win a cascade it has no business entering.
        A second preflight would reset elements the host has already styled.
        """
        css = locate(BLOCKS_STYLESHEET).read_text(encoding="utf-8")
        assert ":root" not in css, "the stylesheet re-emits Tailwind's theme layer"
        assert "box-sizing" not in css, "the stylesheet re-emits Tailwind's preflight"

    def test_stylesheet_emits_no_daisyui_component_rules(
        self, blocks_classes: set[str]
    ) -> None:
        """daisyUI is the host's to provide, and two copies would fight.

        A daisyUI class emitted here would be a second definition of a component
        the host already styles, and which of the two won would come down to the
        order a project happened to link them in.
        """
        emitted = sorted(blocks_classes & HOST_PROVIDED_CLASSES)
        assert not emitted, (
            f"the stylesheet emits {len(emitted)} daisyUI class(es): "
            f"{', '.join(emitted)}. These come from the host."
        )


class TestBlocksAreSelfSufficient:
    """Every utility a block asks for is one this package ships."""

    def test_every_class_used_by_a_block_resolves(
        self, blocks_classes: set[str]
    ) -> None:
        """The contract a host cannot help with.

        A host's Tailwind build scans the host's own source, so a utility used
        only inside this package's templates is absent from it. The failure that
        causes looks like nothing at all: the page renders, the class sits in
        the DOM, and no rule matches it. That is how the gradient on the example
        page shipped dead — `bg-gradient-to-br` built, while `from-primary` and
        `to-secondary` did not.

        daisyUI's own classes are excluded, because those are exactly what the
        host is expected to bring.
        """
        used = template_classes(PACKAGE_TEMPLATES)
        if not used:
            pytest.skip("the package ships no blocks yet, so there is nothing to check")

        missing = {
            token: templates
            for token, templates in used.items()
            if token not in blocks_classes and token not in HOST_PROVIDED_CLASSES
        }
        assert not missing, (
            report_missing(missing)
            + "\nAdd them to assets/daisy-cotton-blocks.css and rebuild with "
            "`npm run build:css`, or list them in HOST_PROVIDED_CLASSES if the "
            "host should be providing them."
        )

    def test_example_page_renders_against_its_host(
        self, blocks_classes: set[str], host_classes: set[str]
    ) -> None:
        """The example is a host project, so it may use anything its host emits.

        Held to a wider bar than a block on purpose: the example demonstrates a
        page built on django-mvp, and page markup outside a block is free to use
        django-mvp's own utilities.
        """
        used = template_classes(EXAMPLE_TEMPLATES)
        assert used, "no template classes were found to check — the scanner is broken"

        available = blocks_classes | host_classes
        missing = {
            token: templates
            for token, templates in used.items()
            if token not in available
        }
        assert not missing, report_missing(missing)
