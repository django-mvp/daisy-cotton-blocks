# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
- Renamed from `django-mvp-bits` to `daisy-cotton-blocks`. The import package is now
  `daisy_cotton_blocks` and the stylesheet ships as `css/daisy-cotton-blocks.css`.
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
