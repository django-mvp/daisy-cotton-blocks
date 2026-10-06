# ADR 0006 — Reveals follow the scroll position

**Status:** accepted

## Decision

The reveals that respond to scrolling are tied to the scroll position by a CSS view timeline. The
package ships no JavaScript for them. A reveal is at its start when the element first shows at the
foot of the screen and at rest once it has come in, and it is wherever the scroll puts it in
between. Scrolled back up, it runs backwards.

The rules that follow, each the reason for something in a template:

1. **Every scroll animation sits behind `motion-safe:` and `supports-[animation-timeline:view()]`.**
   Under `prefers-reduced-motion: reduce`, and in a browser without scroll-driven animation, the
   content renders at rest. No class hides content and waits for something else to show it.
2. **The keyframes have a `from` and no `to`.** The end of every reveal is whatever the element
   already is, so the reveal cannot leave its own styling behind.
3. **An arrival is measured against the element's own entry, not against the screen.** The range
   runs from `entry 0%` to `entry 100%`, times `over`. A range measured against the screen cannot
   finish for the last element on a page, which stays part-way in for good.
4. **A wrapper never uses `overflow: hidden`.** It would become the scroll container the timeline
   measures against, and nothing inside would move ([ADR 0004](0004-moving-backgrounds-are-css-only.md)
   rule 4). The same property stops a stacked panel sticking.
5. **Cascade counts its children with `nth-child`, up to twelve.** `sibling-index()` would count
   any number and is not in every browser. `per` exists because CSS cannot see a grid row: without
   it the second row waits for the whole of the first.
6. **Words takes its text as an attribute.** A template can split a string on its spaces and
   cannot split markup. The text is escaped once before it is split, so a word is written out as
   it stands whether the caller passed a string or a variable.
7. **Hover opens on keyboard focus as well as on a pointer, and its frame is focusable.** A caption
   with no link in it would otherwise be out of reach without a mouse. Where the device reports
   `hover: none` the caption shows all the time.
8. **Stack is `position: sticky` and nothing else.** It needs no animation support, and nothing
   moves that the reader did not move.

## Why

`CONSTITUTION.md` Article XV keeps third-party scripts out, and [ADR 0004](0004-moving-backgrounds-are-css-only.md)
gives the reasons the package has none of its own for movement: nothing for a host to load, order
or allow, no cost off screen, and a failure that leaves a finished page.

The alternative is the reveal that plays once, on a timer, when the element arrives. It needs an
`IntersectionObserver` to notice the arrival and a class that hides the content until the script
has run, which is content a failed or blocked script never shows.

## What it costs

- **A reveal does not replay and does not hold.** It follows the scroll in both directions. A page
  that wants the play-once kind needs a script this package does not ship.
- **Two reveals animate more than ADR 0004 allows a background.** Wipe animates `clip-path` and the
  `blur` effect animates `filter`. Neither lays the page out again, but both repaint as they go.
  A background runs for as long as the page is open and a reveal runs only while its element is
  entering the screen, which is why the cost is accepted here and not there.
- **A wipe stays clipped to its box.** The frame keeps `clip-path: inset(0)` once it is done, so
  a shadow belongs on an element around it.
- **A dim word is below the contrast body text needs** until the scroll reaches it. Words is for
  one short, large statement, and its page says so.
- **Cascade stops staggering after twelve children.**
