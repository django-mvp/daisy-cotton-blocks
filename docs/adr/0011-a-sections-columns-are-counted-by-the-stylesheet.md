# ADR 0011 — A section's columns are counted by the stylesheet

**Status:** accepted

## Decision

`<c-section>` has no attribute for the number of columns. Each `<c-section.col>` written inside it
becomes a column. The stylesheet does the counting: the section's body turns into a grid only when
a column is its direct child, found through the `data-section-col` attribute every column carries,
and each column opens a track of its own.

Columns have one arrangement at wide widths and one below the `lg` breakpoint, where they stack in
the order written. Nothing sets a second breakpoint or a number of columns for a middle width.

The order belongs to the section. `reverse` runs the columns the other way at `lg` and above, and
a column cannot move itself. Stacked columns always follow the order written.

A section inside another section or a column adds no gutters and no vertical padding, and keeps
the copy colour around it unless it sets `invert` itself.

## Why

A Cotton component renders its children before it sees them, so it cannot count them. The
alternative is an attribute the author keeps in step by hand, `cols="3"` beside three columns,
which is one more thing to get wrong and says nothing the markup does not already say.

One breakpoint keeps the component small enough to reason about. Its job is the two or three parts
of a block: copy beside a picture, a claim beside its figures. A row of many cards that goes from
four across to two to one needs control over each width, and giving the section that control would
turn it into a grid system. A project already has one of those in its own stylesheet.

Ordering sits on the section so that the reading order on a phone is never in question. An
`order` on each column would let the stacked order and the written order drift apart, which is the
case WCAG 1.3.2 exists for.

A first version laid the row out as a flex row, which reverses any number of columns for free. A
column with padding of its own then came out wider than its neighbour, because padding is added on
top of a flex share. A grid track includes it.

## Consequences

- `reverse` works by giving each column an `order` from its position, and the stylesheet carries
  rules for six. A seventh column in a reversed section stays where it was written.
- The grid is found with `:has()`. A browser without it shows the columns stacked at every width,
  which is the phone layout and loses nothing.
- A column must be a direct child of the section. One wrapped in another element, a reveal for
  example, is no longer counted, and the wrapper becomes the body's only child.
- django-mvp ships a `<c-section>` of its own, a titled section with a toolbar. A project that
  installs both gets whichever app is listed first in `INSTALLED_APPS`.
