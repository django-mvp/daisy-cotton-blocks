# Roadmap — daisy-cotton-blocks

**Date:** 2026-09-21

This document was designed against [GOALS.md](../GOALS.md). See also [CONTEXT.md](../CONTEXT.md) for domain terminology and [CONSTITUTION.md](../CONSTITUTION.md) for project standards.

The first item is already built and is carried here so the sequence reads whole.

## Versioning

| Version | Gate |
|---------|------|
| `0.0.x` | Building toward the Essential goals. Pre-viable, expect churn, nothing published. |
| `0.1.0` | All Essential goals delivered. The minimum usable release, and the first publish. |
| `0.1.x` → `0.x` | Advancing the Expected goals, at whatever granularity the work takes. Patches are fixes. |
| `1.0.0` | All Expected goals delivered. The complete, dependable release. |
| `1.x` | Stable line: non-breaking fixes and additive blocks only. |
| `2.0` | Next major, where breaking changes go. |

A goal is not one minor version. Some take several, and one minor can move two. Once `1.0` ships, a breaking change never goes out as `1.x` — it waits for the next major.

## Essential goals: v0.1.0

Everything needed to reach a minimum usable release.

### R1 — The stylesheet and the host contract

*Delivered · needs verification · advances G2, G3*

The package ships one stylesheet carrying the plain Tailwind utilities its blocks use, and leaves daisyUI, the active theme and the page reset to the project installing it. Which daisyUI classes a block may rely on is written down and enforced rather than assumed, so a project knows what it has to bring. Installing the package needs no front-end toolchain and changes nothing about how the project already behaves.

Serves G2 and G3.

### R2 — Hero blocks

*feature · advances G1, G5*

The block at the top of a page, and the first one anybody will reach for. It sets the conventions every later family follows: how content is passed in, how a secondary action is expressed, how a block behaves when an optional piece is left out, and what a block does on a narrow screen. Getting those wrong here means correcting them everywhere later, which is why this comes before anything else.

**Deliverables:**

- Several distinct hero layouts, each its own block, covering at least a centred arrangement and a split arrangement with room for an image or mockup.
- A settled way of passing a heading, supporting copy and one or two actions into a block.
- Behaviour at narrow widths that is specified and tested, not incidental.
- Rendered-output tests and documentation shipped with the blocks.

Serves G1 and G5. Out of scope: any content that would come from a queryset.

### R3 — Content section blocks

*feature · advances G1, G5*

The workhorse between the hero and the foot of the page: a titled region holding copy, a media panel, or a grid of short items. Most of a page's length is made of these, and a page cannot be assembled without them.

**Deliverables:**

- Several distinct section layouts, including a single-column arrangement and a two-column arrangement whose media side can be placed on either edge.
- A repeating-item arrangement for feature lists, where the number of items is the template author's to decide.
- Control over which side content sits on at wide widths without duplicating the markup at narrow ones.
- Rendered-output tests and documentation shipped with the blocks.

Serves G1 and G5. Out of scope: pricing and testimonial arrangements, which are their own families later.

### R4 — Call to action blocks

*feature · advances G1, G5*

The block that asks the reader to do something, and the last piece the first complete page needs. Small, but it is where a page converts, and it appears more than once on most pages.

**Deliverables:**

- Several distinct arrangements, covering a full-width band and a contained panel.
- Support for a primary action alone and for a primary paired with a secondary.
- Rendered-output tests and documentation shipped with the blocks.

Serves G1 and G5. Out of scope: anything that submits, which needs a view and belongs to the project.

### R5 — A browsable catalogue

*feature · advances G4*

A block cannot be chosen from its name. Somebody deciding between one hero and another needs to see both, and needs to know what each accepts without opening a template. This is what makes the package adoptable rather than merely installable, and it is the point at which the package can describe itself.

**Deliverables:**

- Every block browsable, rendered, with its options visible and adjustable.
- A documentation convention each block carries, so a block added later is browsable without extra work.
- That convention enforced automatically, so an undocumented or mis-documented block is caught rather than noticed.
- A page built entirely from the package's own blocks, demonstrating the catalogue and serving as the project's own front page.

Serves G4. Out of scope: hosting or publishing that page anywhere.

## Expected goals: v1.0.0

What a complete and dependable version carries beyond the minimum.

### R6 — Pricing blocks

*feature · advances G1, G5*

The family every comparable library ships and the most-requested page after the landing page itself. Held back from the first release because a convincing pricing block has more arrangements than a hero and none of them is needed to put a page on screen.

**Deliverables:**

- Several arrangements covering a plan comparison and a single highlighted plan.
- A way to mark one plan as recommended without hard-coding which.
- Per-plan feature lists whose length is the template author's to decide.

Serves G1 and G5.

### R7 — Social proof blocks

*multi-feature · advances G1, G5*

Testimonials, logo clouds, statistics and the people behind the product. Four small families that do the same job on a page and are worth building together, because they share a repeating-item shape and are almost never used alone.

Serves G1 and G5.

### R8 — Question and answer blocks

*feature · advances G1, G5, G6*

A frequently-asked-questions region, expanding and collapsing. The first family whose behaviour is not purely static, which makes it where the approach to interaction gets settled.

Serves G1, G5 and G6.

### R9 — Page edges

*feature · advances G1, G5*

The foot of the page and the strip across the top of it: a footer carrying links and small print, and an announcement bar. Both frame a page rather than filling it, and a page assembled entirely from this package is not complete without them.

Serves G1 and G5.

### R11 — Contact and newsletter blocks

*feature · advances G1, G5*

A way to ask the reader for something back: a contact region and a signup strip. The blocks render the fields and the framing; where the submission goes and what happens to it belong to the project, which is the line that keeps them presentation.

**Deliverables:**

- A contact arrangement pairing a message area with the details a reader might want instead.
- A newsletter arrangement compact enough to sit inside another region.
- Somewhere for the project to put its own submission target and token, without this package knowing anything about either.
- A shape that carries a validation message when the project has one to show, and looks deliberate when it does not.

Serves G1 and G5. Out of scope: handling a submission, validating one, or storing anything.

### R10 — Motion and visual effect

*feature · advances G6*

A shared approach to movement that individual blocks draw on: what enters, how, and what stays still. Deliberately late, because a motion vocabulary invented before there are blocks to move is a guess, and because a page that works without it must come first.

Serves G6. Out of scope: anything that moves by default, and anything that ignores a reader's stated preference for reduced motion.
