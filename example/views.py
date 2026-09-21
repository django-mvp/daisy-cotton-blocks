from django.http import Http404
from django.template import TemplateDoesNotExist
from django.template.loader import select_template
from mvp.views import MVPTemplateView

from example import blocks


class HomeView(MVPTemplateView):
    """What this package is, for somebody arriving at the demo cold."""

    template_name = "example/home.html"
    page_title = "daisy-cotton-blocks"
    page_subtitle = "Page blocks for Django projects running Cotton and daisyUI"


class GroupView(MVPTemplateView):
    """One block family: its catalogue page, or a placeholder until it has one.

    A family gets a page as soon as somebody writes
    ``example/families/<slug>.html``. Until then the view carries no template
    at all, and django-mvp defaults an unconfigured template to a packaged
    placeholder, so the page renders the shell and says plainly that nothing is
    wired up yet — which is the honest state of every family that has no blocks.
    """

    def get_template_names(self) -> list[str]:
        catalogue = f"example/families/{self.kwargs['slug']}.html"
        try:
            select_template([catalogue])
        except TemplateDoesNotExist:
            return super().get_template_names()
        return [catalogue]

    def get_page_title(self) -> str:
        return self.kwargs["label"]

    def dispatch(self, request, *args, **kwargs):
        label = blocks.planned_family(kwargs["slug"])
        if label is None:
            raise Http404(f"no block family named {kwargs['slug']}")
        kwargs["label"] = label
        self.kwargs["label"] = label
        return super().dispatch(request, *args, **kwargs)
