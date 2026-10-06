# ADR 0009 — A count is started by scroll and timed by the clock

**Status:** accepted

## Decision

`<c-stats.count>` counts up in CSS, with no script, in two parts:

1. **The scroll position throws a switch.** A scroll-driven animation on the figure sets a custom
   property, `--dce-seen`, from 0 to 1 as the figure comes into view, and back as it leaves.
2. **The switch starts a transition.** A style query on that property sets `--dce-count`, a
   custom property registered as a whole number, to the number asked for. A transition on
   `--dce-count` does the counting, and a CSS counter writes its value out.

The finished number is in the markup as ordinary text. Where the browser supports all of this and
the visitor has not asked for reduced motion, that text is hidden visually and the counter is
shown in its place. Everywhere else the text is what is seen. A screen reader is always given the
text and never the counter.

## Why

The reveals tie their movement directly to the scroll position
([ADR 0006](0006-reveals-follow-the-scroll-position.md)). A count cannot do that. A figure that
stops halfway up the screen would stop halfway through its count and show 23 where the truth is
31. A half-faded card is harmless. A wrong number is not.

Running the count on the clock means it always finishes on the number given, however far the page
is scrolled. Starting it from the scroll position keeps it script-free, like every other movement
in the package ([ADR 0004](0004-moving-backgrounds-are-css-only.md)).

## Consequences

- **Whole numbers only, with no separators.** A CSS counter cannot format a number. Text before
  and after the number carries a currency sign, a unit or the decimals.
- **"In view" is measured against the nearest scrolling box.** daisyUI's `stats` row is one, so a
  counting stat inside it is always in view and counts once as the page loads. `<c-stats.band>`
  and a plain grid are not, and a count there waits for the visitor.
- **A browser without scroll-driven animation or style queries shows the finished number.** That
  is a complete result, not a degraded one.
- The stylesheet carries an `@property` rule and the `dce-seen` keyframes for this, beside the
  other movement it defines.
