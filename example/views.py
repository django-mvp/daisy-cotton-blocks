from django.http import Http404
from mvp.views import MVPTemplateView

from example import blocks


class HomeView(MVPTemplateView):
    """What this package is, for somebody arriving at the demo cold."""

    template_name = "example/home.html"
    page_title = "daisy-cotton-blocks"
    page_subtitle = "Page blocks for Django projects running Cotton and daisyUI"


class GroupView(MVPTemplateView):
    """One planned block family, holding its place until it has blocks.

    Deliberately carries no template of its own. django-mvp defaults an
    unconfigured template to a packaged placeholder, so these pages render the
    shell and say plainly that nothing is wired up yet, which is the honest
    state of every one of them right now.
    """

    def get_page_title(self) -> str:
        return self.kwargs["label"]

    def dispatch(self, request, *args, **kwargs):
        label = blocks.planned_family(kwargs["slug"])
        if label is None:
            raise Http404(f"no block family named {kwargs['slug']}")
        kwargs["label"] = label
        self.kwargs["label"] = label
        return super().dispatch(request, *args, **kwargs)
