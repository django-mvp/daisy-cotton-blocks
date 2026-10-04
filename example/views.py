"""Views for the example project."""

from django.http import Http404
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
        return [self.component.template(self.family.slug)]

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
