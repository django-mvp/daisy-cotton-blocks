# daisy-cotton-blocks

Domain model for daisy-cotton-blocks — a library of page blocks for Django projects running Cotton
and daisyUI.

The terms below are the ones to use in issues, commits, tests and block names. Several of them
exist to keep two neighbouring ideas apart, because the obvious word covers both and the
distinction is the one people get wrong.

## Core concepts

**Block**:
The unit this package ships: a self-contained region of a page, rendered by one Cotton component
and configured entirely through its attributes. A hero is a block. A pricing table is a block.
Content comes from the template author, never from a queryset.
_Avoid_: section (a project's own component library usually has one already, meaning something
else), widget, module, element, panel.

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
_Avoid_: variant (see below), prop, parameter, setting.

**Variant**:
Not used, and this entry exists to say why. The word reaches for both of the two ideas above — the
tag suffix in `<c-hero.centred>` and the attribute in `size="lg"` — and a sentence using it for one
reads fine to someone assuming the other. Say *layout* when a different block is meant, and
*option* when an attribute is meant.

**Blocks stylesheet**:
`daisy_cotton_blocks/static/css/daisy-cotton-blocks.css`, the one stylesheet this package ships. It
carries the plain Tailwind utilities the blocks use and nothing else. It is built from
`assets/daisy-cotton-blocks.css`, and the built file is committed so installing the package needs
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
package equally, and the distinction between them is the point. Say *page blocks*.

**Landing page**: the first target, not the scope. A block is useful on any public-facing page.
Naming the package after one page shape would invite the wrong bug reports.
