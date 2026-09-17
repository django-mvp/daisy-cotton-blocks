# Brainstorm

Working notes from the conversation that started this package. These are
conclusions, not ratified decisions — anything here that hardens into a rule
belongs in `CONSTITUTION.md`, and anything that turns out to be a real
architectural commitment belongs in an ADR.

## The gap

django-mvp is an application shell. It has no answer for the pages in front of
the application: the landing page, the pricing page, the sign-up pitch. Its
existing `<c-section>` is a titled content region with a toolbar, and its
`<c-section.hero>` is a daisyUI hero with a background image. Both are
application chrome. Neither is marketing furniture.

The reference point for the idea is [reactbits.dev](https://reactbits.dev/),
scaled well down. Not the WebGL and canvas work — configurable blocks that make
an ordinary page look designed.

## Prior art

Surveyed before starting. Nothing occupies this niche.

**django-cotton-ui** (wrabit, who also wrote django-cotton) is the closest
thing. MIT, Tailwind v4 and Alpine, healthy: v0.3.3 released 2026-09-14, thirty
stars, no open issues, first published June 2026. It ships forty-three
components — accordion, button, combobox, datepicker, dialog, navbar, table,
tabs, toast and the rest. It has no hero, no pricing block, no call to action,
no testimonial, no feature section. It is an alternative to django-mvp's
component layer, not to this package.

**shadcn-django** (239 stars) last released and last pushed 2026-01-13. It is a
copy-in CLI on the shadcn model rather than an installable library, targets
shadcn/ui aesthetics rather than daisyUI, and ships no marketing blocks.

Everything else serving this space is HTML copy-paste: Tailwind UI's marketing
blocks, Flowbite, Preline. None are Django packages and none theme off daisyUI.

The empty niche is specifically: daisyUI-themed, Cotton-native page blocks that
inherit whatever theme the host project already runs.

## The stylesheet, and why it works the way it does

The original intent was to add no CSS at all and build everything from what
django-mvp ships. That does not survive contact with django-mvp's build.

django-mvp's stylesheet is Tailwind's theme and preflight, the whole daisyUI
component set, and a hand-curated pack of layout utilities. Measured against it,
the utilities a modern hero actually needs are mostly absent: no gradients, no
transforms, no `aspect-*`, no `ring-*`, no `animate-*`, and a spacing scale that
stops at `12` (3rem). It ships `transition` and the short durations but nothing
transformable to apply them to. That curation is deliberate — `shadow-*` is
excluded on the grounds that a loose box-shadow works against a unified UI — and
it is the right call for an application shell. It is simply not enough to build
a landing page from.

So this package ships a supplement. The constraints on it, in order of how
load-bearing they are:

1. **Additive only.** Zero overlap with django-mvp's build. Not "minimal
   overlap" — zero, measured.
2. **Tailwind only.** No daisyUI plugin. Components use daisyUI classes;
   django-mvp is what emits them.
3. **No theme, no preflight.** `theme(reference)` gives the utility generator
   the scale without writing any of it out, and the emitted utilities resolve
   against the custom properties django-mvp already defines. This is also what
   makes the components theme-follow for free.
4. **No template scanning.** `source(none)`, and every class whitelisted by
   hand. Scanning this package's templates would re-emit whatever they share
   with django-mvp, which is the duplication the whole design exists to avoid.
5. **Hard dependency, no fallback.** Load django-mvp's stylesheet first or these
   components are unstyled. That is the intended failure mode, not a bug to
   defend against.

### The arbitrary boundary

Rule 1 cannot be satisfied by reading django-mvp's safelist. Its build scans
daisyUI's component sources for class tokens, so daisyUI's own internal usage
leaks classes into the output that nobody listed anywhere. The result is a
boundary with no logic to it:

- `py-16` and `mb-16` ship; `py-20`, `py-24` and `py-32` do not.
- `transition-colors`, `-opacity` and `-shadow` ship; `transition-all` and
  `-transform` do not.
- `ease-out` and `ease-in-out` ship; `ease-linear` and `ease-in` do not.
- `space-y-4` ships; no other `space-y` value does.

It will move again on the next daisyUI upgrade. The whitelist in
`assets/mvp-bits.css` therefore has gaps in it that read as typos, and
`tests/test_stylesheet.py` is what stops someone closing them.

Measured at scaffold time: 269 classes here, 2333 in django-mvp, overlap 0.

## Scope

Presentation only: no models, views, forms, URLs or migrations. Template tags
and filters are allowed but expected to be rare, and each one has to earn its
place.

The catalogue is open-ended on purpose. The package grows as blocks get
designed, and is not committed to filling out a fixed taxonomy. The scope
boundary is the no-application-code rule, not a list of permitted component
categories.

## First target

A SaaS-style landing page, built from roughly five blocks: a hero, a configurable
one/two-column section, a call to action for sign-in and sign-up, and a pricing
overview. Whatever else that page turns out to need is the rest of the first
release.
