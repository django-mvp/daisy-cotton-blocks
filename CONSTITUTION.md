# daisy-cotton-blocks Constitution

The standards every change to this repository is held to. Read at planning and at review.
Changes here are rare and deliberate, never made in the middle of a feature.

## Core articles

### Article I — Test-First

Every behaviour change follows the traffic-light cycle: **Red** — write a test and watch it fail;
**Green** — write the least code that makes it pass; **Refactor** — clean up with the tests staying
green. No implementation before a failing test exists for the behaviour. Pre-existing tests are
never modified or deleted without a recorded, approved decision.

### Article II — Simplicity

Start with the simplest design that satisfies the spec. New dependencies, new abstractions and new
infrastructure each require a stated justification. YAGNI over speculation.

### Article III — Anti-Abstraction

No wrapper layers, base classes or future-proofing indirection without a present, concrete second
use. Prefer duplication over the wrong abstraction. A block that is nearly another block is still
its own template until a third one proves the shared shape.

### Article IV — Integration-First

Contracts and integration points are designed and tested before internals are polished. A block's
attribute surface is settled against a page that actually uses it, not in the abstract.

### Article V — Security & data-safety

Values interpolated into rendered output are escaped through Django's template layer, never by
hand-built string interpolation. A component attribute is untrusted input: an attribute that ends
up inside an `href`, a `src`, a `style` or an inline event handler is escaped for that context or
rejected, and `|safe` never appears without a stated reason. Secrets live in runtime config, never
in code, fixtures or version control.

### Article VI — Documentation

Public API changes ship their documentation in the same pull request: README and CHANGELOG updated,
docstrings on public surfaces. Public surface here means a component, one of its attributes or
slots, a template tag or filter, and what the shipped stylesheet covers. Adding, renaming, removing
or changing the default of any of those leaves the work unfinished until the documentation says so.

### Article VII — Dependency discipline

A new runtime dependency requires a stated justification, and `deptry` must pass: no unused,
missing or transitively-relied-upon dependencies. Python development tooling comes from the shared
`mvp-shared` bundle rather than per-repository pins. The Node dependencies are build tooling and
stay that way. Nothing under `node_modules` is ever a runtime requirement of the installed package,
which is the whole point of committing the built stylesheet.

### Article VIII — Internationalization

User-facing strings are translatable. In Python they are wrapped with `gettext_lazy`; templates
load `{% load i18n %}` and wrap strings with `{% trans %}` or `{% blocktrans %}`. A hard-coded
user-visible string in a pull request is a blocking comment.

Most blocks satisfy this by having no strings of their own — their text arrives from the template
author through attributes and slots. The article bites on the exceptions: a default label, a
placeholder, an ARIA label, a screen-reader-only heading. The first block that ships one also ships
the `locale/` directory and the base English catalog.

### Article IX — Test structure & fixtures (Django)

Tests are organized for fast, targeted discovery.

- **Mirror the source tree.** Every test module mirrors the path of the module it exercises:
  `daisy_cotton_blocks/models.py` → `tests/test_models.py`. Test subpackages carry `__init__.py` to match.
  Where one source module defines several units, it stays one test module and the split is
  expressed with classes, not extra files.

  A test whose subject is not a Python module has nothing to mirror. Those paths are declared in
  `pyproject.toml` under `[tool.forge.conformance] non-mirror-paths`. That is a statement that no
  source module exists to mirror, not a waiver for a test that simply sits in the wrong place.
- **Group related tests into classes.** Within a module, tests are grouped into `Test<Subject>`
  classes, so one area can be targeted when debugging.
- **One factory per model, fixtures wrap the factory, shared setup lives in `conftest.py`.**
  Variants are expressed by overriding fields at the call site, never by subclassing a factory.
  This package defines no models, so the rule applies to whatever a test needs to construct.
- **Use the pytest-django toolchain.** Rendering assertions go through the template engine or the
  test client; query-count guards use `django_assert_num_queries`, never wall-clock timing.

### Article X — Cohesion (Python)

Related behaviour is grouped in a class, not scattered across module-level functions. Two or more
module-level functions belong on a class when they share a subject — the same data, the same first
argument, only meaningful in sequence, or named around the same noun.

In a published package a class is the extension point: a consumer who needs different behaviour
subclasses it and overrides one method, where a module of functions can only be monkey-patched.
Where Django already owns the grouping, use it rather than inventing a class.

This does not license abstraction. Article III still holds: one class grouping today's behaviour is
the goal, not a hierarchy built for a second implementation that does not exist.

## Articles not adopted

- Data-model conventions (Django) — nothing here for it to govern.

That article covers model fields, indexing decisions and migration consolidation. This package
defines no models, and Article XI forbids it from ever defining one. If that boundary is ever
crossed, the article is adopted in the same change that crosses it.

## Project articles

### Article XI — No application surface

This package ships presentation and nothing else. No models, no views, no forms, no URLs, no
migrations, no management commands. A component's content arrives from the template author through
attributes and slots, never from a queryset.

Template tags and filters are permitted and expected to be rare. Each one is justified against the
alternative of doing the work in the calling template.

The boundary is what lets a project adopt this package without a database change or a deployment
step. When a block needs something on the far side of it, such as a model, a view mixin or a form,
that work belongs to the project or to a package that does own an application surface. It is never
reimplemented here.

### Article XII — The stylesheet carries what a host cannot

`daisy_cotton_blocks/static/css/daisy-cotton-blocks.css` is the one stylesheet this package ships,
and it exists for a single reason: a host's Tailwind build scans the host's own source, so the
plain utilities used inside this package's templates are absent from it. Four rules govern it, in
order of how load-bearing they are:

