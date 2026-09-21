# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

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
