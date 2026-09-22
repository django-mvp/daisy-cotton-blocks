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
from django_cotton_gallery.core.annotations import AnnotationParser

BLOCKS_STYLESHEET = "css/daisy-cotton-blocks.css"
HOST_STYLESHEET = "css/django-mvp.css"

CLASS_TOKEN = re.compile(r"\.((?:[A-Za-z0-9_-]|\\.)+)")

# Anchored to the repo root rather than the working directory, so the scan
# finds the same templates however pytest was invoked.
REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_TEMPLATES = REPO_ROOT / "daisy_cotton_blocks" / "templates"
EXAMPLE_TEMPLATES = REPO_ROOT / "example" / "templates"

# The closing quote is the same character as the opening one, never whichever
# quote turns up first. A branch comparing against a string literal --
# `{% if size == 'sm' %}` -- puts single quotes inside a double-quoted
# attribute, and ending the match at the first of those silently drops every
# class after it.
CLASS_ATTRIBUTE = re.compile(
    r"""\bclass\s*=\s*(?P<quote>["'])(?P<value>.*?)(?P=quote)""", re.S
)

TEMPLATE_TAG = re.compile(r"\{%.*?%\}", re.S)
TEMPLATE_VARIABLE = re.compile(r"\{\{.*?\}\}", re.S)

# Stands in for a value only the renderer knows, and is not a character any
# class name may contain, so a token that kept one is a token that was still
# being assembled when the source ran out.
COMPOSED_AT_RENDER_TIME = "\x00"

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


def literal_classes(attribute: str) -> list[str]:
    """The class tokens in ``attribute`` that are written out in the source.

    Template syntax is stripped rather than treated as a reason to give up on
    the attribute, because a block that varies its surface or its spacing puts
    the syntax and the classes in the same attribute:

        class="relative isolate
               {% if invert %}text-neutral-content{% else %}text-base-content{% endif %}"

    The two kinds of syntax are stripped differently, and that difference is
    the whole of this function.

    A ``{% ... %}`` tag writes no text of its own, so it is a boundary between
    tokens: the classes in each branch of an ``{% if %}`` are whole names and
    can each be looked up. Replacing it with a space is what keeps the last
    class of one branch from running into the first of the next.

    A ``{{ ... }}`` does write text, so a token touching one is finished at
    render time and reading the source cannot say what it becomes. Those are
    dropped, and covering them is what the ``@source inline(...)`` list in
    assets/daisy-cotton-blocks.css is for.
    """
    text = TEMPLATE_TAG.sub(" ", attribute)
    text = TEMPLATE_VARIABLE.sub(COMPOSED_AT_RENDER_TIME, text)
    return [token for token in text.split() if COMPOSED_AT_RENDER_TIME not in token]


