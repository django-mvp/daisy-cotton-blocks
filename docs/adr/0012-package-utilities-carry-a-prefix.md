# ADR 0012 — The package's utilities carry a prefix

**Status:** accepted

Amends [0002](0002-stylesheet-carries-what-a-host-cannot.md). The stylesheet still carries what a
host cannot. What changes is what its classes are called.

## Decision

The stylesheet is built with Tailwind's `prefix(dce)`, and every plain utility in a package
template is written with it: `dce:flex`, `dce:lg:grid-cols-2`, `dce:from-primary`. No class this
package emits shares a name with a class a host's build emits. daisyUI's component classes stay
unprefixed, because they are the host's.

The prefixed utilities sit in a layer of their own, `utilities.dce`, nested inside `utilities`. A
nested layer ranks below the outer layer's own rules, so a host's utility beats one of these in
either link order: `hidden` passed to a block overrides the block's `dce:flex`. daisyUI nests its
components the same way, in `utilities.daisyui`, and the entry file names that layer first, so a
package utility still beats a daisyUI component.

`tests/test_stylesheet.py` holds all of that. One test fails if the stylesheet emits a
class without the prefix. Another loads a host stylesheet and this one into a browser, in the
order the README gives and in the other, and reads the computed styles back.

## Why

ADR 0002 called overlap between the two stylesheets harmless: two identical rules cost bytes and
nothing else, unless the host ran a different Tailwind version. That is true of one class at a
time and false of two.

Tailwind makes `md:flex` beat `hidden` by writing it later in the file. A media query adds no
specificity, so position is all that separates them. Both stylesheets put their utilities in the
`utilities` layer, and across two files position means link order. With this package's stylesheet
linked second, as the README asked, its `.hidden` came after the host's `.md\:flex`, and every
`hidden md:flex` element in the host's own templates stayed hidden at every width. Its `.flex`
likewise beat the host's `.sm\:hidden`. This was measured on 2026-10-05 against django-mvp 0.26
in headless Chromium, on a navigation link that had disappeared.

Linking the stylesheets the other way round moves the fault and does not remove it. The host's
`.grid-cols-1` then comes after this package's `.lg\:grid-cols-2`, and `<c-hero.split>` never
reaches two columns on a host that defines the first and not the second. Neither order is right,
because the fault is the shared name.

Three alternatives were weighed.

**A cascade layer of the package's own.** This is what ADR 0002 expected the fix to be. A layer
ranks every rule in it above or below every rule in the host's `utilities` layer, which is the
same choice as link order with the same two outcomes. The layer this stylesheet does use settles
which of two differently named classes wins. It could not have separated two classes with one
name.

**Emit only what the host lacks.** That is ADR 0001, and the reasons 0002 gave for leaving it
stand: there is no single host to subtract from.

**Raise the specificity of the package's rules,** by scoping them under a block's root. A plain
`hidden` scoped that way still beats a host's `md:flex` on anything a template author puts in a
slot.

## What it costs

- **Templates are longer.** Every utility gains four characters, and a contributor has to remember
  them. A class written without the prefix resolves to no rule and fails the suite, so a slip is
  caught before it ships.
- **Unprefixed utilities are gone from the stylesheet.** A project that leaned on this package for
  `py-20` or `bg-base-200` in its own templates has to get them from its own build, or write
  `dce:py-20`.
- **The prefix reaches theme variables.** A utility reads `--dce-text-5xl`, not the host's
  `--text-5xl`, and falls back to Tailwind's default. Two things are passed through to the host's
  own properties in the `@theme reference` block: the semantic palette, which is what makes a block
  follow the theme, and `--spacing`. The rest of Tailwind's scale — type sizes, radii, container
  widths — no longer follows a host that has customised it. A host that wants one to can set the
  `--dce-` property.
- **The stylesheet states Tailwind's layer order.** With no shared names left, link order had one
  way remaining to do damage. Layers rank by first mention, and this file linked first mentioned
  `utilities` before the host mentioned `base`, which put the host's preflight above every utility
  on the page. The entry file now opens with `@layer theme, base, components, utilities;`, the
  line a Tailwind build opens with, so either order gives the same ranking. The README still asks
  for the host's stylesheet first, and the browser test measures both.

## Revisit if

Tailwind gains a way for a host build to scan an installed package's templates, which would remove
the reason this stylesheet exists at all.
