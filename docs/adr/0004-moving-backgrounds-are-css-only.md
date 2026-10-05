# ADR 0004 — Backgrounds move by CSS alone

**Status:** accepted

## Decision

The backgrounds that move are driven by keyframes in the package stylesheet. The package ships no
JavaScript for them. Six rules follow from that, and each is the reason for something in a
template that would otherwise look arbitrary.

1. **Every animation sits behind `motion-safe:`.** Under `prefers-reduced-motion: reduce` each
   background draws the same picture and holds it still.
2. **Only `translate`, `scale` and `opacity` are animated.** The compositor moves a layer without
   repainting it. Animating `background-position` would repaint every frame.
3. **Parallax is a view timeline named on its own frame.** The frame is the size of the block. The
   layer inside is taller, by exactly what it travels, and would measure a longer crossing if the
   timeline were taken from it. While the block crosses the screen the page moves it by the block's
   height plus the viewport's, and the layer falls behind by `1 - speed` of that, which is what
   `--parallax-shift` is half of.
4. **Nothing between a parallax layer and the page may use `overflow: hidden`.** It makes an
   element a scroll container, and a view timeline measures against the nearest one, so the layer
   would never move. The parallax frame and the hero blocks clip with `overflow: clip`.
5. **Where a browser has no scroll-driven animation, parallax does nothing.** Its classes sit
   behind `supports-[animation-timeline:view()]`, and the wrapped background renders cropped and
   still.
6. **Distances that depend on the block are container units.** The horizon's perspective is a
   share of the block's height so its vanishing line and its mask agree in a short block and a
   tall one. Particles and streaks travel in `cqh` and `cqmax` so they clear the block whatever
   its shape.

## Why

`CONSTITUTION.md` Article XV keeps third-party scripts out, and a script of the package's own
would be the first thing a host has to load, order and allow for a purely decorative layer. CSS
needs none of that, costs nothing when the block is off screen, and fails to a still picture.

## What it costs

- **The horizon shimmers towards its vanishing line.** The browser draws the floor flat and then
  squeezes it, and a rule squeezed thinner than a pixel flickers as it moves. The cross rules are
  drawn three pixels deep so they land at about one, and the mask fades the floor out before the
  worst of it. Small squares at high speed still show it.
- **Hyperspace needs `mod()`.** Each streak carries only its number and works out its bearing,
  starting point, thickness, duration and delay from it, which is what lets `density` be any
  number. The bearing steps by the golden angle, which spreads any count evenly round the circle.
  The loop pads a string to the count because a template has no other way to repeat, and the
  string is cut from a fixed three hundred so no value can ask for more.
- **There is no pause control.** The looping backgrounds run for as long as the page is open.
