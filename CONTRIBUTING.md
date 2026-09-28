# Contributing

## Setup

```bash
uv sync
npm install
uv run pre-commit install
```

`npm install` is only for building the stylesheet. Nothing under `node_modules` is needed at runtime.

## Checks

```bash
uv run pytest
uv run pre-commit run --all-files
npm test
```

`npm test` fails when the committed stylesheet no longer matches its source. The example project runs with `uv run python manage.py runserver`.

## Building the stylesheet

The built CSS is committed, so installing the package needs no Node toolchain. After changing what it emits:

```bash
npm run build:css     # or watch:css
```

`assets/daisy-cotton-blocks.css` is the entry. It scans this package's own templates, so a utility a new block uses is picked up by rebuilding. The `@source inline(...)` entries cover what scanning cannot see: classes composed at render time, and the utilities the next blocks are being designed against. `tests/test_stylesheet.py` measures the result.

## Rules

Every change is held to [`CONSTITUTION.md`](CONSTITUTION.md) and the two pages it points at:

- [Testing standards](docs/contributing/standards/testing.md): what gets a test, the test-first cycle, test structure and the coverage floors.
- [Code documentation standards](docs/contributing/standards/code-documentation.md): docstrings, component annotations and comments.
