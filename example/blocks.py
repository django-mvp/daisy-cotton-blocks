"""The block families this package has, or plans.

Declared once and used to build both the sidebar and the placeholder pages, so
a family is named in exactly one place.
"""

# The slugs are the demo's, not the package's. What a family's tag ends up
# being called is settled when that family is designed, and one name is
# already ruled out: a family called "section" would render as
# <c-section.something>, which collides with the component of that name in
# django-mvp and in most other component libraries. Hence "content".
#
# Backgrounds are the one entry the roadmap does not name. They fell out of
# designing the heroes: a background is not part of a layout, so it became its
# own family that composes with every other one. The roadmap item covering it
# is still to be written.
PLANNED_FAMILIES: tuple[tuple[str, str], ...] = (
    ("hero", "Hero"),
    ("background", "Backgrounds"),
    ("content", "Content sections"),
    ("cta", "Calls to action"),
    ("pricing", "Pricing"),
    ("testimonial", "Testimonials"),
    ("logos", "Logo clouds"),
    ("stats", "Statistics"),
    ("team", "Team"),
    ("faq", "Questions and answers"),
    ("footer", "Footers"),
    ("banner", "Announcement bars"),
    ("contact", "Contact"),
    ("newsletter", "Newsletter"),
)


def planned_family(slug: str) -> str | None:
    """The label for a planned family slug, or None if it is not one."""
    for family_slug, label in PLANNED_FAMILIES:
        if family_slug == slug:
            return label
    return None
