# django-mvp-bits

Domain model for django-mvp-bits — a library of page blocks for projects built on django-mvp.

The terms below are the ones to use in issues, commits, tests and component names. Several of them
exist specifically to keep this package's language distinct from django-mvp's, because the two
libraries sit next to each other and the obvious words are already taken.

## Core concepts

**Block**:
The unit this package ships: a self-contained, configurable region of a page, rendered by one
Cotton component and configured entirely through its attributes. A hero is a block. A pricing
table is a block. Content comes from the template author, never from a queryset.
_Avoid_: section (django-mvp already has `<c-section>`, which is something else), widget, module,
element, panel.

**Page block namespace**:
The `mvp-bits` prefix every component tag carries — `<c-mvp-bits.hero>`. Cotton maps hyphens in a
tag onto underscores on disk, so these resolve to `mvp_bits/templates/cotton/mvp_bits/`. The
namespace is not cosmetic: without it, a component here would shadow or be shadowed by one of
django-mvp's depending on `INSTALLED_APPS` order.

**Supplement**:
`mvp_bits/static/css/mvp-bits.css`, the stylesheet this package ships. Named for what it does: it
adds to django-mvp's stylesheet and restates none of it. Loaded second, and useless alone.
_Avoid_: our stylesheet, the theme, the framework, the CSS bundle.

**Whitelist**:
The hand-written `@source inline(...)` list in `assets/mvp-bits.css` naming every class the
supplement is allowed to emit. Nothing is discovered by scanning templates. django-mvp calls its
equivalent a *safelist*, and it works differently — django-mvp scans its own templates as well,
where this package scans nothing.
_Avoid_: safelist (means django-mvp's, which is a different thing), allowlist, class list.

**Overlap**:
The set of class selectors defined by both stylesheets. The contract is that it is empty, and
`tests/test_stylesheet.py` measures it rather than assuming it. "Zero overlap" is the whole
design constraint in two words.

**Host project**:
The Django project that installs this package. It owns the theme, the base template and the
stylesheet link order. This package never reaches into any of them.
_Avoid_: consumer, client, downstream, user.

**Theme**:
A daisyUI theme, supplied by django-mvp and selected by the host project. Blocks are built from
the semantic palette (`primary`, `base-100`, …) rather than literal colours, which is what makes
them follow whatever theme is active.
_Avoid_: skin, palette (the palette is part of a theme, not a synonym for it), style.

**Application chrome**:
What django-mvp owns — navigation, forms, tables, CRUD pages, anything whose content comes from
the application. Naming the far side of the boundary makes "does this belong here?" answerable:
if it needs a model, a view or a form, it is chrome and it belongs upstream.

**Semantic palette**:
daisyUI's named colour roles: `primary`, `secondary`, `accent`, `neutral`, `base-100`, `base-200`,
`base-300` and their `-content` pairs. The supplement declares these as reference-only theme
colours so it can emit gradient stops against them without writing a single custom property.

## Terms deliberately not used

**Component library**: accurate but too broad — it describes django-mvp, django-cotton-ui and this
package equally, and the distinction between them is the point. Say *page blocks*.

**Landing page**: the first target, not the scope. A block is useful on any public-facing page.
Naming the package after one page shape would invite the wrong bug reports.
