# ADR 0007 — Built from daisy-cotton's components

**Status:** accepted

## Decision

daisy-cotton is a dependency of this package. Where a component here needs something daisy-cotton
already renders, it uses that component and does not write the markup again. The first case is the
portrait in `<c-quote.byline>`, which is `<c-avatar>`.

The rules that follow:

1. **Check daisy-cotton before writing markup.** If it has a component for the thing, use it.
   A component that maps one-to-one onto a daisyUI component belongs there, and one that is
   missing is added there, not here.
2. **Call it with `only`.** Cotton hands a component's own attributes down to the components
   inside it. Without `only`, a `class` meant for the quote lands on the avatar as well.
3. **Use the attributes daisy-cotton documents, and as few as will do.** A host may have another
   component of the same name ahead of daisy-cotton's in `INSTALLED_APPS`, and Django renders the
   first it finds. django-mvp's own avatar is one. The fewer attributes passed, the more of those
   it works with. The byline passes `src` and an empty `alt`, and takes the stock size.
4. **A colour option is named `variant`,** as it is on every daisy-cotton component.

## Why

The package describes itself as what is built on top of daisy-cotton's components, and until now
it depended only on Cotton and reached daisyUI's classes directly. That held while every block was
layout around a host's own content. A quote needs an avatar, and a second copy of the avatar's
markup would drift from the first: its sizing, its placeholder, its presence indicator.

Leaving the base components to the host was the alternative. A host without daisy-cotton would
then render `<c-avatar>` as a missing template, which is an error on the page and not a styling
gap.

## Consequences

- Installing this package installs daisy-cotton, and `daisy_cotton` goes in `INSTALLED_APPS`.
- A host that already has a component of the same name keeps its own, by app order.
- The classes a daisy-cotton component emits are the host's to build, as daisyUI's are. This
  package's stylesheet carries only what its own templates use
  ([ADR 0002](0002-stylesheet-carries-what-a-host-cannot.md)).