def template_classes(root: Path) -> dict[str, set[str]]:
    """Every literal class token the templates under ``root`` ask for.

    Keyed by class, valued by the templates using it, so a failure names the
    file to go and look at. Paths are shown relative to the repository when
    they sit inside it, which the scan roots that matter do.
    """
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
    """The classes in ``used`` that ``available`` has no rule for."""
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
    """What `template_classes` reads out of an attribute, and what it leaves alone.

    Blocks branch on their attributes, so nearly every class attribute a block
    writes carries template syntax somewhere in it. A scanner that gave up on
    the whole attribute would walk every block in the package and check none of
    them, which looks exactly like a suite that is passing.
    """

    def scan(self, tmp_path: Path, markup: str) -> dict[str, set[str]]:
        (tmp_path / "block.html").write_text(markup, encoding="utf-8")
        return template_classes(tmp_path)

    def test_a_literal_class_beside_template_syntax_is_read(
        self, tmp_path: Path
    ) -> None:
        found = self.scan(tmp_path, '<section class="isolate {{ class }}">')
        assert "isolate" in found

    def test_both_branches_of_a_conditional_are_read(self, tmp_path: Path) -> None:
        """A dead class hides in whichever branch nobody is looking at."""
        found = self.scan(
            tmp_path,
            '<section class="{% if invert %}text-neutral-content'
            '{% else %}text-base-content{% endif %}">',
        )
        assert {"text-neutral-content", "text-base-content"} <= set(found)

    def test_two_branches_do_not_fuse_into_one_token(self, tmp_path: Path) -> None:
        """`{% endif %}` separates them in the source and has to separate them here.

        Dropping a tag without putting something in its place runs the last
        class of one branch into the first of the next, and the invented token
        that makes resolves to no rule — a failure report naming a class that
        appears nowhere in the template it blames.
        """
        found = self.scan(
            tmp_path,
            '<section class="{% if a %}py-12{% endif %}{% if b %}py-16{% endif %}">',
        )
        assert {"py-12", "py-16"} <= set(found)
        assert "py-12py-16" not in found

    def test_a_class_after_a_quoted_comparison_is_read(self, tmp_path: Path) -> None:
        """The comparison's own quotes are not the end of the attribute."""
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
        """Reading the source cannot say what `text-{{ tone }}-content` becomes.

        Half a class name is worse than no class name: it would be reported as
        missing on every build, and the way to quiet it would be to emit a rule
        for a class that never reaches the DOM.
        """
        found = self.scan(tmp_path, '<section class="isolate text-{{ tone }}-content">')
        assert set(found) == {"isolate"}

    def test_a_template_is_named_by_the_classes_it_uses(self, tmp_path: Path) -> None:
        """The report is only actionable if it says where to go and look."""
        found = self.scan(tmp_path, '<section class="isolate">')
        assert found["isolate"] == {str(tmp_path / "block.html")}


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
        """The guard on rule 2 of the stylesheet contract: no daisyUI plugin.

        Plain Tailwind cannot emit `btn` however it is configured, so what this
        catches is someone adding `@plugin "daisyui"` to the entry — the one
        change that would make this package ship a second definition of every
        component the host already styles, with link order deciding which wins.
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
        assert used, "no template classes were found to check — the scanner is broken"

        missing = unresolved_classes(used, blocks_classes | HOST_PROVIDED_CLASSES)
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

        missing = unresolved_classes(used, blocks_classes | host_classes)
        assert not missing, report_missing(missing)

    def test_a_dead_class_in_a_conditional_branch_is_caught(
        self, tmp_path: Path, blocks_classes: set[str]
    ) -> None:
        """The check above, run against the defect it exists to catch.

        Written against markup of its own rather than a block, because the
        check is only evidence of anything once it has been shown to go red,
        and every block in the package is expected to keep it green.
        """
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
    """Every block the package ships, as the Cotton tag it is used as."""
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
    """Every class the block puts in the DOM, across the values it accepts.

    Rendered once with its defaults and then once per declared option, rather
    than combinatorially: each option writes its own class independently of the
    others, so one variant per option covers every branch that composes one.
    """
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
    """The classes the source scan above deliberately cannot see.

    A background takes a palette colour as an attribute and assembles
    `bg-{{ from }}` while it renders. Reading the template cannot say what that
    becomes, so those classes are covered by the `@source inline(...)` list in
    assets/daisy-cotton-blocks.css instead — and naming a class in that list is
    not proof that it produces a rule. A colour utility whose palette entry is
    missing from the `@theme reference` block builds to nothing at all, and the
    page that results renders markup with no styling attached to it.

    So this renders each block across every value its own annotations declare
    and checks what actually lands in the DOM, which is the only thing that
    settles the question.
    """

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
            "assets/daisy-cotton-blocks.css and rebuild with `npm run build:css`."
        )

    def test_a_palette_colour_with_no_rule_behind_it_is_caught(
        self, render, blocks_classes: set[str]
    ) -> None:
        """The check above, run against the defect it exists to catch.

        `chartreuse` is not one of daisyUI's colours and nothing emits a rule
        for it, which is exactly the shape of the failure: an attribute value
        composes a class name, the class name reaches the DOM, and no rule
        matches it.
        """
        html = render('<c-background.glow from="chartreuse" />')
        rendered = {
            token
            for attribute in CLASS_ATTRIBUTE.finditer(html)
            for token in attribute.group("value").split()
        }

        missing = rendered - (blocks_classes | HOST_PROVIDED_CLASSES)

        assert missing == {"bg-chartreuse"}
