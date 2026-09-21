# Brainstorm

Working notes from the conversation that started this package. These are
conclusions, not ratified decisions — anything here that hardens into a rule
belongs in `CONSTITUTION.md`, and anything that turns out to be a real
architectural commitment belongs in an ADR.

## The gap

Component libraries in this space are application shells. They have no answer
for the pages in front of the application: the landing page, the pricing page,
the sign-up pitch. django-mvp, where the idea started, is representative — its
`<c-section>` is a titled content region with a toolbar and its
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

## The stylesheet

The original intent was to add no CSS at all and build everything from what a
host project already ships. That does not survive contact with how Tailwind
builds: a host scans its own source and never reaches an installed package's
templates, so the plain utilities a block uses are absent from it however
complete the host's own build is.

The reasoning that follows from that, and the reasoning it replaced, are in
`docs/adr/0002` and `docs/adr/0001`. The rules themselves are Article XII of
`CONSTITUTION.md`. Nothing about the stylesheet is settled here.

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
