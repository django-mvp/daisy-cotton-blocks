# daisy-cotton-blocks

Page blocks for Django projects running [django-cotton](https://django-cotton.com/) and [daisyUI](https://daisyui.com/) — heroes, section layouts, calls to action and the rest of the furniture a public-facing page needs.

Component libraries in this space cover the application: navigation, forms, tables, dialogs. They stop at the pages that sit in front of it — the landing page, the pricing page, the sign-up pitch. Those get assembled by hand out of raw utility classes, in every project, every time.

Blocks are configured through attributes and take their colours from whatever daisyUI theme the project already runs, so a page built from them re-themes with the rest of the site.

## Status

Version 0.0.1. The build pipeline and the stylesheet contract are in place; the blocks are not written yet. Nothing here is stable.

## Requirements

- Python 3.12+
- Django 5.2 or 6.0
- django-cotton 2.6+
- daisyUI 5, loaded by the project

daisyUI is a hard requirement and this package does not ship it. Any project already running daisyUI satisfies it, whether through its own Tailwind build or through a package that provides one, such as [django-mvp](https://github.com/django-mvp/django-mvp).

## Install

```bash
pip install daisy-cotton-blocks
```

Add it to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...,
    "django_cotton",
    "daisy_cotton_blocks",
]
```

Then load its stylesheet alongside the one carrying daisyUI:

```html
<link rel="stylesheet" href="{% static 'css/your-daisyui-build.css' %}">
<link rel="stylesheet" href="{% static 'css/daisy-cotton-blocks.css' %}">
```

The two stylesheets do different jobs. Yours carries daisyUI, its themes and Tailwind's preflight. This one carries the plain Tailwind utilities the blocks need and which your build has no way to know about, because it scans your source and these templates live in site-packages. Some rules will appear in both, which costs bytes and nothing else.

Blocks are then available as Cotton tags:

```html
<c-hero.centred title="Ship it on Friday">
  ...
</c-hero.centred>
```

## Scope & philosophy

**What this is.** A presentation-only component library. Templates, a stylesheet, and the small amount of JavaScript some blocks need. Blocks are configured through attributes and themed by whatever daisyUI theme the project runs, so a page built from them never pins a literal colour into the markup.

**What this deliberately is not.**

- **Not an application.** No models, no views, no forms, no URLs, no migrations. A block's content comes from the template author, never from a queryset.
- **Not a CSS framework.** No daisyUI plugin, no theme layer, no preflight. Those come from the project.
- **Not an application component library.** Navigation, forms, tables and dialogs are somebody else's job. This package owns the marketing surface.
- **Not a fixed catalogue.** The set of blocks grows as new ones are designed. There is no taxonomy to fill in.
- **Not page templates.** Blocks only. You pick the ones you want and assemble the page yourself. There is no one-tag landing page.

**Tie-breaks.** When two of these pull against each other: theme-driven beats hard-coded, a block that composes existing daisyUI markup beats one that invents its own, and leaving a job to the project beats doing it here.

The directions the package works toward are in [GOALS.md](https://github.com/django-mvp/daisy-cotton-blocks/blob/main/GOALS.md).

## Building the stylesheet

The built CSS is committed, so installing the package needs no Node toolchain. Contributors changing what it emits do:

```bash
npm install
npm run build:css     # or watch:css
```

`assets/daisy-cotton-blocks.css` is the entry. It scans this package's own templates, so a utility a new block uses is picked up by rebuilding. The `@source inline(...)` entries alongside cover what scanning cannot see: classes composed at render time, and the utilities the first blocks are being designed against. `tests/test_stylesheet.py` measures the result.

## License

MIT
