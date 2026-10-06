# ADR 0008 — Stats draw no charts

**Status:** accepted

## Decision

Nothing in this package draws a chart, or anything that reads as one. That includes the small
line of recent values, a sparkline, that often sits under a figure.

A trend stat leaves room instead. Whatever a page author puts between the tags of
`<c-stats.trend>`, `<c-stats.trend-inline>`, `<c-stats.trend-corner>` or `<c-stats.trend-footer>`
is placed under the figures, and nothing is rendered there when the tags are empty.

A bar showing one share of a whole is not a chart in this sense. `<c-stats.progress>` uses the
`progress` element, through daisy-cotton's `<c-progress>`.

## Why

Charting is django-mvp-charts' job. A sparkline drawn here would be a second, smaller charting
layer with its own scaling rules, no axis, no values and no hover, sitting beside a package that
does all of those properly. Two ways to draw a line in one stack drift apart.

A first version of this family did include a sparkline stat, drawn as inline SVG from a list of
numbers. Apart from the line it was a plain stat, so removing it cost nothing a slot does not give
back.

## Consequences

- A project that wants a chart beside a figure brings its own, from any charting package.
- This package gains no charting code, no filter that turns numbers into coordinates and no
  script.
- The four layouts with room for a chart accept any content there. The package does not check
  that it is a chart.
