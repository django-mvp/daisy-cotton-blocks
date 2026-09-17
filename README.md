# django-mvp-bits

Page blocks for [django-mvp](https://github.com/django-mvp/django-mvp) projects — heroes, section layouts, calls to action and the rest of the furniture a public-facing page needs.

django-mvp gives you an application shell: navigation, forms, tables, CRUD views. It does not help with the pages that sit in front of the application — the landing page, the pricing page, the sign-up pitch. Those get assembled by hand out of raw utility classes, in every project, every time.

This package is optional. Installing it adds components and one stylesheet, and changes nothing about how django-mvp behaves.

## Status

Version 0.0.1. The build pipeline and the stylesheet contract are in place; the components are not written yet. Nothing here is stable.

## Requirements

- Python 3.12+
- Django 5.2 or 6.0
- django-mvp 0.23.0+

## Install

```bash
pip install django-mvp-bits
```

Add it to `INSTALLED_APPS`, after `mvp`:

```python
INSTALLED_APPS = [
    ...,
    "mvp",
    "mvp_bits",
]
```

Then load the stylesheet **after** django-mvp's:

```html
<link rel="stylesheet" href="{% static 'css/django-mvp.css' %}">
<link rel="stylesheet" href="{% static 'css/mvp-bits.css' %}">
```

Order matters and the dependency is real. This stylesheet is a supplement: it contains only the utilities django-mvp's build does not already emit, and it carries no theme of its own. On its own it styles nothing.

Components are then available in templates under the `mvp-bits` namespace:

```html
<c-mvp-bits.hero title="Ship it on Friday">
  ...
</c-mvp-bits.hero>
```

## Scope & philosophy

**What this is.** A presentation-only component library. Templates, a stylesheet, and the small amount of JavaScript some components need. Blocks are configured through attributes and themed by whatever daisyUI theme the host project runs, so a page built from them re-themes with the rest of the site and never pins a literal colour into the markup.

**What this deliberately is not.**

- **Not an application.** No models, no views, no forms, no URLs, no migrations. A component's content comes from the template author, never from a queryset. Anything that needs a model or a view mixin belongs upstream in django-mvp.
- **Not a second stylesheet.** Nothing here restates a rule django-mvp already ships. The supplement is measured against django-mvp's build on every test run and the permitted overlap is zero.
- **Not a CSS framework.** No daisyUI plugin, no theme layer, no preflight. Those come from django-mvp.
- **Not a replacement for django-mvp's components.** django-mvp owns the application chrome. This package owns the marketing surface.
- **Not a fixed catalogue.** The set of blocks grows as new ones are designed. There is no taxonomy to fill in.

**Tie-breaks.** When two of these pull against each other: additive-only beats convenience, theme-driven beats hard-coded, and a block that composes existing daisyUI markup beats one that invents its own.

## Building the stylesheet

The built CSS is committed, so installing the package needs no Node toolchain. Contributors changing the utility whitelist do:

```bash
npm install
npm run build:css     # or watch:css
```

`assets/mvp-bits.css` is the entry. Every class it emits is whitelisted there by hand — templates are not scanned, because scanning them would re-emit whatever they share with django-mvp. The whitelist has gaps that look like mistakes and are not; the file explains each one, and `tests/test_stylesheet.py` is what keeps them honest.

## License

MIT
