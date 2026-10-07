# daisy-cotton-ext

[![Tests](https://github.com/django-mvp/daisy-cotton-ext/actions/workflows/tests.yml/badge.svg)](https://github.com/django-mvp/daisy-cotton-ext/actions/workflows/tests.yml) [![Coverage](https://codecov.io/gh/django-mvp/daisy-cotton-ext/branch/main/graph/badge.svg)](https://codecov.io/gh/django-mvp/daisy-cotton-ext) ![Python 3.12 | 3.13](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue) ![Django 5.2 | 6.0 | 6.1](https://img.shields.io/badge/django-5.2%20%7C%206.0%20%7C%206.1-blue) [![License: MIT](https://img.shields.io/badge/license-MIT-green)](https://github.com/django-mvp/daisy-cotton-ext/blob/main/LICENSE)

Extended components and page blocks for django-cotton and daisyUI.

Built on [django-cotton](https://django-cotton.com/) and [daisyUI](https://daisyui.com/). [daisy-cotton](https://github.com/django-mvp/daisy-cotton) holds one Cotton component for each daisyUI component. This package holds what is built on top of those, and it comes in two kinds:

- **Extended components**: single components that go further than their daisyUI counterpart, such as a card with more structure than `card` gives you.
- **Page blocks**: whole regions of a public-facing page, such as a hero, ready to drop in.

The blocks came first, and they are what is built so far.

Component libraries in this space cover the application: navigation, forms, tables, dialogs. They stop at the pages that sit in front of it — the landing page, the pricing page, the sign-up pitch. Those get assembled by hand out of raw utility classes, in every project, every time.

Blocks are configured through attributes and take their colours from whatever daisyUI theme the project already runs, so a page built from them re-themes with the rest of the site.

## Contents

- [Status](#status)
- [Scope & philosophy](#scope--philosophy)
- [Requirements](#requirements)
- [Install](#install)
- [Blocks](#blocks)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [License](#license)

## Status

Version 0.0.1. Eleven families are built: the section and its columns, the heading, heroes, backgrounds, text effects, reveals, quotes, stats, points, sign-in pages and sign-up pages. Nothing here is stable. Block names, attributes and the set of classes the stylesheet emits all change between minor versions, and the [CHANGELOG](https://github.com/django-mvp/daisy-cotton-ext/blob/main/CHANGELOG.md) is how a project finds out.

## Scope & philosophy

**What this is.** A presentation-only library of extended components and page blocks. Templates, a stylesheet, and the small amount of JavaScript some blocks need. Blocks are configured through attributes and themed by whatever daisyUI theme the project runs, so a page built from them never pins a literal colour into the markup.

**What this deliberately is not.**

- **Not an application.** No models, no views, no forms, no URLs, no migrations. A block's content comes from the template author, never from a queryset.
- **Not a CSS framework.** No daisyUI plugin, no theme layer, no preflight. Those come from the project.
- **Not the base components.** A component that maps one-to-one onto a daisyUI component belongs in [daisy-cotton](https://github.com/django-mvp/daisy-cotton). What lives here adds to one or combines several.
- **Not application chrome.** Navigation, forms, tables and CRUD pages take their content from the application, and they are somebody else's job.
- **Not a fixed catalogue.** The set of blocks grows as new ones are designed. There is no taxonomy to fill in.
- **Not page templates.** Blocks only. You pick the ones you want and assemble the page yourself. There is no one-tag landing page.

**Tie-breaks.** When two of these pull against each other: theme-driven beats hard-coded, a block that composes existing daisyUI markup beats one that invents its own, and leaving a job to the project beats doing it here.

The directions the package works toward are in [GOALS.md](https://github.com/django-mvp/daisy-cotton-ext/blob/main/GOALS.md), and the order they are being built in is in the [roadmap](https://github.com/django-mvp/daisy-cotton-ext/blob/main/docs/ROADMAP.md).

## Requirements

- Python 3.12+
- Django 5.2, 6.0 or 6.1
- django-cotton 2.6+
- [daisy-cotton](https://github.com/django-mvp/daisy-cotton) 0.1.3+, installed with this package
- daisyUI 5, loaded by the project

daisyUI is a hard requirement and this package does not ship it. Any project already running daisyUI satisfies it, whether through its own Tailwind build or through a package that provides one, such as [django-mvp](https://github.com/django-mvp/django-mvp).

## Install

```bash
pip install daisy-cotton-ext
```

Add it to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...,
    "django_cotton",
    "daisy_cotton",
    "daisy_cotton_ext",
]
```

`daisy_cotton` holds the base components some of these are built from, such as the avatar beside a quotation's name. A project that already has a component of the same name, its own or another package's, keeps it: Django uses the first one it finds in `INSTALLED_APPS` order. django-mvp ships a `<c-section>` of its own, a titled section with a toolbar, so a project that uses both packages gets whichever is listed first.

Then load its stylesheet after the one carrying daisyUI:

```html
<link rel="stylesheet" href="{% static 'css/your-daisyui-build.css' %}">
<link rel="stylesheet" href="{% static 'css/daisy-cotton-ext.css' %}">
```

The two stylesheets do different jobs. Yours carries daisyUI, its themes and Tailwind's preflight. This one carries the plain Tailwind utilities the blocks need and which your build has no way to know about, because it scans your source and these templates live in site-packages.

Every class in this stylesheet is prefixed `dce:`, as in `dce:flex` and `dce:lg:grid-cols-2`, so none of them shares a name with a class in your build and neither stylesheet can override the other's utilities. Link them in the order shown. The other order is tested and works against a Tailwind 4 build, but yours first is the one to rely on.

A class you pass to a block yourself, through its `class` attribute or inside a slot, is yours and comes from your build. This stylesheet emits nothing unprefixed.

Blocks are then available as Cotton tags:

```html
<c-hero.centred title="Ship it on Friday">
  ...
</c-hero.centred>
```

## Blocks

### Section and columns

The outer shell of a region of a page, and the columns inside it. A section always spans the page, and so does its background. `container` decides how wide the content inside may grow.

| Tag | What it is |
|---|---|
| `<c-section>` | The shell: a `section` element with a background layer, a header and a body held to a chosen width |
| `<c-section.col>` | One column of a section |

Nothing says how many columns a section has. Each `<c-section.col>` opens one, and they share the width equally unless `span` says otherwise. Below the `lg` breakpoint they become one column, in the order written.

```html
<c-section container="wide" reverse class="bg-base-200">
  <c-slot name="background"><c-background.grid /></c-slot>
  <c-slot name="header">
    <c-heading eyebrow="Deploy tracking" title="See which change broke the graph" />
  </c-slot>
  <c-section.col span="2">
    <p>Every deploy is drawn on the same timeline as your error rate.</p>
  </c-section.col>
  <c-section.col span="3">
    <img src="{% static 'img/timeline.png' %}" alt="A deploy marked on an error-rate graph">
  </c-section.col>
</c-section>
```

`<c-section>` takes:

| Attribute | Default | What it does |
|---|---|---|
| `height` | `content` | `content` is as tall as what the section holds. `screen` is at least as tall as the window, with the content centred in it |
| `flush` | off | Drops the room above and below the content, for columns that carry surfaces of their own |
| `container` | `default` | How wide the content may grow: `narrow` for a page of text, `default`, `wide`, or `full` to run to the edges of the page with no gutter |
| `gap` | `md` | The room between columns, and between them once stacked: `none`, `sm`, `md` or `lg` |
| `align` | `stretch` | Where columns of different heights sit against each other: `stretch`, `start`, `center` or `end` |
| `reverse` | off | Runs the columns the other way at `lg` and above, for up to six columns. Stacked columns always read in the order written |
| `invert` | off | Light copy, for a dark background |
| `class` | — | Extra classes on the section element. A plain surface colour goes here: `bg-base-200` |

| Slot | What goes in it |
|---|---|
| default | Anything, or one `<c-section.col>` for each column |
| `background` | A background block, rendered into a layer behind the content |
| `header` | Above the columns, across the whole width |

`<c-section.col>` takes:

| Attribute | Default | What it does |
|---|---|---|
| `span` | `1` | How many shares of the width the column takes. A `2` beside a `3` is two fifths beside three fifths |
| `align` | — | Where this column sits against taller neighbours, when it should differ from the section: `start`, `center` or `end` |
| `class` | — | Extra classes on the column. A surface colour and padding go here |

It has a `background` slot of its own, which puts a background block behind that column alone.

A section can sit inside another, or inside a column. The inner one adds no gutters and no room above or below, and keeps the copy colour of the section around it, so an outer section can carry a background across the page while an inner one holds the text to `narrow`.

Columns are for a small, fixed number of parts that stack at one breakpoint. A row of many cards that should go from four across to two to one is a grid, and is not what this is for. The reasoning is in [ADR 0011](docs/adr/0011-a-sections-columns-are-counted-by-the-stylesheet.md).

### Heading

`<c-heading>` is the three lines that open most sections and heroes: a short line above, the heading, and a sentence under it. Any of them can be left out, and with none it renders nothing.

```html
<c-heading eyebrow="Included in every plan" title="What you get on day one" lead="Nothing here is held back for a larger plan." />
```

| Attribute | Default | What it does |
|---|---|---|
| `eyebrow` | — | A short line above the heading |
| `title` | — | The heading. Use a `title` slot instead when it contains markup |
| `lead` | — | The supporting sentence under it |
| `level` | `2` | Heading level. It never changes how large the heading looks |
| `size` | `md` | How large the heading is set: `md` opens a section, `lg` and `xl` open a page |
| `align` | `center` | Which edge the words sit against: `start`, `center` or `end`. `none` sets nothing, so they follow the text alignment around them |
| `invert` | off | Light copy, for a dark background |
| `class` | — | Extra classes on the wrapper |

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

Six more move. Each one holds still for a reader whose system asks for reduced motion.

| Tag | What it does | Attributes |
|---|---|---|
| `<c-background.parallax>` | Wraps any other background and scrolls it more slowly than the page | `speed` |
| `<c-background.aurora>` | Three blurred discs drifting across each other | `from`, `via`, `to`, `intensity`, `speed` |
| `<c-background.flow>` | A three-colour wash sliding from side to side | `from`, `via`, `to`, `opacity`, `speed` |
| `<c-background.horizon>` | A ruled floor rolling towards the reader | `size`, `intensity`, `speed` |
| `<c-background.particles>` | Small dots rising and fading | `variant`, `intensity`, `speed` |
| `<c-background.hyperspace>` | Streaks of light flying out from the centre | `variant`, `density`, `intensity`, `speed` |

An attribute that sets an amount takes a number, and any number works:

| Attribute | What the number means |
|---|---|
| `intensity`, `opacity`, `dim` | From `0` to `1` |
| `size` | A length in rem |
| `speed` | A multiple of the usual pace: `2` is twice as fast, `0.5` half |
| `speed` on parallax | How fast the layer scrolls against the page: `1` moves with it, `0.5` at half its speed |
| `density` | A multiple of the usual forty streaks |

The number is written to the layer's `style` attribute, as a custom property or as `opacity`. A page served under a content security policy that forbids inline styles ignores it and gets the defaults.

The movement is CSS only. Parallax relies on scroll-driven animation, so in a browser without it the wrapped background stays where it is. It also needs every element between itself and the page to clip with `overflow: clip` and never `overflow: hidden`, which the hero blocks do.

Two things to know about them. A background belongs in a `background` slot and nowhere else, because it positions itself against that slot's wrapper rather than filling its parent in normal flow. And a dark background needs `invert` on the block, since a background cannot reach up to recolour its sibling. Each block's page says whether it wants one.

```html
<c-hero.centred title="Ship the page, not the CSS"
                lead="Blocks for the pages in front of your app."
                invert>
  <c-slot name="background">
    <c-background.image src="{% static 'img/desk.jpg' %}" dim="0.85" />
  </c-slot>
  <c-slot name="actions">
    <a class="btn btn-primary btn-lg" href="{% url 'signup' %}">Get started</a>
  </c-slot>
</c-hero.centred>
```

### Text effects

A text effect is an inline span around a few words. It goes anywhere words go and takes its size and weight from whatever it sits in, so the heading stays the page's own.

```html
<h1 class="text-5xl font-bold">
  Ship the page, <c-text.gradient>not the CSS</c-text.gradient>
</h1>
```

Three hold still:

| Tag | What it does | Attributes |
|---|---|---|
| `<c-text.glow>` | Lights the words in a theme colour with a soft halo behind them | `variant`, `intensity`, `spread`, `pulse`, `repeat` |
| `<c-text.outline>` | Draws the letters as a line with nothing inside them | `variant`, `weight` |
| `<c-text.depth>` | Gives the words a solid edge, so they stand off the page | `variant`, `depth` |

Six move. Each one renders the finished words, holding still, for a reader whose system asks for reduced motion.

| Tag | What it does | Attributes |
|---|---|---|
| `<c-text.gradient>` | Three theme colours sliding through the letters | `from`, `via`, `to`, `speed`, `repeat` |
| `<c-text.shimmer>` | A band of colour crossing words that keep their own colour | `variant`, `speed`, `frequency`, `repeat` |
| `<c-text.marker>` | A stroke drawn under the words, once, as the page loads | `variant`, `size`, `speed`, `delay` |
| `<c-text.typewriter>` | A line typed out a letter at a time, once | `text`, `speed`, `delay` |
| `<c-text.wave>` | A ripple running along a line, letter by letter | `text`, `height`, `speed`, `repeat` |
| `<c-text.glitch>` | Slices of the words jumping sideways for a moment, every few seconds | `from`, `to`, `intensity`, `frequency`, `repeat` |

The numbers mean the same thing throughout:

| Attribute | What the number means |
|---|---|
| `speed` | A multiple of the usual pace: `2` is twice as fast, `0.5` half, and `0` leaves the words at rest |
| `frequency` | A multiple of how often it happens: `2` is twice as often, and `0` never |
| `pulse` | How quickly a glow breathes, as a multiple. `0`, the default, holds it steady |
| `repeat` | How many times it runs before it stops. Left out, it never stops |
| `intensity` on glow | From `0` to `1` |
| `intensity` on glitch, `spread`, `depth` | A multiple of the usual amount |
| `size`, `height` | A share of the height of the letters |
| `weight` | A thickness in pixels |
| `delay` | Seconds before it starts |

On a shimmer, `speed` is how fast the band travels across the words and `frequency` is how often it comes round. A crossing never takes longer than the wait between crossings.

Things to know before reaching for one:

- **Typewriter and wave take their line as a `text` attribute**, because a template can split a string into letters and cannot split markup. `text="{{ title }}"` and `:text="title"` both work.
- **Glow and glitch are for a few words on one line.** They lay copies of the words over the original, so the phrase does not wrap, and their content should be plain words.
- **Gradient, outline and depth are for headings.** A palette colour makes no promise of contrast against the page, and large type survives that where a sentence does not.
- **Nothing pauses a looping effect.** A page that has to meet WCAG 2.2.2 sets `repeat` on each one, or supplies its own control.
- **A screen reader is given the words once**, whichever effect is drawing them and however many copies or letters it draws.

The reasoning is in [ADR 0005](docs/adr/0005-text-effects-are-spans-moved-by-css.md).

### Reveals

A reveal wraps content the page already has and brings it in as the reader scrolls to it or points at it. Nothing moves until it is asked to: a page uses a reveal by wrapping something in one.

| Tag | What it does | Attributes |
|---|---|---|
| `<c-reveal.enter>` | Brings in whatever it wraps as it scrolls into view | `effect`, `distance`, `over` |
| `<c-reveal.cascade>` | Brings in its direct children one after another | `effect`, `distance`, `step`, `per`, `over` |
| `<c-reveal.wipe>` | Uncovers a picture from one edge while it settles from a slight zoom | `from`, `zoom`, `over` |
| `<c-reveal.words>` | Lights a paragraph a word at a time as it is scrolled through | `text`, `dim`, `start`, `end` |
| `<c-reveal.stack>` | Stops each panel at the top of the screen and slides the next one over it | `top`, `step` |
| `<c-reveal.hover>` | Keeps a caption out of sight until the picture is pointed at or focused | `effect`, `zoom`, `label` |

`effect` on enter and cascade is one of `up`, `down`, `left`, `right`, `zoom`, `blur` and `fade`. A direction is the way the content travels, so `up` rises into place from below. On hover it is `slide` or `cover`. `from` on wipe is `left`, `right`, `top`, `bottom` or `centre`.

The other attributes are numbers:

| Attribute | What the number means |
|---|---|
| `distance` | How far the content travels, in rem |
| `over` | How much scrolling an arrival takes, as a multiple of the element's own height |
| `step` on cascade | How far each child waits behind the one before, as a share of its height |
| `per` on cascade | How many children sit in a row, so the count starts again on each row. `0` counts straight through |
| `zoom` | A multiple of the picture's size. `1` holds it still |
| `dim` on words | How faint a word is before it is reached, from `0` to `1` |
| `start`, `end` on words | How far up the screen the paragraph has come when the first and the last word light, from `0` at the bottom edge to `1` once it has left the top |
| `top`, `step` on stack | How far below the top of the screen a panel stops, and how much lower each one stops than the last, in rem |

```html
<c-reveal.cascade per="3" class="grid gap-6 md:grid-cols-3">
  <div class="card bg-base-200">…</div>
  <div class="card bg-base-200">…</div>
  <div class="card bg-base-200">…</div>
</c-reveal.cascade>

<c-reveal.hover class="rounded-box" label="Northern ridge, site 14">
  <img src="{% static 'img/ridge.jpg' %}" alt="A ridgeline at dusk" />
  <c-slot name="caption">
    <strong>Northern ridge, site 14</strong>
    <a class="link" href="{% url 'site' 14 %}">Open the record</a>
  </c-slot>
</c-reveal.hover>
```

Things to know before using one:

- **The scroll reveals follow the scroll position.** There is no script and no timer, so the movement runs backwards when the page is scrolled back up, and it does not replay.
- **Without scroll-driven animation the content is simply there.** The same goes for a reader whose system asks for reduced motion. Stack is the exception in the other direction: it is ordinary sticky positioning and works everywhere.
- **Clip with `overflow: clip`, never `overflow: hidden`,** on anything between a reveal and the page. `overflow: hidden` makes a scroll container, and inside one a scroll reveal never moves and a stacked panel never sticks. `left` and `right` start outside the wrapper's box, so their parent usually wants `overflow-clip`.
- **`over` above `1` can leave the last thing on a page part-way in,** because the page runs out of scroll before the arrival finishes.
- **Cascade staggers its first twelve children.** Any after that arrive with the first.
- **Words takes its text as an attribute, not a slot,** and splits it on spaces, so it carries plain words and no markup. A word is fainter than body text should be until it is reached, which suits one short, large statement and not body copy.
- **Hover is reachable without a mouse.** The frame takes keyboard focus and the caption stays open while anything inside it has focus. Where the device has no hover, the caption shows all the time.
- **Give each stacked panel a solid surface,** or the one underneath shows through.

The reasoning is in [ADR 0006](docs/adr/0006-reveals-follow-the-scroll-position.md).

### Quotes

A quote is what somebody said and who said it. Four are components that sit inside a page's own layout, three are blocks that take the full width, and one is the caption the others share.

| Tag | What it does | Attributes |
|---|---|---|
| `<c-quote.pull>` | Sets a quotation off from an article with a rule down its leading edge | `variant`, `size` |
| `<c-quote.mark>` | Puts one oversized quotation mark above the words | `variant`, `align`, `size` |
| `<c-quote.card>` | A card with the person at the foot and an optional row of stars | `rating`, `variant` |
| `<c-quote.bubble>` | A speech bubble with its tail pointing at the person | `variant`, `align` |
| `<c-quote.centred>` | One quotation, large and centred, across the page | `invert`, `size` |
| `<c-quote.split>` | A picture of the person beside what they said | `src`, `alt`, `reverse`, `invert`, `size` |
| `<c-quote.wall>` | Many quotations packed into columns | `eyebrow`, `title`, `lead`, `level`, `columns`, `size` |
| `<c-quote.byline>` | The portrait, name and role under a quotation | `align`, `size`, `invert` |

Every quote but the wall also takes the person: `name`, `role`, `source`, `href` and `src`. `source` is the work the words come from, and `href` is where it can be read. `src` is a small portrait, except on split, where it is the picture beside the words.

`variant` is a colour of the theme: `primary`, `secondary`, `accent` or `neutral`. It colours the rule on pull, the mark on mark, the filled stars on card and the whole bubble on bubble, which also takes `base-100`, `base-200` and `base-300`.

```html
<c-quote.pull name="Amara Okafor" role="Head of Platform, Northwind" src="{% static 'img/amara.jpg' %}">
  “Friday afternoon stopped being frightening.”
</c-quote.pull>

<c-quote.wall title="What people say" columns="3">
  <c-quote.card rating="5" name="Mei Tanaka" role="Compliance Lead, Harbour Bank">
    “The audit log answered the question before the auditor had finished asking it.”
  </c-quote.card>
  <c-quote.card rating="4" variant="primary" name="Jonas Lindqvist" source="Fjordline engineering blog" href="https://example.com/blog">
    “Rolling back used to be a meeting. Now it is a button.”
  </c-quote.card>
</c-quote.wall>
```

Things to know before using one:

- **Every quote is a `figure` holding a `blockquote`,** with a `figcaption` when there is anybody to name. A quote given no `name`, `role` or `source` has no caption at all.
- **Write the quotation marks yourself,** except in mark, where the oversized one does that job.
- **`source` is marked up as a citation and the person is not.** `cite` names a work. Given an `href`, the source becomes a link and the address is recorded on the `blockquote`.
- **The portrait is daisy-cotton's `<c-avatar>`,** at its stock size, with an empty `alt` because the name sits beside it. The picture on split is different: give it an `alt` when it shows more than the name says.
- **`rating` is a whole number from 1 to 5.** The stars are read out as one thing, “4 out of 5”. Anything else, and there is no row of stars.
- **A wall reads down each column, not across.** That is what lets long and short quotations sit together without gaps. Put them in a grid when the order across matters.
- **Centred and split take a `background` slot,** like the heroes, and `invert` for a dark one.

The reasoning for building on daisy-cotton's components is in [ADR 0007](docs/adr/0007-built-from-daisy-cotton-components.md).

### Stats

A stat is a figure and what it counts. daisy-cotton's `<c-stat>` shows a title, a number and a line of description. These add what usually comes next: how the number has moved, how far it is towards a target, an icon beside it, a count up as the visitor reaches it. Eight are stats that go wherever a stat goes, one is the badge they share, and three are blocks that set figures out across a page.

| Component | What it is | Options of its own |
|---|---|---|
| `<c-stats.trend>` | A figure with how it has moved underneath it | `change`, `direction`, `inverse` |
| `<c-stats.trend-inline>` | The same, with the change beside the figure | `change`, `direction`, `inverse` |
| `<c-stats.trend-corner>` | The same, with the change in the top corner | `change`, `direction`, `inverse` |
| `<c-stats.trend-centred>` | The same, on the centre line, figure first | `change`, `direction`, `inverse` |
| `<c-stats.trend-footer>` | The same, with the change ruled off along the bottom | `change`, `direction`, `inverse` |
| `<c-stats.trend-row>` | The same, laid on its side for a stacked list | `change`, `direction`, `inverse` |
| `<c-stats.progress>` | A figure with a bar towards a target or a limit | `percent`, `variant` |
| `<c-stats.count>` | A figure that counts up as it scrolls into view | `to`, `prefix`, `suffix`, `time` |
| `<c-stats.change>` | The arrow badge the trend stats carry, by itself | `change`, `direction`, `inverse` |
| `<c-stats.band>` | Figures in one row across the page, under an optional heading | `eyebrow`, `title`, `lead`, `level`, `cascade`, `invert`, `size` |
| `<c-stats.split>` | The case in words on one side, the figures on panels on the other | `eyebrow`, `title`, `lead`, `level`, `size` |
| `<c-stats.headline>` | One very large figure, filled with a gradient | `value`, `title`, `lead`, `level`, `icon`, `speed`, `size` |

Every single-figure stat also takes `title`, `value` and `desc`, the names `<c-stat>` uses, and an optional `icon`.

```html
<c-stat.group>
  <c-stats.trend icon="deploys" title="Deploys a day" value="31" change="12%" desc="since last month" />
  <c-stats.trend title="Median lead time" value="18m" change="26m" direction="down" inverse desc="since the spring" />
  <c-stats.progress title="Raised this quarter" value="€42k" percent="70" desc="of a €60k target" />
</c-stat.group>

<c-stats.band title="A year in numbers" cascade>
  <c-stats.count title="Releases" to="7440" />
  <c-stats.count title="Teams" to="41" />
  <c-stats.count title="Saved a year" to="48" prefix="€" suffix="k" />
</c-stats.band>
```

Things to know before using one:

- **Each single-figure stat is daisy-cotton's `<c-stat>` with something added,** so it goes in a `<c-stat.group>` beside plain stats.
- **The six trend stats take the same attributes.** Changing layout is changing the tag.
- **`direction` says which way the figure moved and `inverse` says a fall is the good news,** as it is for a lead time or a failure count. The arrow and a direction read out to a screen reader carry the move. The colour only repeats it.
- **`icon` is a name handed to your project's own `<c-icon>`,** so it draws whichever icon set you already use. Leave it out and there is no icon. Fill the `figure` slot for a picture or a logo. Corner and row take a small icon only.
- **No stat draws a chart.** Trend, inline, corner and footer place whatever you put between their tags under the figures, which is where a chart from a charting package goes.
- **You format the figures and work out the percentage.** `value` arrives as words. `percent` is a number from 0 to 100.
- **`<c-stats.count>` counts whole numbers, written without separators.** For a large figure, count the leading part and put the rest in `suffix`: `to="12" suffix="k"`. A screen reader is given the finished number. Under `prefers-reduced-motion`, and in a browser without scroll-driven animation, so is everyone else.
- **Inside a `<c-stat.group>`, a count runs once as the page loads.** A stat group is a scrolling box of its own, and "in view" is measured against the nearest one. Put counting stats in `<c-stats.band>` or a plain grid for a count that waits.
- **Nothing else here moves unless asked.** `cascade` on a band and `speed` on a headline are both off by default.
- **The band takes a `background` slot,** like the heroes, and `invert` for a dark one.

The reasoning is in [ADR 0008](docs/adr/0008-stats-draw-no-charts.md) and [ADR 0009](docs/adr/0009-a-count-is-started-by-scroll-and-timed-by-the-clock.md).

Every attribute, its accepted values and its default are listed on each block's and component's own page in the example project, built from the annotations in the block's template. Run it with `python manage.py runserver` from a checkout.

### Sign in and sign up

Whole-page blocks for the two pages in front of an application. Each one is the layout and nothing behind it: the logo, the form and the buttons that skip the form are the application's, and arrive as slots. Five are for signing in, four for signing up, and one is the panel most of them draw their form in.

| Tag | What it does | Attributes of its own |
|---|---|---|
| `<c-sign-in.centred>` | A card in the middle of the screen with the logo above it | |
| `<c-sign-in.split>` | The form in one half of the screen and a brand pane in the other | `reverse`, `surface` |
| `<c-sign-in.floating>` | One background across the screen, a line of copy on it, and the form in a translucent card | `headline`, `invert` |
| `<c-sign-in.stepped>` | One question to a screen, in large type, under a bar holding the logo | `eyebrow` |
| `<c-sign-in.providers>` | A wide card in two panes, with the one-press ways in up front and the form behind a disclosure | `disclosure`, `open`, `surface` |
| `<c-sign-up.pitch>` | The case for signing up beside the form that does it | `eyebrow`, `headline` |
| `<c-sign-up.showcase>` | The form beside a picture of the product, running off the edge of the screen | `caption`, `surface` |
| `<c-sign-up.bento>` | The form as the tall middle tile of a grid of reasons | |
| `<c-sign-up.stepped>` | A run of steps across the top and one card for the current step | |
| `<c-auth.panel>` | A heading, the buttons that skip the form, a word between, the form and a foot | `size`, `align`, `card`, `surface` |

Every one takes `title`, `lead`, `level`, `divider` and `class`, and these slots:

| Slot | What goes in it |
|---|---|
| `logo` | The application's logo: an image or inline SVG, usually inside a link home |
| default | The application's form, with its fields, its errors and its submit button |
| `providers` | One full-width button for each way in that skips the form |
| `footer` | The link across to the other page, or the terms |
| `background` | A background component, drawn behind the page or behind its pane |

Several add slots of their own: `aside` for a brand pane, `nav` for the far end of a top bar, `points` on pitch, `media` on showcase, `tiles` on bento and `steps` on the stepped sign-up.

With [django-allauth](https://docs.allauth.org/), a sign-in template comes out like this:

```html
{% load static socialaccount %}
<c-sign-in.split title="Welcome back" lead="Sign in to pick up where you left off.">
  <c-slot name="logo">
    <a href="/"><img src="{% static 'brand/logo.svg' %}" alt="Acme" class="h-8"></a>
  </c-slot>
  <c-slot name="providers">
    <c-button href="{% provider_login_url 'google' %}" outline class="btn-block" text="Continue with Google" />
  </c-slot>

  <form method="post" action="{% url 'account_login' %}">
    {% csrf_token %}
    {{ form.as_div }}
    <c-button type="submit" variant="primary" class="btn-block" text="Sign in" />
  </form>

  <c-slot name="footer">New here? <a class="link" href="{% url 'account_signup' %}">Create an account</a></c-slot>
  <c-slot name="background"><c-background.grid /></c-slot>
  <c-slot name="aside">
    <c-quote.byline invert name="Amara Okafor" role="Head of Platform, Northwind" />
  </c-slot>
</c-sign-in.split>
```

Things to know before using one:

- **Each block fills the screen.** It is the page, so put it straight inside `body` with no application shell around it.
- **The logo is always a slot, and it is there at every width.** On the layouts with a brand pane, the pane is dropped below the `lg` breakpoint and the logo stays with the form.
- **No block renders a field.** Use your own form rendering or daisy-cotton's form components. The demo's forms are stand-ins.
- **The divider is drawn only between two things.** With no `providers`, or with no form, there is no word between them. `divider` is the word. Left out, it is “or”, translated with the rest of the package's own words.
- **A block has no words of its own beyond that divider and the line that opens the disclosure.** A block given no `title` has no heading.
- **The page keeps one heading.** `title` is an `h1` unless `level` says otherwise. On pitch the `headline` takes that level and the form's `title` sits one below it. The large line on floating and the caption on showcase are paragraphs.
- **Give `<c-sign-in.providers>` `open` when the form comes back with errors,** or the errors are folded away with it.
- **What is in a brand pane is decoration.** It is not shown on a narrow screen, so nothing a visitor needs belongs there. The picture on showcase is also hidden from a screen reader.
- **`surface` is a pair of classes,** a background and the text colour that goes with it: `surface="bg-primary text-primary-content"`.
- **`<c-sign-up.stepped>` takes the whole run of steps in its `steps` slot.** daisy-cotton's `<c-steps>` is the obvious thing to put there.
- **`<c-auth.panel>` is for a page none of these covers:** a password reset, a code to confirm. It draws the same structure, with a card around it when given `card`.

Why the blocks stop at the frame is in [ADR 0010](docs/adr/0010-sign-in-pages-own-the-frame-and-not-the-form.md).

### Points

A short list of reasons, each a mark, a few words in bold and a sentence. `<c-points>` is the list and `<c-points.point>` is one reason in it.

```html
<c-points>
  <c-points.point title="Ten minutes to set up.">
    Connect a repository and your next deploy shows up on its own.
  </c-points.point>
  <c-points.point title="Works where you already deploy from.">
    <c-slot name="mark"><c-icon name="github" /></c-slot>
    GitHub, GitLab and Bitbucket.
  </c-points.point>
</c-points>
```

The mark is a tick in the theme's primary colour unless the `mark` slot holds something else. Either way it is hidden from a screen reader, so the words have to carry the point alone.

## Contributing

Development setup, building the stylesheet and the rules changes are held to are in [CONTRIBUTING.md](https://github.com/django-mvp/daisy-cotton-ext/blob/main/CONTRIBUTING.md).

## Changelog

Every release is recorded in [CHANGELOG.md](https://github.com/django-mvp/daisy-cotton-ext/blob/main/CHANGELOG.md).

## License

[MIT](https://github.com/django-mvp/daisy-cotton-ext/blob/main/LICENSE)
