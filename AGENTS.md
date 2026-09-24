# AGENTS.md — Agent Configuration for daisy-cotton-blocks

<!-- Thin index only — bloat here = ignored instructions. Details live in the pointed-to files. -->

daisy-cotton-blocks ships page blocks: configurable regions of a public-facing page, each rendered
by one Cotton component and styled by daisyUI classes the host project provides, plus the plain
Tailwind utilities this package ships itself. `CONTEXT.md` defines these terms, including why
*variant* is not one of them. Use them.

Presentation only. No models, no views, no forms, no URLs, no migrations. Anything needing one of
those belongs to the project, not here.

## Stack & commands

- **Stack:** Python 3.12+ / Django 5.2, 6.0 and 6.1, uv-managed, built on Cotton and daisyUI
- **Install:** `uv sync` **and** `npm install` (the stylesheet build)
- **Test:** `uv run pytest`
- **Lint:** `uv run pre-commit run --all-files` (ruff lint + format, mypy, deptry)
- **Type-check:** `uv run mypy`
- **Build (Python):** `uv build`
- **Build (stylesheet):** `npm run build:css`, or `npm run watch:css` while working
- **Example project:** `uv run python manage.py runserver 0.0.0.0:8018`

Lint is the pre-commit run, not a bare `ruff check .`: the hook config excludes `docs/` and
migrations, and a raw invocation reports findings in paths the gate does not cover.

## The stylesheet contract

The division of labour that is easy to break by accident, and the reason the stylesheet tests
exist.

`daisy_cotton_blocks/static/css/daisy-cotton-blocks.css` is **committed**, so installing the
package needs no Node toolchain. It is built from `assets/daisy-cotton-blocks.css`, which is
Tailwind only — no daisyUI plugin, no theme layer, no preflight — and which scans this package's
templates plus an inline list for classes scanning cannot see.

The host provides daisyUI, its themes and preflight. This package provides the plain utilities its
own templates use, because a host's Tailwind build scans the host's source and never reaches
site-packages.

Three consequences worth knowing before editing `assets/daisy-cotton-blocks.css`:

1. **Overlap with the host is fine.** A project on django-mvp loads two stylesheets that both
   define `py-20`. Do not try to trim it. The case that matters is a host on a different Tailwind
   version, where one class name carries two different declarations and link order decides.
2. **daisyUI classes are the host's.** The ones blocks may rely on are listed in
   `HOST_PROVIDED_CLASSES` in `tests/test_stylesheet.py`. Using one that is not listed fails the
   suite, and adding one raises the daisyUI floor for every project — a minor-version change, per
   constitution Article XV.
3. **A named class can still emit nothing.** Listing a class is not proof it builds. `from-primary`
   needs daisyUI's palette declared in the `@theme reference` block, or it silently produces no
   rule and the page renders unstyled markup.

After any change to what the stylesheet emits: `npm run build:css`, then `uv run pytest`, then
commit the rebuilt CSS alongside the entry.

## Every block documents itself

A new block is not finished until its own template carries the annotation comments that describe
it. Constitution Article XVII is the contract and `tests/test_annotations.py` is the gate. A block
that skips them fails the suite.

The short version: a single-line `{# @description ... #}`, one `{# @prop ... #}` per attribute in
`<c-vars>`, and one `{# @slot:name — ... #}` per named slot the template renders. Copy the shape
from `cotton/hero/centred.html`, which carries every form of all three. Three traps, each of which
has cost time already:

1. **Each annotation is one line.** Django's `{#...#}` pattern does not cross a newline, so a
   comment closed on the next line is not a comment and is served to the reader as page text.
2. **Slot names stay out of `<c-vars>`.** Cotton fills a named slot whether or not it is declared,
   and a declared one reads to the linter as an undocumented prop.
3. **Never write the block's own tag in angle brackets inside its comments.** The parser takes the
   first occurrence in the source as the declaration and then reports every real prop as missing.

Reasoning goes below the annotations in a `{% comment %}` block, never into the one-liners.
`uv run python manage.py cotton_lint` reports the same findings as the test, with a browsable
gallery to look at them in.

## Agent skills

### Issue tracker

Issues tracked in GitHub Issues via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default label vocabulary mapped 1:1 to canonical roles (needs-triage, needs-info, ready-for-agent,
ready-for-human, wontfix). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout — one `CONTEXT.md` at root and `docs/adr/` for architectural decisions.
See `docs/agents/domain.md`.

### CI checks

CI runs from the shared reusable workflows in `django-mvp/shared`, pinned at `v0.4.1`. Because
they are called rather than inlined, those status checks carry their caller job as a prefix.
The required checks are:

- `call-build / Code Quality`
- `call-build / Security Scan`
- `call-build / Build Package`
- `call-tests / Test Python 3.12, Django 5.2`
- `call-tests / Test Python 3.12, Django 6.0`
- `call-tests / Test Python 3.13, Django 5.2`
- `call-tests / Test Python 3.13, Django 6.0`
- `Built stylesheet matches its source`

The last one is repo-local, from `stylesheet.yml`, and carries **no prefix** — anything matching
check names against the `call-*` pattern will miss it. It rebuilds the stylesheet with the Tailwind
CLI and fails if the committed file differs. What the stylesheet contains, rather than whether it
is current, is covered by pytest instead, so it runs locally and on every matrix cell.

`tests.yml`, `build.yml` and `stylesheet.yml` deliberately carry no `paths:` filter on
`pull_request`. A required check that is filtered out never reports, and a check that never
reports blocks the merge.

## Releasing

Releases run through the shared release flow, never by hand and never by pushing a tag.

1. Dispatch **Prepare Release** with a bump level. It opens a PR carrying the version bump and
   the CHANGELOG section.
2. Merging that PR is the release decision. **Tag Release** then cuts the tag and the GitHub
   Release from the merge commit.
3. **Publish** uploads to PyPI through trusted publishing. PyPI's trusted publisher is bound to
   the `publish.yml` filename — renaming that file breaks publishing until the PyPI project
   settings are changed to match.

`pyproject.toml` holds the version and is the single source of truth for all three steps.

Nothing has been released yet. The first release needs two things confirmed first: a PyPI trusted
publisher pointed at `publish.yml`, and a `RELEASE_TOKEN` that can actually write to this
repository. The initial scaffold's Tag Release run failed with `403 Resource not accessible by
personal access token` on the releases endpoint.

## Development workflow

Feature work follows a spec-driven process: spec → plan → tasks → implement → review → PR, with
`specs/NNN-slug/` directories generated per feature. Project standards and the quality bar live in
`CONSTITUTION.md`.

`docs/brainstorm.md` holds the working notes the package was founded on, chiefly the prior-art
survey. Those are conclusions, not ratified decisions. Anything that has hardened is in
`CONSTITUTION.md` or an ADR, and `docs/adr/0002` is the one to read before touching the stylesheet.
