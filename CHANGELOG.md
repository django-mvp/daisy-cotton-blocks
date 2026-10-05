# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