1. **Utilities only, and only the ones the blocks use.** The file is built by scanning this
   package's templates, with `@source inline(...)` covering what scanning cannot see — classes
   composed at render time, and the utilities the next blocks are being designed against.
2. **No daisyUI, no theme, no preflight.** All three belong to the host. `theme(reference)` gives
   the generator the scale without writing any of it out, and the emitted utilities resolve against
   the custom properties the host's daisyUI build defines on `:root`. That is also what makes a
   block follow whatever theme is active, for free.
3. **Overlap with a host's build is expected and untested.** Two identical rules cost bytes and
   nothing else. The case that is worth knowing about is a host on a different Tailwind version,
   where one class name can carry two different declarations and link order decides.
4. **The host contract is written down, never assumed.** The daisyUI classes a block may rely on
   are listed in `HOST_PROVIDED_CLASSES` in `tests/test_stylesheet.py`. Reaching for one that is
   not listed fails the suite, which is the prompt to decide whether a host should really be
   expected to provide it.

**An emitted class is not a built class.** Naming a class in the inline list is not proof it
produces a rule. A colour utility needs the semantic palette declared in the `@theme reference`
block or it silently produces nothing and the page renders unstyled markup.

**The built file is committed, and rebuilt on the branch that changes its input.** Installing the
package needs no Node toolchain, which is what the committed artifact buys. `npm test` and the
`Built stylesheet matches its source` check both fail when the committed file and its source
disagree.

### Article XIII — Blocks are configured, not edited

A block is named for its role on the page, never for its implementation or an external design
system. Its attributes are the only supported way to change its presentation, and where a project
needs more control than they give, the answer is a template override rather than a wider attribute
surface.

**Layout is fixed per block, and an attribute never changes it.** A different arrangement is a
different block in the same family — `<c-hero.centred>` beside `<c-hero.split>` — not an option on
one component that branches internally. A block that grows a layout switch is two blocks that have
not been separated yet.

Colour comes from daisyUI's semantic palette (`primary`, `base-100` and the rest), never a literal
value and never a Tailwind palette name. That is what makes a page built from these blocks re-theme
with the rest of the site instead of drifting away from it.

Reusable markup is expressed as a Cotton component under `daisy_cotton_blocks/templates/cotton/`,
named in lowercase-kebab form, never as an `{% include %}` partial. Blocks sit at the top of that
directory rather than under a prefix of their own, so a tag reads `<c-hero.centred>`. The cost is
accepted and real: a project defining its own `cotton/hero/centred.html` shadows this one, or is
shadowed by it, depending on `INSTALLED_APPS` order.

### Article XIV — Rendered markup is a contract

Components render valid, semantic HTML and are accessible by default: a real heading hierarchy,
alternative text where an image carries meaning, keyboard-reachable interactive elements, and ARIA
attributes only where the markup alone does not convey the role. Accessibility here covers the
markup this package emits. What a host project does with its own theme, contrast and content is
its own.

Every packaged component has a test proving it renders, and a change to markup structure updates or
adds a test asserting the part of the contract it changed. Assertions are made against rendered
output, not against the presence of a class name: a class assertion proves a string is in a
template and nothing about what the browser draws.

### Article XV — Compatibility

The package is pre-1.0 and says so in the README. Block names, attribute surfaces and the set of
classes the stylesheet emits may change between minor versions, and every such change is recorded
in the CHANGELOG. Default behaviour stays stable across patch releases. There are no compatibility
aliases: an API is changed cleanly, and the CHANGELOG is how a project finds out.

Supported versions are Python 3.12 or later and the currently-supported Django releases, with the
CI matrix as the authoritative statement of both. Dropping either is a minor-version change with a
CHANGELOG entry.

**The daisyUI requirement is a compatibility surface and moves like one.** Blocks are written
against daisyUI 5. Adding a class from a later daisyUI to `HOST_PROVIDED_CLASSES` raises the floor
for every project installing this package, so it is a minor-version change with a CHANGELOG entry,
never a silent addition alongside the block that wanted it.

### Article XVI — Nothing executable is fetched at page load

No block pulls a script, a font or a stylesheet from a third-party origin. Where a block needs
behaviour, it uses what the host project already runs, and any JavaScript this package ships of its
own is bundled rather than fetched.

This is a marketing-surface library, which is exactly the kind of code that attracts a CDN tag for
an animation library or a web font. A project that installs this package gains no external origin
it did not already have.

## Quality bar

Read at planning and at review; applies to every change.

- Test coverage: **project ≥ 90%, patch ≥ 85%**, per `codecov.yml`. These are floors, not a ratchet
  toward 100%.
- Every public API change updates README and CHANGELOG in the same pull request.
- `ruff check`, `ruff format --check`, `mypy` and `deptry` pass — through
  `pre-commit run --all-files`, which is the gate, rather than a bare invocation that reports
  findings in paths the hooks exclude.
- The committed stylesheet matches its source, locally via `npm test` and in CI.
- The package builds, its metadata is valid, and the README renders on the package index with
  absolute URLs.

`djlint` is configured in `pyproject.toml` and can be run over `daisy_cotton_blocks/templates`, but it is
deliberately **not** a gate: it misfires against Cotton's `<c-vars>` syntax and needs ignore rules
first. Do not cite it as an enforced standard until it runs in CI.

## Non-negotiables

- One pull request per feature, and the repository owner merges it.
- Automation commits under the bot identity, never a human token. The default branch requires one
  approval, so the author and the approver are always distinct.
- Machine verification — tests, build, lint, the stylesheet check — gates every stage exit. No
  judgment call overrides a red gate.

---

**Version**: 2.0.0 | **Ratified**: 2026-09-17 | **Last Amended**: 2026-09-21
