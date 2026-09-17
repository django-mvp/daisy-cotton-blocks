# ADR 0001 — Ship a supplementary stylesheet rather than reuse django-mvp's alone

**Status:** accepted

## Decision

The package ships its own stylesheet, `mvp_bits/static/css/mvp-bits.css`, loaded after
django-mvp's. It contains only utilities django-mvp's build does not already emit, it is built from
a hand-written whitelist rather than by scanning templates, and the built file is committed so that
installing the package needs no Node toolchain.

The rules that govern it are Article XII of `CONSTITUTION.md`. This record is why they are those
rules and not others.

## Why

The starting intent was to ship no CSS at all and build every block from what django-mvp already
emits. That does not survive contact with django-mvp's build.

django-mvp's stylesheet is Tailwind's theme and preflight, the daisyUI component set, and a curated
pack of layout utilities. Measured against it, the utilities a modern hero needs are mostly absent:
no gradients, no transforms, no `aspect-*`, no `ring-*`, no `animate-*`, and a spacing scale that
stops at 3rem. The curation is deliberate — `shadow-*` is excluded on the argument that a loose box
shadow works against a unified interface — and it is right for an application shell. It is not
enough to build a landing page from.

Three alternatives were weighed against shipping a supplement.

**Push the missing utilities upstream into django-mvp.** Rejected: it would grow the stylesheet
every project loads for the benefit of the ones building a marketing page, and it asks django-mvp
to carry an opinion about a surface it does not own.

**Scan this package's templates, the way django-mvp scans its own.** Rejected: scanning re-emits
every class the templates share with django-mvp, which is precisely the duplication the design
exists to prevent. Two stylesheets defining the same selector is a cascade problem that surfaces as
an inexplicable override months later. Whitelisting by hand costs an edit per new class and makes
the overlap measurable, which is what `tests/test_stylesheet.py` measures.

**Ship a full standalone build with its own theme and preflight.** Rejected: it would re-declare
the custom properties django-mvp already defines, and blocks would then follow their own colours
rather than the host project's daisyUI theme. Emitting utilities against a `theme(reference)` block
instead means they resolve against whatever theme is live, which is what makes a block re-theme for
free.

The committed build artifact follows from the same goal. A Python package that requires Node to
install is a package most projects will not adopt, so the cost lands on the two or three
contributors who change the whitelist rather than on every consumer.

Measured when the decision was taken: 269 classes here, 2333 in django-mvp, overlap 0.

## Revisit if

django-mvp's curated utility pack grows to cover what page blocks need, which would shrink the
supplement toward nothing and make a single stylesheet viable again. Or if the hand-written
whitelist stops being maintainable — the signal would be contributors closing its deliberate gaps
faster than the tests catch them, which would mean the boundary needs to be derived from
django-mvp's build rather than tracked by hand.
