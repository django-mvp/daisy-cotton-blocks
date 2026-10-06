"""The catalogue the demo's navigation and routing are both built from.

Declared once, so a component is named in exactly one place: the sidebar, the
URLconf and the page templates all read this.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Component:
    """One block, and the page that shows it.

    Attributes:
        slug: The component's name within its family, as used in its Cotton tag
            and its URL.
        label: The name shown in the sidebar and as the page title.
        group: The heading the component is listed under within its family's
            sidebar section, or empty when the family is not divided.
    """

    slug: str
    label: str
    group: str = ""

    def tag(self, family_slug: str) -> str:
        """Return the Cotton tag this component is used as, without its brackets.

        Args:
            family_slug: The slug of the family the component belongs to.

        Returns:
            The tag, for example ``c-hero.centred``.
        """
        return f"c-{family_slug}.{self.slug}"

    def template(self, family_slug: str) -> str:
        """Return the path of the demo page that shows this component.

        Args:
            family_slug: The slug of the family the component belongs to.

        Returns:
            The template path, relative to a template root.
        """
        return f"example/components/{family_slug}/{self.slug}.html"


@dataclass(frozen=True)
class Family:
    """All the components that do the same job on a page.

    A naming convention rather than a thing in the code — there is no shared
    template and no base component behind one.

    Attributes:
        slug: The family's name, as used in its Cotton tags and URLs.
        label: The name shown as the sidebar section heading.
        components: The blocks in the family, in the order they are listed.
    """

    slug: str
    label: str
    components: tuple[Component, ...]

    def groups(self) -> list[tuple[str, list[Component]]]:
        """Return the components under their group headings, in declaration order.

        Returns:
            One (heading, components) pair per group. A family that is not
            divided comes back as a single pair with an empty heading.
        """
        grouped: dict[str, list[Component]] = {}
        for component in self.components:
            grouped.setdefault(component.group, []).append(component)
        return list(grouped.items())

    def find(self, slug: str) -> Component | None:
        """Return the component with the given slug.

        Args:
            slug: The component's name within this family.

        Returns:
            The component, or None when the family has no such component.
        """
        for component in self.components:
            if component.slug == slug:
                return component
        return None


# Only families that have blocks: each family docs/ROADMAP.md plans arrives here
# when it has something to show, not as a placeholder page.
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
            Component("glow", "Glow", group="Static"),
            Component("gradient", "Gradient", group="Static"),
            Component("grid", "Grid", group="Static"),
            Component("image", "Image", group="Static"),
            Component("parallax", "Parallax", group="Dynamic"),
            Component("aurora", "Aurora", group="Dynamic"),
            Component("flow", "Flow", group="Dynamic"),
            Component("horizon", "Horizon", group="Dynamic"),
            Component("particles", "Particles", group="Dynamic"),
            Component("hyperspace", "Hyperspace", group="Dynamic"),
        ),
    ),
    Family(
        slug="text",
        label="Text effects",
        components=(
            Component("glow", "Glow", group="Static"),
            Component("outline", "Outline", group="Static"),
            Component("depth", "Depth", group="Static"),
            Component("gradient", "Gradient", group="Dynamic"),
            Component("shimmer", "Shimmer", group="Dynamic"),
            Component("marker", "Marker", group="Dynamic"),
            Component("typewriter", "Typewriter", group="Dynamic"),
            Component("wave", "Wave", group="Dynamic"),
            Component("glitch", "Glitch", group="Dynamic"),
        ),
    ),
    Family(
        slug="reveal",
        label="Reveals",
        components=(
            Component("enter", "Enter", group="On scroll"),
            Component("cascade", "Cascade", group="On scroll"),
            Component("wipe", "Wipe", group="On scroll"),
            Component("words", "Words", group="On scroll"),
            Component("stack", "Stack", group="On scroll"),
            Component("hover", "Hover", group="On hover"),
        ),
    ),
    Family(
        slug="quote",
        label="Quotes",
        components=(
            Component("pull", "Pull", group="Components"),
            Component("mark", "Mark", group="Components"),
            Component("card", "Card", group="Components"),
            Component("bubble", "Bubble", group="Components"),
            Component("centred", "Centred", group="Blocks"),
            Component("split", "Split", group="Blocks"),
            Component("wall", "Wall", group="Blocks"),
            Component("byline", "Byline", group="Parts"),
        ),
    ),
)


def find(family_slug: str, component_slug: str) -> tuple[Family, Component] | None:
    """Return the family and component a pair of slugs names.

    Args:
        family_slug: The slug of the family.
        component_slug: The slug of the component within that family.

    Returns:
        The family and its component, or None when either slug names nothing.
    """
    for family in FAMILIES:
        if family.slug != family_slug:
            continue
        component = family.find(component_slug)
        if component is not None:
            return family, component
    return None


def every_component() -> list[tuple[Family, Component]]:
    """Return every (family, component) pair, for parametrising over the catalogue.

    Returns:
        The pairs, family by family, in declaration order.
    """
    return [
        (family, component) for family in FAMILIES for component in family.components
    ]
