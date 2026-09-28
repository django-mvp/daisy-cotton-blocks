"""Shared fixtures for the test suite."""

from collections.abc import Callable

import pytest
from django.template import engines
from django_cotton.compiler_regex import CottonCompiler


@pytest.fixture
def render() -> Callable[..., str]:
    def _render(markup: str, **context: object) -> str:
        compiled = CottonCompiler().process(markup)
        return engines["django"].from_string(compiled).render(context)

    return _render
