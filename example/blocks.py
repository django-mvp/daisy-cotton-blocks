"""The catalogue the demo's navigation and routing are both built from.

Declared once, so a component is named in exactly one place: the sidebar, the
URLconf and the page templates all read this.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Component:
    """One block, and the page that shows it."""

    slug: str
    label: str

    def tag(self, family_slug: str) -> str:
        """The Cotton tag this component is used as, without its brackets."""
        return f"c-{family_slug}.{self.slug}"

    def template(self, family_slug: str) -> str:
        """The demo page that shows it."""
        return f"example/components/{family_slug}/{self.slug}.html"


@dataclass(frozen=True)
class Family:
    """All the components that do the same job on a page.

    A naming convention rather than a thing in the code — there is no shared
    template and no base component behind one.
    """

    slug: str
    label: str
    components: tuple[Component, ...]

    def find(self, slug: str) -> Component | None:
        for component in self.components:
            if component.slug == slug:
                return component
        return None


# Only the families that have blocks. The roadmap plans nine more, and each one
# arrives here when it has something to show rather than holding a placeholder
# page that says it does not.
FAMILIES: tuple[Family, ...] = (
    Family(
        slug="hero",
        label="Hero sections",
        components=(
            Component("centred", "Centred"),
            Component("split", "Split"),
            Component("showcase", "Showcase"),
            Component("highlight", "Highlight"),
        ),
    ),
    Family(
        slug="background",
        label="Backgrounds",
        components=(
            Component("glow", "Glow"),
            Component("gradient", "Gradient"),
            Component("grid", "Grid"),
            Component("image", "Image"),
        ),
    ),
)


def find(family_slug: str, component_slug: str) -> tuple[Family, Component] | None:
    """The family and component a pair of slugs names, or None."""
    for family in FAMILIES:
        if family.slug != family_slug:
            continue
        component = family.find(component_slug)
        if component is not None:
            return family, component
    return None


def every_component() -> list[tuple[Family, Component]]:
    """Every (family, component) pair, for parametrising over the catalogue."""
    return [
        (family, component) for family in FAMILIES for component in family.components
    ]
