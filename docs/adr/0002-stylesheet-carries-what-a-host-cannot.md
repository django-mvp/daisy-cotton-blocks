# ADR 0002 — The stylesheet carries what a host cannot, not what a host lacks

**Status:** accepted

Supersedes [0001](0001-supplementary-stylesheet.md), which designed the stylesheet as a supplement
to django-mvp's.

## Decision

The package ships one stylesheet, `daisy_cotton_blocks/static/css/daisy-cotton-blocks.css`,
containing the plain Tailwind utilities its own templates use and nothing else. It is built by
scanning those templates, with an inline list covering classes composed at render time. daisyUI,
its themes and Tailwind's preflight come from the host project. Overlap between this stylesheet and
a host's own build is expected and is not tested for.

The rules that govern it are Article XII of `CONSTITUTION.md`. This record is why the design
changed.

## Why

ADR 0001 defined the stylesheet by subtraction: emit what django-mvp's build does not, measure the
overlap at zero, whitelist every class by hand because scanning would re-emit whatever the
templates shared with django-mvp. That design was correct while django-mvp was a hard dependency
and the only host the package would ever have.

The package is no longer coupled to django-mvp. Nothing in it imports django-mvp, and it never did
— the dependency was entirely at the stylesheet level. Positioned instead at any Django project
running Cotton and daisyUI, subtraction has nothing left to subtract from, and it breaks in a way
worth stating precisely: a host's Tailwind build scans the host's own source, so it never reaches
this package's templates in site-packages. daisyUI's component classes survive that, because a
daisyUI build emits them wholesale. The plain utilities a block uses do not. A stylesheet defined
as "what django-mvp lacks" would leave those missing on every host that is not django-mvp.

Two alternatives were weighed.

**Ship a general-purpose utility pack and let django-mvp consume it.** Rejected. It points an
application shell at a marketing block library, which is the wrong direction for a dependency, and
it strands any third-party integration that wants those utilities without wanting these blocks.
Curating a "common utilities" list also rebuilds the arbitrary boundary this change exists to
delete, one repository to the left.

**Ship a daisyUI build too, for projects that have none.** Rejected. A project running Cotton with
daisyUI already has daisyUI by definition, and shipping a copy would put this package on daisyUI's
release cadence and force a choice of which themes to include, which has no good default.

What the change buys, beyond working on more than one host: the hand-written whitelist goes, and
with it the gaps that read as typos and were not. Those gaps existed because django-mvp already
emitted `py-16`, `space-y-4` and `transition-colors`, having picked them up from scanning daisyUI's
own sources — a boundary nobody wrote down, which moved on every daisyUI upgrade, and which needed
a test and three paragraphs of explanation to stop a contributor "fixing" it.

What it costs is duplication. A project running django-mvp now loads two stylesheets that both
define `py-20`. Two identical rules cost bytes and nothing else. The case that does matter, and the
one to expect a bug report from, is a host on a different Tailwind version: the same class name can
carry different declarations, and which applies comes down to link order.

## Revisit if

Tailwind gains a way for a host build to scan an installed package's templates, which would remove
the reason this stylesheet exists at all. Or if version skew between this package's build and a
host's stops being theoretical — the signal would be a report of a block rendering differently
depending on stylesheet order, at which point the fix is likely to be scoping this package's
utilities into their own cascade layer rather than reverting to subtraction.
