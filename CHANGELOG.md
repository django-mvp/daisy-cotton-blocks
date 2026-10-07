# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `<c-section>` and `<c-section.col>`. A section is the outer shell of a region of a page: it
  spans the page, takes a `background` slot and a `header` slot, and holds its content to the
  width `container` names. Each `<c-section.col>` inside it becomes a column, sharing the width by
  `span`, and they stack in the order written below the `lg` breakpoint. `reverse` runs them the
  other way at `lg` and above. A column takes a `background` slot of its own, and a section can
  sit inside another.
- `<c-heading>`, the short line, heading and supporting sentence that open a section or a hero,
  with `level`, `size` and `align`.
- Nine text effects, each an inline span around a few words: `<c-text.glow>`, `<c-text.outline>`
  and `<c-text.depth>`, which hold still, and `<c-text.gradient>`, `<c-text.shimmer>`,
  `<c-text.marker>`, `<c-text.typewriter>`, `<c-text.wave>` and `<c-text.glitch>`, which move. The
  movement is CSS only, each one renders the finished words under `prefers-reduced-motion`, and a
  looping effect takes `repeat` to stop it after a set number of runs.
- The reveal family. Five follow the scroll position:
  `<c-reveal.enter>` brings in whatever it wraps, `<c-reveal.cascade>` brings in its children one
  after another, `<c-reveal.wipe>` uncovers a picture from one edge, `<c-reveal.words>` lights a
  paragraph a word at a time and `<c-reveal.stack>` slides each panel over the one before.
  `<c-reveal.hover>` keeps a caption out of sight until its picture is pointed at or focused. The
  movement is CSS only. Under `prefers-reduced-motion`, and in a browser without scroll-driven
  animation, the content is simply there.
- The quote family. `<c-quote.pull>`, `<c-quote.mark>`, `<c-quote.card>` and `<c-quote.bubble>` sit
  inside a page's own layout. `<c-quote.centred>`, `<c-quote.split>` and `<c-quote.wall>` are blocks
  that take the full width. `<c-quote.byline>` is the caption they share: a portrait, a name, and a
  role or a cited source. Each quote is a `figure` holding a `blockquote`.
- The stats family, built on daisy-cotton's `<c-stat>`. `<c-stats.trend>` shows how a figure has
  moved and comes in five more layouts that take the same attributes: `<c-stats.trend-inline>`,
  `<c-stats.trend-corner>`, `<c-stats.trend-centred>`, `<c-stats.trend-footer>` and
  `<c-stats.trend-row>`. `<c-stats.progress>` adds a bar towards a target, `<c-stats.count>` counts
  up as it scrolls into view, and `<c-stats.change>` is the arrow badge by itself.
  `<c-stats.band>`, `<c-stats.split>` and `<c-stats.headline>` are blocks that set figures out
  across a page. Every stat takes an optional `icon`. None draws a chart.
- Five sign-in pages and four sign-up pages, as blocks that fill the screen: `<c-sign-in.centred>`,
  `<c-sign-in.split>`, `<c-sign-in.floating>`, `<c-sign-in.stepped>` and `<c-sign-in.providers>`,
  and `<c-sign-up.pitch>`, `<c-sign-up.showcase>`, `<c-sign-up.bento>` and `<c-sign-up.stepped>`.
  Each is the layout only. The logo, the form and the buttons that skip the form arrive as slots,
  under the same names in all nine, so a django-allauth template fills them directly.
- `<c-auth.panel>`, the heading, provider buttons, divider, form and foot that seven of those pages
  draw their form in, with an optional card around it. For a page of the same kind that none of
  them covers.
- `<c-points>` and `<c-points.point>`, a short list of reasons with a tick or a mark of your own
  beside each.
- A translation catalogue, `locale/en`, for the few words the package supplies itself: the
  direction a trend stat reads out to a screen reader, a quote card's rating, and the word a
  sign-in page puts between its provider buttons and its form.

### Changed

- Every hero, quote and stats page block is built from `<c-section>`, and takes its eyebrow, title
  and lead from `<c-heading>` where it has them. `<c-stats.headline>` keeps its own heading, which
  joins the figure and its title. Attributes and slots are unchanged. The markup inside the
  section element is not: the content sits in a `div` carrying `data-section-body`, the columns of
  `<c-hero.split>`, `<c-quote.split>` and `<c-stats.split>` are `div` elements carrying
  `data-section-col`, and a reversed block no longer uses the `lg:order-1` and `lg:order-2`
  classes. Two things render differently. A hero given an empty `title` leaves the heading
  element out. `<c-stats.headline>` lets a figure run up to 64px wider before it wraps.

- The daisyUI classes a host is expected to provide now include `badge-soft`, `badge-sm`, the
  success, error and neutral badge colours, `progress` and its colours, `stat-figure` and
  `stat-actions`. All are in daisyUI 5.

