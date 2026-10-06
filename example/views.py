"""Views for the example project."""

from pathlib import Path

from django.http import Http404
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.generic import TemplateView
from mvp.views import MVPTemplateView

from example import blocks


class HomeView(MVPTemplateView):
    """What this package is, for somebody arriving at the demo cold."""

    template_name = "example/home.html"
    page_title = "daisy-cotton-ext"
    page_subtitle = "Extended components and page blocks for Django projects running Cotton and daisyUI"


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
