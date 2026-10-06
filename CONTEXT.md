# daisy-cotton-ext

Domain model for daisy-cotton-ext — a library of extended components and page blocks for Django
projects running Cotton and daisyUI.

The terms below are the ones to use in issues, commits, tests and block names. Several of them
exist to keep two neighbouring ideas apart, because the obvious word covers both and the
distinction is the one people get wrong.

## Core concepts

**Block**:
The unit this package ships: a self-contained region of a page, rendered by one Cotton component
and configured entirely through its attributes. A hero is a block. A pricing table is a block.
Content comes from the template author, never from a queryset.
_Avoid_: widget, module, element, panel.

**Section**:
The shell most blocks are built in, `<c-section>`: a `section` element that spans the page, a
background layer behind it, and a body held to a chosen width. A section is a component a block
is made from, and a page author can use it directly. Say *block* for the finished region of a
page and *section* only for this component.

**Column**:
One `<c-section.col>` inside a section. Columns sit side by side at wide widths and stack in the
order written below the `lg` breakpoint.
_Avoid_: grid, cell (a grid wraps and has rows, which columns do not).

**Extended component**:
A single component that goes further than its daisyUI counterpart: more structure, more options,
or behaviour the base component leaves out. It is still one component doing one job, which is what
separates it from a block. A component that maps one-to-one onto a daisyUI component is neither,
and belongs in daisy-cotton.
_Avoid_: advanced component, pro component, block (a block is a region of a page).

**Block family**:
All the blocks that do the same job on a page, sharing a tag prefix: `hero` is a family, and
`<c-hero.centred>`, `<c-hero.split>` and `<c-hero.with-mockup>` are blocks within it. A family is a
naming convention rather than a thing in the code — there is no shared template and no base
component behind one.

**Layout**:
What distinguishes one block from its siblings in the same family: where the copy sits, whether
there is an image and which side it is on, how the content stacks on a narrow screen. Layout is
fixed per block. Wanting a different one means reaching for a different block, never passing an
attribute.
_Avoid_: variant (see below), style, mode.

**Option**:
An attribute that changes a block's presentation without touching its layout: background, icon,
size, alignment, whether a secondary action renders. Options are the whole configuration surface
of a block.

An option that sets an amount takes a number: speed, intensity, opacity, and a size where fine
control is the point, such as how far apart a grid's rules sit. An option that picks from a
designed scale takes a name: a font size, a button size, a block's `size`. A number reaches the
page as a custom property or a single declaration on the element's `style` attribute, put through
`floatformat` so that nothing but a number can be written there. That is the only use of `style`:
anything longer is a class. The reasoning is in
`docs/adr/0003-amounts-are-numbers-written-to-style.md`.
_Avoid_: variant (see below), prop, parameter, setting.

**Variant**:
Not used as a term, and this entry exists to say why. The word reaches for both of the two ideas
above — the tag suffix in `<c-hero.centred>` and the attribute in `size="lg"` — and a sentence
using it for one reads fine to someone assuming the other. Say *layout* when a different block is
meant, and *option* when an attribute is meant.

The one place the word does appear is as an attribute name. `variant` is the option that picks a
theme colour, as in `<c-text.glow variant="accent">`, because that is what daisy-cotton calls it
and this package extends daisy-cotton. In prose it is still an option.

**Blocks stylesheet**:
`daisy_cotton_ext/static/css/daisy-cotton-ext.css`, the one stylesheet this package ships. It
carries the plain Tailwind utilities the blocks use and nothing else. It is built from
`assets/daisy-cotton-ext.css`, and the built file is committed so installing the package needs
no Node toolchain.
_Avoid_: the theme, the framework, the CSS bundle, the supplement (it no longer supplements
anything — it stands alone).

**Host project**:
The Django project that installs this package. It owns daisyUI, the active theme, the base
template and the stylesheet link order. This package never reaches into any of them.
_Avoid_: consumer, client, downstream, user.

**Host contract**:
What a project has to already have for the blocks to render as designed: daisyUI 5 and a theme.
The daisyUI classes the blocks rely on are named in `HOST_PROVIDED_CLASSES` in
`tests/test_stylesheet.py`, which is the contract written down rather than assumed. Using a daisyUI
class not on that list fails the suite.

**Theme**:
A daisyUI theme, supplied and selected by the host project. Blocks are built from the semantic
palette rather than literal colours, which is what makes them follow whatever theme is active.
_Avoid_: skin, palette (the palette is part of a theme, not a synonym for it), style.

**Semantic palette**:
daisyUI's named colour roles: `primary`, `secondary`, `accent`, `neutral`, `base-100`, `base-200`,
`base-300` and their `-content` pairs. The blocks stylesheet declares these as reference-only theme
colours so it can emit gradient stops against them without writing a single custom property.

**Overlap**:
Class selectors defined both by this package's stylesheet and by a host's own build. Expected, and
not measured: two identical rules cost bytes and nothing else. The case that does matter is a host
on a different Tailwind version, where the same class name can carry different declarations and
link order decides which one applies.

**Application chrome**:
Navigation, forms, tables, CRUD pages — anything whose content comes from the application rather
than the template author. Naming the far side of the boundary makes "does this belong here?"
answerable: if it needs a model, a view or a form, it is chrome and it is not ours.

## Terms deliberately not used

**Component library**: accurate but too broad. It describes django-cotton-ui, django-mvp and this
package equally, and the distinction between them is the point. Say *page blocks* or *extended
components*.

**Landing page**: the first target, not the scope. A block is useful on any public-facing page.
Naming the package after one page shape would invite the wrong bug reports.