- **Breaking.** The attribute that picks a theme colour is `variant`, the name daisy-cotton gives
  it, in place of `color`. It changes on `<c-hero.highlight>`, `<c-background.particles>` and
  `<c-background.hyperspace>`: `color="accent"` becomes `variant="accent"`. `color` is no longer
  recognised and renders the default. The text effects that take a theme colour, `<c-text.glow>`,
  `<c-text.outline>`, `<c-text.depth>`, `<c-text.shimmer>` and `<c-text.marker>`, use `variant` as
  well.
- daisy-cotton is now a dependency, and `daisy_cotton` goes in `INSTALLED_APPS`. The quote family
  shows a portrait with its `<c-avatar>`.
- **Breaking.** Every class the stylesheet emits is prefixed `dce:`, and the blocks' markup uses
  the prefixed names: `dce:flex`, `dce:lg:grid-cols-2`. The stylesheet emits no unprefixed
  utility. A project that relied on it for a utility in its own templates, `py-20` or
  `bg-base-200` for instance, needs that class from its own build, or can write `dce:py-20`. CSS
  written against a block's old class names needs the new ones.
- A utility from the project's own build always beats one of the stylesheet's, whichever file is
  linked first, so a class passed to a block overrides the block's default.
- Type sizes, radii and container widths inside a block come from Tailwind's defaults and no
  longer follow a project that has redefined `--text-5xl` and the like. Colours and `--spacing`
  still follow the project. Setting the `--dce-` form of a property, `--dce-text-5xl`, overrides
  it for the blocks.

### Fixed

- The stylesheet no longer overrides a project's own responsive utilities. Linked after the
  project's stylesheet, as the README says to, its `.hidden` beat the project's `.md\:flex`, so
  an element written `hidden md:flex` in the project's templates stayed hidden at every width.
  `hidden lg:block`, `hidden sm:grid` and `sm:hidden` failed the same way.

## [v0.2.0] - 2026-10-05

### Added

- Six backgrounds that move: `<c-background.parallax>`, which wraps any other background and
  scrolls it more slowly than the page, and `<c-background.aurora>`, `<c-background.flow>`,
  `<c-background.horizon>`, `<c-background.particles>` and `<c-background.hyperspace>`. The
  movement is CSS only, and each one holds still under `prefers-reduced-motion`.

### Changed

- **Breaking.** Background attributes that set an amount take a number in place of a name:
  `intensity` on glow and grid, `opacity` on gradient and `dim` on image run from `0` to `1`, and
  `size` on grid is a length in rem. `intensity="bold"` becomes `intensity="0.3"`,
  `opacity="full"` becomes `opacity="1"`, `dim="strong"` becomes `dim="0.85"` and `size="lg"`
  becomes `size="5"`. A name is no longer recognised and renders the default.
- A background writes those numbers to its `style` attribute, as a custom property or as
  `opacity`. Under a content security policy that forbids inline styles they are ignored and the
  defaults apply.
- The hero blocks clip with `overflow: clip` in place of `overflow: hidden`, so a parallax
  background inside one can measure the block against the page.

## [v0.1.0] - 2026-10-05

### Added

- The hero family: `<c-hero.centred>`, `<c-hero.split>` and `<c-hero.showcase>`, which share one
  attribute and slot vocabulary, plus `<c-hero.highlight>` for marking words inside a heading.
- The background family: `<c-background.glow>`, `<c-background.gradient>`, `<c-background.grid>`
  and `<c-background.image>`. Each one goes in another block's `background` slot, so any background
  composes with any layout.
- Every block carries `@description`, `@prop` and `@slot` annotations. The example project builds
  each block's reference page from them, and `python manage.py cotton_lint` checks them.
- The stylesheet emits the palette, gradient, opacity and object-position utilities the background
  blocks compose while they render, which a scan of the templates cannot see.

### Changed

- The project is built and developed with uv instead of Poetry: `uv sync` installs the development
  environment and `uv.lock` replaces `poetry.lock`. The published package is unchanged.
- Django 6.1 is supported, and tested on every change alongside 5.2 and 6.0.
- Renamed from `django-mvp-bits` to `daisy-cotton-ext`. The import package is now
  `daisy_cotton_ext` and the stylesheet ships as `css/daisy-cotton-ext.css`.
- The package's scope covers extended components as well as page blocks: single components that
  go further than their daisyUI counterpart sit alongside the blocks.
- The package no longer requires django-mvp. It works on any Django project running Cotton and
  daisyUI, and `django-cotton` is now a declared dependency.
- The stylesheet carries the plain Tailwind utilities the blocks use, rather than only those a
  django-mvp build omits. Some rules will now appear both here and in a host's own build.
- Blocks are addressed without a namespace prefix, so a tag reads `<c-hero.centred>`. A project
  defining a component at the same path shadows this one, or is shadowed by it, depending on
  `INSTALLED_APPS` order.

## [0.0.1]

Initial scaffold. Build pipeline, stylesheet contract and test harness; no
components yet.
