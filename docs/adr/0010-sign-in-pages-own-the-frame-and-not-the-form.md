# ADR 0010 — Sign-in pages own the frame and not the form

**Status:** accepted

## Decision

A sign-in or sign-up block renders the layout of the page and nothing an application has to
supply. The logo, the form, the buttons for third-party providers and the link to the other page
are slots. No block renders a field, a label, an error or a submit button.

The rules that follow:

1. **The same slot names in every block:** `logo`, the default slot for the form, `providers`,
   `footer` and `background`. A layout with something more adds a slot for it and keeps these.
2. **The logo is a slot and never an attribute,** and it is rendered once, somewhere that survives
   every width. A layout that drops a pane on a narrow screen keeps the logo out of that pane.
3. **A block draws what sits between the slots,** and only when both sides are there: the word
   between the provider buttons and the form is left out when either is missing.
4. **A block does not open itself.** `<c-sign-in.providers>` folds the form behind a disclosure
   and takes `open` from the page, because whether the form came back with errors is something
   only the application knows.
5. **What most of them share is one component.** `<c-auth.panel>` holds the heading, the provider
   buttons, the divider, the form and the foot. A layout whose form area is a different shape
   writes its own.

## Why

Article X keeps forms out of this package, and a sign-in page is mostly a form. The form's fields,
validation, redirect target and token all belong to whatever handles authentication. In a Django
project that is usually django-allauth, which already hands a template the form, the list of
providers and the addresses to link to. A block that rendered fields would have to guess at all of
that and would be wrong for the next project.

What is left once the form is taken out is still most of the work of the page: where the logo
goes, how the form sits beside what the page has to say for itself, what happens on a narrow
screen, and keeping one heading. That is layout, and it is the same in every project.

The alternative was to leave these pages out as application chrome. They sit in front of the
application and not inside it, and they are the pages a visitor sees before any other, which is
the ground this package exists to cover.

## Consequences

- A page is put together in the project's own template: a block, with the project's form in it.
- The demo's forms are stand-ins built from the base field and button components. They show a
  default state and an error state so the layouts can be judged with both.
- Pages of the same kind that have no block here, such as a password reset or a code to confirm,
  use `<c-auth.panel>` inside a layout of the project's own.
