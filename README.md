# daisy-cotton-blocks

Page blocks for Django projects running [django-cotton](https://django-cotton.com/) and [daisyUI](https://daisyui.com/) — heroes, section layouts, calls to action and the rest of the furniture a public-facing page needs.

Component libraries in this space cover the application: navigation, forms, tables, dialogs. They stop at the pages that sit in front of it — the landing page, the pricing page, the sign-up pitch. Those get assembled by hand out of raw utility classes, in every project, every time.

Blocks are configured through attributes and take their colours from whatever daisyUI theme the project already runs, so a page built from them re-themes with the rest of the site.

## Status

Version 0.0.1. Two families are built, heroes and backgrounds, and nothing here is stable. Block names, attributes and the set of classes the stylesheet emits all change between minor versions, and the [CHANGELOG](CHANGELOG.md) is how a project finds out.

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

## Blocks

### Heroes

Three arrangements and one inline helper. A different arrangement is a different tag rather than an option on one component, so moving a page from one to another is a one-word change.

| Tag | What it is |
|---|---|
| `<c-hero.centred>` | One column, centred. The opener for a page whose words are the product. |
| `<c-hero.split>` | Copy beside a visual, stacking to one column below `lg`. |
| `<c-hero.showcase>` | Centred copy over a wide, lifted product panel. |
| `<c-hero.highlight>` | An inline span that fills the words it wraps with one of daisyUI's colour pairs. Headings only. |

The three arrangements take the same attributes:

| Attribute | Default | What it does |
|---|---|---|
| `eyebrow` | — | A short line above the heading: a category, a release name |
| `title` | — | The heading |
| `lead` | — | The supporting sentence under it |
| `level` | `1` | Heading level, so a page carrying two heroes keeps a real heading order |
| `invert` | off | Light copy, for a dark background |
| `size` | `md` | How much vertical room the block takes: `sm`, `md`, `lg`, and `screen` on the centred arrangement |
| `class` | — | Extra classes on the outer section. A plain surface colour goes here: `bg-base-200` |
| `reverse` | off | Split only. Mirrors the two columns at `lg` and above |

And the same slots. Anything you pass that is not listed above is forwarded to the section element, so `id`, `data-` attributes and the rest reach the markup untouched.

| Slot | What goes in it |
|---|---|
| `background` | A background block, rendered into a layer behind the copy |
| `announcement` | Above the eyebrow. A pill linking to the latest release, usually |
| `actions` | The button row. Write real anchor or button markup, so it can post, submit or carry anything |
| `footnote` | Under the actions. A trust line, a rating, a row of logos |
| `media` | Split and showcase only. The picture beside or below the copy |

### Backgrounds

A background is not part of a layout, so it is not part of a block. Each one is its own block that goes in another block's `background` slot, which means any background composes with any layout.

| Tag | What it draws | Attributes |
|---|---|---|
| `<c-background.glow>` | Two heavily blurred discs of the theme's colours | `from`, `to`, `intensity` |
| `<c-background.gradient>` | A wash between two palette colours | `from`, `via`, `to`, `direction`, `opacity` |
| `<c-background.grid>` | A faint ruled grid | `size`, `intensity`, `flat` |
| `<c-background.image>` | A picture, dimmed by the theme's `neutral` | `src`, `dim`, `position` |

Two things to know about them. A background belongs in a `background` slot and nowhere else, because it positions itself against that slot's wrapper rather than filling its parent in normal flow. And a dark background needs `invert` on the block, since a background cannot reach up to recolour its sibling. Each block's page says whether it wants one.

```html
<c-hero.centred title="Ship the page, not the CSS"
                lead="Blocks for the pages in front of your app."
                invert>
  <c-slot name="background">
    <c-background.image src="{% static 'img/desk.jpg' %}" dim="strong" />
  </c-slot>
  <c-slot name="actions">
    <a class="btn btn-primary btn-lg" href="{% url 'signup' %}">Get started</a>
  </c-slot>
</c-hero.centred>
```

Every attribute, its accepted values and its default are listed on each block's own page in the example project, built from the annotations in the block's template. Run it with `python manage.py runserver` from a checkout.

## Scope & philosophy

**What this is.** A presentation-only component library. Templates, a stylesheet, and the small amount of JavaScript some blocks need. Blocks are configured through attributes and themed by whatever daisyUI theme the project runs, so a page built from them never pins a literal colour into the markup.

**What this deliberately is not.**

- **Not an application.** No models, no views, no forms, no URLs, no migrations. A block's content comes from the template author, never from a queryset.
- **Not a CSS framework.** No daisyUI plugin, no theme layer, no preflight. Those come from the project.
- **Not an application component library.** Navigation, forms, tables and dialogs are somebody else's job. This package owns the marketing surface.
- **Not a fixed catalogue.** The set of blocks grows as new ones are designed. There is no taxonomy to fill in.
- **Not page templates.** Blocks only. You pick the ones you want and assemble the page yourself. There is no one-tag landing page.

**Tie-breaks.** When two of these pull against each other: theme-driven beats hard-coded, a block that composes existing daisyUI markup beats one that invents its own, and leaving a job to the project beats doing it here.

The directions the package works toward are in [GOALS.md](https://github.com/django-mvp/daisy-cotton-blocks/blob/main/GOALS.md), and the order they are being built in is in the [roadmap](https://github.com/django-mvp/daisy-cotton-blocks/blob/main/docs/ROADMAP.md).

## Building the stylesheet

The built CSS is committed, so installing the package needs no Node toolchain. Contributors changing what it emits do:

```bash
npm install
npm run build:css     # or watch:css
```

`assets/daisy-cotton-blocks.css` is the entry. It scans this package's own templates, so a utility a new block uses is picked up by rebuilding. The `@source inline(...)` entries alongside cover what scanning cannot see: classes composed at render time, and the utilities the first blocks are being designed against. `tests/test_stylesheet.py` measures the result.

## License

MIT
