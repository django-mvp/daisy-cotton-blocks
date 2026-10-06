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
        kind: The sidebar section the component is listed in, ``component`` or
            ``block``, for one that differs from the rest of its family. Empty
            to take the family's.
        tag_name: The component's Cotton tag, for one whose tag is not its
            family's slug followed by its own. Empty for the usual case.
        states: The (slug, label) pairs of the states a whole-page block is
            previewed in. Only read for a family that sets ``page``.
    """

    slug: str
    label: str
    group: str = ""
    kind: str = ""
    tag_name: str = ""
    states: tuple[tuple[str, str], ...] = (
        ("default", "As it loads"),
        ("errors", "After a failed attempt"),
    )

    def tag(self, family_slug: str) -> str:
        """Return the Cotton tag this component is used as, without its brackets.

        Args:
            family_slug: The slug of the family the component belongs to.

        Returns:
            The tag, for example ``c-hero.centred``.
        """
        return self.tag_name or f"c-{family_slug}.{self.slug}"

    def template(self, family_slug: str) -> str:
        """Return the path of the demo page that shows this component.

        Args:
            family_slug: The slug of the family the component belongs to.

        Returns:
            The template path, relative to a template root.
        """
        return f"example/components/{family_slug}/{self.slug}.html"

    def preview(self, family_slug: str) -> str:
        """Return the path of the bare page that shows this block on its own.

        Args:
            family_slug: The slug of the family the component belongs to.

        Returns:
            The template path, relative to a template root.
        """
        return f"example/previews/{family_slug}/{self.slug}.html"


@dataclass(frozen=True)
class Family:
    """All the components that do the same job on a page.

    A naming convention rather than a thing in the code — there is no shared
    template and no base component behind one.

    Attributes:
        slug: The family's name, as used in its Cotton tags and URLs.
        label: The name shown as the sidebar section heading.
        components: The blocks in the family, in the order they are listed.
        kind: The sidebar section the family's components are listed in unless
            one says otherwise: ``block`` for a region of a page, ``component``
            for a single piece that goes inside one.
        page: The one demo page every component in the family is shown on, for
            a family of whole-page blocks that are previewed in a frame. Empty
            when each component has a demo page of its own.
    """

    slug: str
    label: str
    components: tuple[Component, ...]
    kind: str = "component"
    page: str = ""

    def kind_of(self, component: Component) -> str:
        """Return the sidebar section a component of this family is listed in.

        Args:
            component: A component of this family.

        Returns:
            The component's own kind, or the family's when it names none.
        """
        return component.kind or self.kind

    def groups(self, kind: str = "") -> list[tuple[str, list[Component]]]:
        """Return the components under their group headings, in declaration order.

        Args:
            kind: Keep only the components listed in this sidebar section.
                Empty keeps them all.

        Returns:
            One (heading, components) pair per group. A family that is not
            divided comes back as a single pair with an empty heading.
        """
        grouped: dict[str, list[Component]] = {}
        for component in self.components:
            if kind and self.kind_of(component) != kind:
                continue
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
        slug="section",
        label="Section",
        kind="block",
        components=(
            Component("section", "Section", tag_name="c-section"),
            Component("col", "Column", tag_name="c-section.col"),
        ),
    ),
    Family(
        slug="hero",
        label="Heroes",
        kind="block",
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
            Component("centred", "Centred", group="Blocks", kind="block"),
            Component("split", "Split", group="Blocks", kind="block"),
            Component("wall", "Wall", group="Blocks", kind="block"),
            Component("byline", "Byline", group="Parts"),
        ),
    ),
    Family(
        slug="stats",
        label="Stats",
        components=(
            Component("trend", "Stacked", group="Trend layouts"),
            Component("trend-inline", "Inline", group="Trend layouts"),
            Component("trend-corner", "Corner", group="Trend layouts"),
            Component("trend-centred", "Centred", group="Trend layouts"),
            Component("trend-footer", "Footer", group="Trend layouts"),
            Component("trend-row", "Row", group="Trend layouts"),
            Component("progress", "Progress", group="Other figures"),
            Component("count", "Count up", group="Other figures"),
            Component("change", "Change", group="Parts"),
            Component("band", "Band", group="Sections", kind="block"),
            Component("split", "Split", group="Sections", kind="block"),
            Component("headline", "Headline", group="Sections", kind="block"),
        ),
    ),
    Family(
        slug="parts",
        label="Page parts",
        kind="component",
        components=(
            Component("heading", "Heading", tag_name="c-heading"),
            Component("points", "Points", tag_name="c-points"),
            Component("panel", "Sign-in panel", tag_name="c-auth.panel"),
        ),
    ),
    Family(
        slug="sign-in",
        label="Sign in",
        kind="block",
        page="example/entrance_page.html",
        components=(
            Component("centred", "Centred"),
            Component("split", "Split"),
            Component("floating", "Floating"),
            Component(
                "stepped",
                "Stepped",
                states=(
                    ("email", "First question"),
                    ("method", "Second question"),
                    ("errors", "After a failed attempt"),
                ),
            ),
            Component("providers", "Providers first"),
        ),
    ),
    Family(
        slug="sign-up",
        label="Sign up",
        kind="block",
        page="example/entrance_page.html",
        components=(
            Component("pitch", "Pitch"),
            Component("showcase", "Showcase"),
            Component("bento", "Bento"),
            Component(
                "stepped",
                "Stepped",
                states=(
                    ("details", "First step"),
                    ("verify", "Second step"),
                    ("errors", "After a failed attempt"),
                ),
            ),
        ),
    ),
)

# The sidebar sections, in the order they are listed, and the kind each holds.
SECTIONS: tuple[tuple[str, str], ...] = (
    ("component", "Components"),
    ("block", "Sections"),
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
