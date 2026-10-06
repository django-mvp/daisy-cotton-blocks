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
assets/daisy-cotton-ext.css -- needs the Node toolchain. It runs in the
Stylesheet workflow, and locally via ``npm test``.
"""

import re
from pathlib import Path

import pytest
from django.contrib.staticfiles import finders
from django_cotton_gallery.core.annotations import AnnotationParser

BLOCKS_STYLESHEET = "css/daisy-cotton-ext.css"
HOST_STYLESHEET = "css/django-mvp.css"

CLASS_TOKEN = re.compile(r"\.((?:[A-Za-z0-9_-]|\\.)+)")

# Anchored to the repo root so the scan finds the same templates from any directory.
REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_TEMPLATES = REPO_ROOT / "daisy_cotton_ext" / "templates"
EXAMPLE_TEMPLATES = REPO_ROOT / "example" / "templates"

# The closing quote must match the opening one: `{% if size == 'sm' %}` puts single
# quotes inside a double-quoted attribute and would cut the match short (#20).
CLASS_ATTRIBUTE = re.compile(
    r"""\bclass\s*=\s*(?P<quote>["'])(?P<value>.*?)(?P=quote)""", re.S
)

TEMPLATE_TAG = re.compile(r"\{%.*?%\}", re.S)
TEMPLATE_VARIABLE = re.compile(r"\{\{.*?\}\}", re.S)

# Stands in for a value only the renderer knows. No class name contains it, so a
# token that kept one was still being assembled.
COMPOSED_AT_RENDER_TIME = "\x00"

# The daisyUI classes the host supplies, so this package emits no rule for them.
# Explicit rather than inferred: an unlisted class fails the coverage test, which
# prompts a decision on whether the host should provide it (#20).
HOST_PROVIDED_CLASSES = frozenset(
    {
        "avatar",
        "badge",
        "badge-error",
        "badge-neutral",
        "badge-sm",
        "badge-soft",
        "badge-success",
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
        "progress",
        "progress-accent",
        "progress-error",
        "progress-primary",
        "progress-secondary",
        "progress-success",
        "progress-warning",
        "stat",
        "stat-actions",
        "stat-desc",
        "stat-figure",
        "stat-title",
        "stat-value",
        "stats",
    }
)


def locate(static_path: str) -> Path:
    found = finders.find(static_path)
    assert found is not None, (
        f"{static_path} is not discoverable through the staticfiles finders"
    )
    return Path(found)


def class_selectors(stylesheet: Path) -> set[str]:
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


def literal_classes(attribute: str) -> list[str]:
    text = TEMPLATE_TAG.sub(" ", attribute)
    text = TEMPLATE_VARIABLE.sub(COMPOSED_AT_RENDER_TIME, text)
    return [token for token in text.split() if COMPOSED_AT_RENDER_TIME not in token]


def template_classes(root: Path) -> dict[str, set[str]]:
    used: dict[str, set[str]] = {}
    if not root.is_dir():
        return used
    for template in root.rglob("*.html"):
        markup = template.read_text(encoding="utf-8")
        name = (
            template.relative_to(REPO_ROOT)
            if template.is_relative_to(REPO_ROOT)
            else template
        )
        for attribute in CLASS_ATTRIBUTE.finditer(markup):
            for token in literal_classes(attribute.group("value")):
                used.setdefault(token, set()).add(str(name))
    return used


def unresolved_classes(
    used: dict[str, set[str]], available: set[str]
) -> dict[str, set[str]]:
    return {
        token: templates for token, templates in used.items() if token not in available
    }


def report_missing(missing: dict[str, set[str]]) -> str:
    return "\n".join(
        [f"{len(missing)} class(es) resolve to no rule:"]
        + [
            f"  {token} — used in {', '.join(sorted(templates))}"
            for token, templates in sorted(missing.items())
        ]
    )


class TestTheClassScanner:
    def scan(self, tmp_path: Path, markup: str) -> dict[str, set[str]]:
        (tmp_path / "block.html").write_text(markup, encoding="utf-8")
        return template_classes(tmp_path)

    def test_a_literal_class_beside_template_syntax_is_read(
        self, tmp_path: Path
    ) -> None:
        found = self.scan(tmp_path, '<section class="isolate {{ class }}">')
        assert "isolate" in found

    def test_both_branches_of_a_conditional_are_read(self, tmp_path: Path) -> None:
        found = self.scan(
            tmp_path,
            '<section class="{% if invert %}text-neutral-content'
            '{% else %}text-base-content{% endif %}">',
        )
        assert {"text-neutral-content", "text-base-content"} <= set(found)

    def test_two_branches_do_not_fuse_into_one_token(self, tmp_path: Path) -> None:
        found = self.scan(
            tmp_path,
            '<section class="{% if a %}py-12{% endif %}{% if b %}py-16{% endif %}">',
        )
        assert {"py-12", "py-16"} <= set(found)
        assert "py-12py-16" not in found

    def test_a_class_after_a_quoted_comparison_is_read(self, tmp_path: Path) -> None:
        found = self.scan(
            tmp_path,
            "<section class=\"{% if size == 'sm' %}py-12{% else %}py-24{% endif %}\">",
        )
        assert {"py-12", "py-24"} <= set(found)

    def test_an_attribute_spanning_several_lines_is_read_whole(
        self, tmp_path: Path
    ) -> None:
        found = self.scan(
            tmp_path,
            '<section class="relative\n                isolate\n'
            '                overflow-hidden">',
        )
        assert {"relative", "isolate", "overflow-hidden"} <= set(found)

    def test_a_class_composed_at_render_time_is_left_to_the_inline_list(
        self, tmp_path: Path
    ) -> None:
        found = self.scan(tmp_path, '<section class="isolate text-{{ tone }}-content">')
        assert set(found) == {"isolate"}

    def test_a_template_is_named_by_the_classes_it_uses(self, tmp_path: Path) -> None:
        found = self.scan(tmp_path, '<section class="isolate">')
        assert found["isolate"] == {str(tmp_path / "block.html")}


@pytest.fixture(scope="module")
def blocks_classes() -> set[str]:
    return class_selectors(locate(BLOCKS_STYLESHEET))


@pytest.fixture(scope="module")
def host_classes() -> set[str]:
    return class_selectors(locate(HOST_STYLESHEET))


class TestStylesheetStaysOutOfTheHostsWay:
    def test_stylesheet_is_discoverable(self) -> None:
        assert locate(BLOCKS_STYLESHEET).is_file()

    def test_stylesheet_is_not_empty(self, blocks_classes: set[str]) -> None:
        assert len(blocks_classes) > 100, (
            f"only parsed {len(blocks_classes)} classes out of the stylesheet"
        )

    def test_stylesheet_carries_no_theme_or_preflight(self) -> None:
        css = locate(BLOCKS_STYLESHEET).read_text(encoding="utf-8")
        assert ":root" not in css, "the stylesheet re-emits Tailwind's theme layer"
        assert "box-sizing" not in css, "the stylesheet re-emits Tailwind's preflight"

    def test_stylesheet_emits_no_daisyui_component_rules(
        self, blocks_classes: set[str]
    ) -> None:
        emitted = sorted(blocks_classes & HOST_PROVIDED_CLASSES)
        assert not emitted, (
            f"the stylesheet emits {len(emitted)} daisyUI class(es): "
            f"{', '.join(emitted)}. These come from the host."
        )


class TestBlocksAreSelfSufficient:
    def test_every_class_used_by_a_block_resolves(
        self, blocks_classes: set[str]
    ) -> None:
        used = template_classes(PACKAGE_TEMPLATES)
        assert used, "no template classes were found to check — the scanner is broken"

        missing = unresolved_classes(used, blocks_classes | HOST_PROVIDED_CLASSES)
        assert not missing, (
            report_missing(missing)
            + "\nAdd them to assets/daisy-cotton-ext.css and rebuild with "
            "`npm run build:css`, or list them in HOST_PROVIDED_CLASSES if the "
            "host should be providing them."
        )

    def test_example_page_renders_against_its_host(
        self, blocks_classes: set[str], host_classes: set[str]
    ) -> None:
        used = template_classes(EXAMPLE_TEMPLATES)
        assert used, "no template classes were found to check — the scanner is broken"

        missing = unresolved_classes(used, blocks_classes | host_classes)
        assert not missing, report_missing(missing)

    def test_a_dead_class_in_a_conditional_branch_is_caught(
        self, tmp_path: Path, blocks_classes: set[str]
    ) -> None:
        (tmp_path / "block.html").write_text(
            '<section class="py-16 space-y-4\n'
            "               {% if size == 'sm' %}md:py-16"
            '{% else %}not-a-utility-anything-emits{% endif %}">',
            encoding="utf-8",
        )

        missing = unresolved_classes(
            template_classes(tmp_path), blocks_classes | HOST_PROVIDED_CLASSES
        )

        assert set(missing) == {"not-a-utility-anything-emits"}
        assert "block.html" in report_missing(missing)


def block_tags() -> list[str]:
    return sorted(
        f"c-{template.parent.name}.{template.stem}"
        for template in (PACKAGE_TEMPLATES / "cotton").rglob("*.html")
    )


def source_of(tag: str) -> str:
    family, component = tag.removeprefix("c-").split(".")
    return (PACKAGE_TEMPLATES / "cotton" / family / f"{component}.html").read_text(
        encoding="utf-8"
    )


def classes_reaching_the_dom(render, tag: str) -> set[str]:
    component = AnnotationParser().parse(source_of(tag))
    variants = [""] + [
        f'{prop.clean_name}="{option}"'
        for prop in component.props
        for option in prop.options
    ]

    found: set[str] = set()
    for variant in variants:
        html = render(f"<{tag} {variant} />")
        for attribute in CLASS_ATTRIBUTE.finditer(html):
            found |= set(attribute.group("value").split())
    return found


class TestClassesComposedAtRenderTime:
    @pytest.mark.parametrize("tag", block_tags())
    def test_every_class_a_block_renders_resolves(
        self, render, blocks_classes: set[str], tag: str
    ) -> None:
        used = classes_reaching_the_dom(render, tag)
        assert used, f"{tag} rendered no classes at all"

        missing = sorted(
            token
            for token in used
            if token not in blocks_classes | HOST_PROVIDED_CLASSES
        )

        assert not missing, (
            f"{tag} renders {len(missing)} class(es) that resolve to no rule: "
            f"{', '.join(missing)}.\nAdd them to the @source inline(...) list in "
            "assets/daisy-cotton-ext.css and rebuild with `npm run build:css`."
        )

    def test_a_palette_colour_with_no_rule_behind_it_is_caught(
        self, render, blocks_classes: set[str]
    ) -> None:
        html = render('<c-background.glow from="chartreuse" />')
        rendered = {
            token
            for attribute in CLASS_ATTRIBUTE.finditer(html)
            for token in attribute.group("value").split()
        }

        missing = rendered - (blocks_classes | HOST_PROVIDED_CLASSES)

        assert missing == {"bg-chartreuse"}
