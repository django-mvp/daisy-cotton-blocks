"""Views for the example project."""

from pathlib import Path

from django.conf import settings
from django.http import Http404
from django.template.loader import get_template
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.generic import TemplateView
from mvp.views import MVPTemplateView

from example import blocks

# What each family is for, in the words of the front page. Keyed by the family's
# slug, then by the sidebar section the sentence is shown under.
SUMMARIES: dict[str, dict[str, str]] = {
    "hero": {
        "block": "The opening of a page: centred, split beside a visual, or over a product panel."
    },
    "section": {
        "block": "The shell the others are built in: a background, a width and columns that stack."
    },
    "quote": {
        "component": "A quotation as a card, a bubble, a pull quote or under one oversized mark.",
        "block": "One quotation across the page, beside a portrait, or a wall of many.",
    },
    "stats": {
        "component": "A figure with its trend, its progress towards a target, or counting up.",
        "block": "A band of figures, figures beside the case they back, or one headline number.",
    },
    "sign-in": {
        "block": "Five frames for a sign-in form. The form stays your application's."
    },
    "sign-up": {"block": "Four sign-up pages that put the pitch beside the form."},
    "background": {
        "component": "Glows, gradients, grids and moving layers, in the theme's own colours."
    },
    "text": {
        "component": "Gradient, glow, marker, typewriter and other treatments for a few words."
    },
    "reveal": {
        "component": "Content that arrives, cascades or lights up as it scrolls into view."
    },
    "parts": {
        "component": "The heading, the list of points and the sign-in panel the blocks share."
    },
}


# The sentence under each kind's heading on the front page.
LEADS: dict[str, str] = {
    "component": "Single pieces, for a page you lay out yourself.",
    "block": "Whole regions of a page, ready to drop in.",
}


class HomeView(TemplateView):
    """The project's front page, built from the package's own components.

    A page with no demo shell around it, as a project's own landing page would
    be. Its figures and its index of families are read from the catalogue, so
    neither can fall behind what the demo actually shows.
    """

    template_name = "example/home.html"

    def get_context_data(self, **kwargs):
        """Add the catalogue's counts and its families under each kind."""
        context = super().get_context_data(**kwargs)
        every = blocks.every_component()
        context["component_count"] = len(every)
        context["family_count"] = len(blocks.FAMILIES)
        context["background_count"] = sum(f.slug == "background" for f, c in every)
        context["text_count"] = sum(f.slug == "text" for f, c in every)
        context["catalogue"] = [
            {"label": label, "lead": LEADS[kind], "families": self.families(kind)}
            for kind, label in blocks.SECTIONS
        ]
        first_family, first_component = every[0]
        context["catalogue_url"] = reverse(
            "component",
            kwargs={"family": first_family.slug, "component": first_component.slug},
        )
        context["gallery_url"] = (
            reverse("django_cotton_gallery:index") if settings.DEBUG else ""
        )
        return context

    def families(self, kind: str) -> list[dict[str, str]]:
        """Return the families with a component of this kind, and where each starts.

        Args:
            kind: The sidebar section, ``component`` or ``block``.

        Returns:
            One entry per family: its label, its summary and the URL of its
            first component of that kind.
        """
        entries = []
        for family in blocks.FAMILIES:
            groups = family.groups(kind)
            if not groups:
                continue
            first = groups[0][1][0]
            entries.append(
                {
                    "label": family.label,
                    "summary": SUMMARIES.get(family.slug, {}).get(kind, ""),
                    "url": reverse(
                        "component",
                        kwargs={"family": family.slug, "component": first.slug},
                    ),
                }
            )
        return entries


class ComponentView(MVPTemplateView):
    """One block, shown live with the markup that produced it.

    A page per component rather than per family: a family page grew a section
    per block and every block after the first was below the fold, which is the
    wrong shape for something whose whole job is to be looked at.
    """

    def get_template_names(self) -> list[str]:
        """Use the demo page of the requested component."""
        if self.family.page:
            return [self.family.page]
        return [self.component.template(self.family.slug)]

    def get_context_data(self, **kwargs):
        """Add the family and component, and a whole-page block's preview source."""
        context = super().get_context_data(**kwargs)
        context["family"] = self.family
        context["component"] = self.component
        context["tag"] = self.component.tag(self.family.slug)
        if self.family.page:
            preview = get_template(self.component.preview(self.family.slug))
            context["source"] = Path(preview.origin.name).read_text(encoding="utf-8")
        return context

    def get_page_title(self) -> str:
        """Title the page with the component's label."""
        return self.component.label

    def dispatch(self, request, *args, **kwargs):
        """Resolve the family and component from the URL, or answer 404."""
        found = blocks.find(kwargs["family"], kwargs["component"])
        if found is None:
            raise Http404(
                f"no component named {kwargs['family']}.{kwargs['component']}"
            )
        self.family, self.component = found
        return super().dispatch(request, *args, **kwargs)


@method_decorator(xframe_options_sameorigin, name="dispatch")
class PreviewView(TemplateView):
    """A whole-page block on a page of its own, with no demo shell around it.

    A sign-in page fills the screen and answers to the width of the screen, so
    it is judged in a frame of its own rather than inside the sidebar layout.
    The state comes from the query string, and posting the stand-in form lands
    on whichever state its action names, which is how the error state is reached.
    """

    def get_template_names(self) -> list[str]:
        """Use the preview page of the requested component."""
        return [self.component.preview(self.family.slug)]

    def get_context_data(self, **kwargs):
        """Add the state the block is previewed in, defaulting to its first."""
        context = super().get_context_data(**kwargs)
        known = [slug for slug, label in self.component.states]
        requested = self.request.GET.get("state", "")
        context["state"] = requested if requested in known else known[0]
        context["failed"] = context["state"] == "errors"
        context["component"] = self.component
        return context

    def post(self, request, *args, **kwargs):
        """Answer a post of the stand-in form with the page itself."""
        return self.get(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """Resolve the family and component from the URL, or answer 404."""
        found = blocks.find(kwargs["family"], kwargs["component"])
        if found is None or not found[0].page:
            raise Http404(f"no preview of {kwargs['family']}.{kwargs['component']}")
        self.family, self.component = found
        return super().dispatch(request, *args, **kwargs)
