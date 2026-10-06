"""Filters for the text effects that take a line apart."""

from html import unescape

from django import template
from django.utils.safestring import SafeData

register = template.Library()


@register.filter
def plain(value: object) -> str:
    """Return a line as the characters a reader sees, with any escaping undone.

    An attribute written as ``text="{{ title }}"`` reaches a component already
    escaped, and one written as ``:text="title"`` does not. Split into letters,
    the first would put ``&amp;`` on the page as five of them.

    Args:
        value: The line, as the component was given it.

    Returns:
        The line as an ordinary string, which a template escapes again wherever
        it writes it out.
    """
    text = str(value)
    return unescape(text) if isinstance(value, SafeData) else text
