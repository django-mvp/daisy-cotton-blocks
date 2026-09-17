# AGENTS.md — Agent Configuration for django-mvp-bits

<!-- Thin index only — bloat here = ignored instructions. Details live in the pointed-to files. -->

django-mvp-bits ships page blocks: configurable regions of a public-facing page, each rendered by
one Cotton component under the `mvp-bits` namespace and styled by classes django-mvp's stylesheet
already provides, plus a supplement that adds what it does not. `CONTEXT.md` defines these terms;
use them.

Presentation only. No models, no views, no forms, no URLs, no migrations. Anything needing one of
those belongs upstream in django-mvp.

## Stack & commands

- **Stack:** Python 3.12+ / Django 5.2 and 6.0, Poetry-managed, built on django-mvp and Cotton
- **Install:** `poetry install` **and** `npm install` (the stylesheet build)
- **Test:** `poetry run pytest`
- **Lint:** `poetry run pre-commit run --all-files` (ruff lint + format, mypy, deptry)
- **Type-check:** `poetry run mypy`
- **Build (Python):** `poetry build`
- **Build (stylesheet):** `npm run build:css`, or `npm run watch:css` while working
- **Example project:** `poetry run python manage.py runserver 0.0.0.0:8018`

Lint is the pre-commit run, not a bare `ruff check .`: the hook config excludes `docs/` and
migrations, and a raw invocation reports findings in paths the gate does not cover.

## The stylesheet contract

The one rule that is easy to break by accident, and the reason two of the tests exist.

`mvp_bits/static/css/mvp-bits.css` is **committed**, so installing the package needs no Node
toolchain. It is built from `assets/mvp-bits.css`, which is Tailwind only — no daisyUI plugin, no
theme layer, no preflight — and which whitelists every class by hand rather than scanning
templates. Scanning would re-emit whatever the templates share with django-mvp, which is the
duplication the design exists to prevent.

Three consequences worth knowing before editing `assets/mvp-bits.css`:

1. **The whitelist has gaps that look like typos.** The spacing scale skips 16. `space-y` skips 4.
   There is `transition-all` but no `transition-colors`. django-mvp already emits each of those.
   Do not close a gap without running the tests.
2. **The boundary is arbitrary and moves.** Those classes are not in django-mvp's own safelist —
   they leak into its build because it scans daisyUI's component sources, so a daisyUI upgrade
   shifts the line in both directions.
3. **A whitelisted class can still emit nothing.** Adding a class to the whitelist is not proof it
   builds. `from-primary` needs daisyUI's palette declared in the `@theme reference` block, or it
   silently produces no rule and the page renders unstyled markup.

After any change to the whitelist: `npm run build:css`, then `poetry run pytest`, then commit the
rebuilt CSS alongside the entry.

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
CLI and fails if the committed file differs. Its other half, that the supplement shares no selector
with django-mvp's, is a pytest case instead, so it also runs locally and on every matrix cell.

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

`docs/brainstorm.md` holds the working notes the package was founded on — the prior-art survey and
why the stylesheet is built the way it is. Those are conclusions, not ratified decisions; anything
that hardens goes to `CONSTITUTION.md` or an ADR.
