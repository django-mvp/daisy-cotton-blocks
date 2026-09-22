"""Shared fixtures for the test suite."""

from collections.abc import Callable

import pytest
from django.template import engines
from django_cotton.compiler_regex import CottonCompiler


@pytest.fixture
def render() -> Callable[..., str]:
    """Render a snippet of Cotton markup and return the HTML it produces.

    Cotton compiles its tags inside a template *loader*, so markup handed
    straight to the engine keeps its `<c-...>` tags as literal text and renders
    no component at all — which reads as a block that produced nothing rather
    than as a test that never ran one. Running the compiler first is exactly
    what the loader does with a file on disk, and it lets a test state the
    markup it is about in its own body instead of keeping a fixture template
    per case somewhere else.
    """

    def _render(markup: str, **context: object) -> str:
        compiled = CottonCompiler().process(markup)
        return engines["django"].from_string(compiled).render(context)

    return _render
