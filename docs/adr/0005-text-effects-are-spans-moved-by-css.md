# ADR 0005 — Text effects are spans, moved by CSS alone

**Status:** accepted

## Decision

A text effect is one inline `<span>` around the words it changes. The ones that move are driven by
keyframes in the package stylesheet, and the package ships no JavaScript for them. The rules that
follow, each the reason for something in a template:

1. **Every animation sits behind `motion-safe:`, and the words at rest are the finished words.**
   Under `prefers-reduced-motion: reduce` a gradient holds still, a marker is already drawn and a
   typed line is already typed. The marker and the typewriter get this from keyframes that have a
   start and no end.
2. **An effect that keeps going takes `repeat`.** Left out, it runs for as long as the page is
   open. Given a number, it runs that many times and stops. The typewriter's caret blinks three
   times and goes, whatever it is given.
3. **A pace of `0` writes no animation at all.** An animation's length is a division by its pace.
   Divided by nothing, it never ends or never starts, and an opacity animation of no length on a
   blurred layer has stalled a page. So `speed="0"`, `frequency="0"` and `pulse="0"` leave the class
   out, and the words render at rest.
4. **A shimmer's pace and its frequency are set by the width of its background.** CSS has no gap
   between two runs of an animation, and a keyframe percentage cannot be a variable. So one run is
   one wait, the band moves at one pace through all of it, and the background is as many times the
   width of the words as the wait is times the crossing. The band is measured in ems so it keeps
   its width whatever that comes to.
5. **Typewriter and wave take their line as an attribute.** A template can split a string into
   letters and cannot split markup. `text="{{ title }}"` reaches a component already escaped, so
   the `plain` filter undoes that before the line is split, and each letter is escaped again as it
   is written.
6. **An effect that draws the words more than once gives them to a screen reader once.** The glow's
   halo and the glitch's slices are copies marked `aria-hidden`. Typewriter and wave hide their
   letters the same way and carry the whole line in one visually hidden span.
7. **Wave wraps each word.** A letter has to be a box of its own to be moved, and a line may break
   between any two such boxes, which would split a word in half.
8. **Colours are palette names, not contrast pairs.** A gradient, an outline or a raised edge in
   `primary` makes no promise against the page behind it, which is why those three say they are
   for headings. Shimmer leaves the words their own colour and is safe at any size.

## Why

[ADR 0004](0004-moving-backgrounds-are-css-only.md) gives the reasons the package has no script of
its own for movement, and they hold here unchanged: nothing for a host to load, order or allow, no
cost off screen, and a failure that leaves the words on the page.

A span is the smallest thing that works. It goes wherever words go, takes its size and weight from
whatever it sits in, and leaves the heading level to the page.

## What it costs

- **There is no pause control.** WCAG 2.2 success criterion 2.2.2 asks for a way to pause, stop or
  hide anything that starts moving on its own and keeps going for more than five seconds beside
  other content. CSS alone cannot offer one. A page that has to meet it sets `repeat` on every
  looping effect, or supplies its own control. Backgrounds carry the same cost, but a background is
  decoration and these are words.
- **Three effects repaint.** A fill clipped to its letters cannot be moved by the compositor, so
  the gradient, the shimmer and the marker animate a background and repaint the few words they
  cover. ADR 0004's rule against that was written for a layer the size of a block.
- **Glow and glitch do not wrap.** A copy laid over the words needs a box to be laid over, so the
  phrase is an inline block and stays on one line. Their slot is also rendered more than once, so
  it takes plain words and nothing carrying an `id`.
- **A shimmer cannot cross more slowly than it comes round.** Below that the band would still be
  on the words when the next run began, so the width is held at a floor.
- **A number on `style` needs inline styles.** Under a content security policy that forbids them,
  every effect falls back to its defaults ([ADR 0003](0003-amounts-are-numbers-written-to-style.md)).
