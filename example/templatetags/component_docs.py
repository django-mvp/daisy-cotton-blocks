"""Render a component's own annotations as a reference table.

Every block carries `@description`, `@prop` and `@slot` comments, which the
component gallery reads to build its live controls and its lint report. This
tag reads the same comments and renders them into the demo page for that
component, so the page and the gallery cannot disagree about what a block
accepts — and so a prop is documented in exactly one place, next to the markup
it configures.

The parsing is django-cotton-gallery's, not a second implementation of the
annotation format. A parser of our own would drift from the one the linter
enforces, and the first symptom would be a demo page quietly describing an
attribute that no longer exists. `AnnotationParser` is pure — no I/O, no Django
imports — so it works here without the gallery being an installed app, which
keeps the test settings free of the gallery's startup banner.

This is demo scaffolding. It lives in the example project rather than the
package because reading a template's source at render time is a documentation
concern, and the package ships presentation only.
"""

from __future__ import annotations

from pathlib import Path

from django import template
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django_cotton_gallery.core.annotations import AnnotationParser
from django_cotton_gallery.core.schemas import ParsedComponent

register = template.Library()

parser = AnnotationParser()


def template_name(tag: str) -> str:
    """The template a Cotton tag resolves to.

    ``c-hero.centred`` and ``<c-hero.centred>`` both give
    ``cotton/hero/centred.html``, which is the path Cotton itself would load.
    Accepting the bracketed form too, because that is how a tag is written
    everywhere else on these pages and requiring one spelling would be a
    detail for the page author to get wrong.
    """
    name = tag.strip().removeprefix("<").removesuffix(">").removeprefix("c-")
    return f"cotton/{name.replace('.', '/')}.html"


def parse(tag: str) -> ParsedComponent | None:
    """Parse the annotations on the component a Cotton tag names.

    Resolved through Django's own loader rather than by walking the package
    directory, so the file read is the same one Cotton would render — including
    when a project has shadowed it with its own.
    """
    try:
        found = get_template(template_name(tag))
    except TemplateDoesNotExist:
        return None
    if found.origin is None or found.origin.name is None:
        return None
    return parser.parse(Path(found.origin.name).read_text(encoding="utf-8"))


@register.inclusion_tag("example/component_docs.html")
def component_docs(tag: str) -> dict[str, object]:
    """Render the reference tables for one component.

    Renders nothing at all when the component cannot be found or carries no
    annotations, rather than an empty heading over an empty table: a component
    with nothing documented should read as undocumented, not as documented
    with nothing in it.
    """
    return {"tag": tag, "component": parse(tag)}


@register.simple_tag
def component_description(tag: str) -> str:
    """The one-line `@description`, for use as a page's own summary.

    Separate from the tables so a page can lead with the sentence the component
    describes itself by, instead of a second one written by hand that drifts.
    """
    component = parse(tag)
    return component.description if component else ""
