# Feature Specification: Stat components

**Feature Branch**: `001-stat-components`

**Created**: 2026-10-06

**Status**: Draft

**Serves**: G1, G5, G6 · **Roadmap**: R7 (the statistics part)

**Input**: Components for showing figures, for anyone building a dashboard or a landing page with this package. They build on daisy-cotton's stat, come in several layouts, work with or without an icon, and draw no charts of their own.

## Summary

daisy-cotton's stat shows a title, a number and a line of description. This feature adds what a developer usually wants next:

- a stat that says how its figure has moved, and whether that move is welcome
- six arrangements of that stat, all taking the same attributes
- a stat with a bar showing progress towards a target or a limit
- a stat whose number counts up when the visitor reaches it
- the badge that states a move, usable by itself
- three page sections that set figures out on a landing page

Every stat takes an optional icon. None of them draws a chart. A developer who wants one beside a figure puts their own chart into the room a trend stat leaves for it.

A prototype of all of this was built and reviewed before this specification was written. The specification describes what was agreed there.

## Clarifications

### Session 2026-10-06

- Q: Does the package draw a small chart, such as a sparkline, inside a stat? → A: No. Nothing in this package looks like a chart. A trend stat leaves room for one that the developer supplies.
- Q: What is the attribute that picks a theme colour called? → A: `variant`, the name daisy-cotton uses on every component.
- Q: How is an icon named? → A: By whatever name the project's own icon component understands. The stat hands the name on and resolves nothing itself.
- Q: Which trend layouts accept a picture in place of the icon, and which leave room for a chart? → A: Stacked, inline, centred and footer accept a picture. Corner and row take a small icon only. Stacked, inline, corner and footer leave room for a chart. Centred and row do not.
- Q: What does the counting stat do inside a daisyUI `stats` row, where the browser cannot tell that the visitor has reached it? → A: It counts once, when the page loads, and ends on the true number. This is documented as a limit and is not prevented.
- Q: What numbers can the counting stat count to? → A: Whole numbers, written without separators. Anything else a figure needs, such as a currency sign, a unit or decimals, is supplied as text before or after the number.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A developer shows how a figure has moved (Priority: P1)

A developer building a dashboard has a figure and knows how it compares with last month. They render a trend stat with the figure, the size of the change, the direction it moved and what it is measured against. Where a fall is the good news, as with a lead time or a failure count, they say so, and the stat marks the move as welcome.

The same badge is available alone, for a table cell or a heading.

**Why this priority**: This is the most common thing a developer wants from a stat that the base component does not do, and every layout in story 2 is built from it.

**Independent Test**: Render a trend stat with each direction, with and without the "a fall is good" setting, and read the move and its meaning from the output without looking at colour.

**Acceptance Scenarios**:

1. **Given** a figure, a change and a direction, **When** the trend stat is rendered, **Then** the output contains the figure, the change and what it is measured against, and states the direction in words that assistive technology reads out.
2. **Given** a rise, **When** the stat is rendered with no further setting, **Then** the move is marked as welcome. **Given** a fall, **Then** it is marked as unwelcome.
3. **Given** the developer has said a fall is the good news, **When** the stat is rendered with a fall, **Then** the move is marked as welcome, and a rise is marked as unwelcome.
4. **Given** a direction of no change, **When** the stat is rendered, **Then** the move is marked as neither welcome nor unwelcome.
5. **Given** no change is supplied, **When** the stat is rendered, **Then** no badge and no direction appear.
6. **Given** a title, figure, change or description containing markup characters, **When** the stat is rendered, **Then** they appear as text and are not interpreted.
7. **Given** a change and a direction and nothing else, **When** the change badge is rendered alone, **Then** it states the same move in the same way as it does inside a stat.

---

### User Story 2 - A developer chooses how a trend stat is arranged (Priority: P1)

A developer wants the stats on a page to suit where they sit: a row along the top of a dashboard, a panel standing alone, a short list down the side. They pick one of six arrangements of the trend stat. Each is a component of its own and all six take the same attributes, so trying another arrangement means changing the tag and nothing else.

The six are: stacked, inline, corner, centred, footer and row.

**Why this priority**: Layout variety is the reason to offer these beyond the base stat, and it is what goal G5 asks of every family.

**Independent Test**: Render the same figure through all six components with identical attributes and confirm each shows the same content.

**Acceptance Scenarios**:

1. **Given** one set of attributes, **When** it is passed to each of the six trend layouts, **Then** each renders the title, the figure, the change with its direction, and the description.
2. **Given** any of the six, **When** it is rendered, **Then** the output is a daisy-cotton stat that can sit in a stat group beside plain stats.
3. **Given** any of the six, **When** a part is left out (title, change or description), **Then** the rest renders and nothing is left where the missing part would be.
4. **Given** any of the six, **When** extra attributes such as an id are passed, **Then** they reach the stat's outer element.

---

### User Story 3 - A developer puts an icon or a picture beside a figure (Priority: P2)

A developer wants each figure on a dashboard to carry an icon. They pass the icon's name, and the stat shows it using the icon component the project already has. Leaving the name out gives a stat with no icon and no gap where one would be. Where the thing beside the figure is a picture or a logo, they supply that in place of the icon.

**Why this priority**: Developers commonly want icons with stats, and every stat in this feature has to work both ways.

**Independent Test**: Render each stat component with an icon name, without one, and with a picture, and compare the three outputs.

**Acceptance Scenarios**:

1. **Given** an icon name, **When** any stat component in this feature is rendered, **Then** the project's icon component is rendered with that name, and the icon is hidden from assistive technology.
2. **Given** no icon name and no picture, **When** any stat component is rendered, **Then** the output has no icon and no empty element for one.
3. **Given** a picture supplied in place of the icon, **When** a layout that accepts one is rendered, **Then** the picture is rendered and the icon component is not.

---

### User Story 4 - A developer shows progress towards a target or a limit (Priority: P2)

A developer has a figure and a percentage: money raised against a goal, storage used against an allowance. They render a progress stat, which shows the figure, a bar and the percentage written out. They pick the bar's colour by variant, so a limit being approached can be shown as a warning.

**Why this priority**: It is the second most common extension of a stat and is independent of the trend stat.

**Independent Test**: Render the progress stat at several percentages and read the bar's value, its accessible name and the written percentage from the output.

**Acceptance Scenarios**:

1. **Given** a figure, a title and a percentage, **When** the progress stat is rendered, **Then** the output contains a progress bar whose value is that percentage out of 100, named for assistive technology by the title, and the percentage written as text.
2. **Given** a percentage over 100, **When** the stat is rendered, **Then** the bar is full and the written percentage is the number given.
3. **Given** a percentage that is not a number, **When** the stat is rendered, **Then** the bar's value is 0 and nothing but a number reaches the bar.
4. **Given** a variant, **When** the stat is rendered, **Then** the bar carries that variant. **Given** none, **Then** it carries the primary variant.

---

### User Story 5 - A developer leaves room for their own chart (Priority: P2)

A developer using django-mvp-charts, or any charting library, wants a small chart of the run behind a figure. They put the chart between the trend stat's tags and it is placed with the figure. This package supplies the room and nothing else.

**Why this priority**: It keeps charting out of this package while still letting a stat carry one.

**Independent Test**: Render a trend stat with content between its tags and without, and compare.

**Acceptance Scenarios**:

1. **Given** content between the tags of a trend layout that leaves room for a chart, **When** it is rendered, **Then** that content appears inside the stat.
2. **Given** nothing between the tags, or only whitespace, **When** it is rendered, **Then** no element is rendered for the chart.

---

### User Story 6 - A developer has a figure count up as the visitor reaches it (Priority: P3)

A developer building a landing page wants the headline numbers to count up from nothing as the visitor scrolls to them. They render a counting stat with the number to count to, any text to put before or after it, and how long the count should take. Visitors who have asked for reduced motion, and browsers that cannot do it, see the finished number.

**Why this priority**: It is a landing-page flourish. It serves G6 and nothing depends on it.

**Independent Test**: Render the counting stat and confirm the finished number is present as text. In a browser, scroll to it and observe the count start from nothing and end on the number given.

**Acceptance Scenarios**:

1. **Given** a number to count to, **When** the counting stat is rendered, **Then** the finished number is present in the output as text that assistive technology reads, and the counting figure is hidden from it.
2. **Given** text to put before and after the number, **When** the stat is rendered, **Then** both appear with the number.
3. **Given** a number that is not whole, **When** the stat is rendered, **Then** it counts to the nearest whole number. **Given** something that is not a number, **Then** it counts to 0.
4. **Given** a browser that supports it and a visitor with no reduced-motion preference, **When** the stat scrolls into view, **Then** the figure counts from 0 to the number in the time given, and never comes to rest on any other value.
5. **Given** a visitor who has asked for reduced motion, **When** the page loads, **Then** the finished number is shown and nothing moves.

---

### User Story 7 - A developer sets figures out as a section of a page (Priority: P3)

A developer building a landing page wants a section for the product's numbers. They choose from three: a band with the figures in one row under an optional heading, a split with the case in words on one side and the figures on panels on the other, and a headline built round one very large figure. The band and the split take any stat as their figures.

**Why this priority**: These are the statistics blocks the roadmap lists under social proof. They are built from the stats in the earlier stories.

**Independent Test**: Render each section with and without its optional parts and with different numbers of figures.

**Acceptance Scenarios**:

1. **Given** a band with a heading, a supporting sentence and figures, **When** it is rendered, **Then** the heading is rendered at the level asked for and the figures appear after it.
2. **Given** a band with figures and no heading, **When** it is rendered, **Then** no heading element and no empty heading area is rendered.
3. **Given** a band with a background supplied, **When** it is rendered, **Then** the background is rendered behind the figures and hidden from assistive technology.
4. **Given** a band asked to bring its figures in one after another, **When** it is rendered, **Then** the figures are wrapped by the package's cascade reveal. **Given** no such request, **Then** nothing about the band moves.
5. **Given** a split with a heading, a sentence, actions and figures, **When** it is rendered, **Then** the copy and its actions come before the figures in the output.
6. **Given** a headline with a figure and a title, **When** it is rendered, **Then** the two together form one heading at the level asked for.
7. **Given** a headline with no speed set, **When** it is rendered, **Then** the figure's colours do not move.

---

### Edge Cases

- A figure of 0 is rendered as 0 in every stat and is not treated as missing.
- A very long title or description wraps inside its stat. A very long figure does not make the page scroll sideways.
- A stat rendered with nothing but a figure renders that figure alone.
- A counting stat placed in a daisyUI `stats` row counts once as the page loads. The documentation says so and points to the band or a plain grid for a count that waits.
- A band with a single figure, and a band with more figures than fit comfortably, both render every figure.
- A split with an odd number of figures renders every figure.
- A headline whose figure is too long for one line wraps it.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The package MUST provide a trend stat that shows a title, a figure, the size of a change, its direction and what it is measured against. *(US1)*
- **FR-002**: A trend stat MUST state the direction of the move in words available to assistive technology, so the move is never carried by colour alone. *(US1)*
- **FR-003**: A trend stat MUST let the developer say that a fall is the good news, and MUST mark the move as welcome, unwelcome or neither accordingly. *(US1)*
- **FR-004**: The package MUST provide the change badge as a component usable outside a stat. *(US1)*
- **FR-005**: The package MUST provide six layouts of the trend stat (stacked, inline, corner, centred, footer, row), each a separate component, all accepting the same attributes. *(US2)*
- **FR-006**: Every single-figure stat in this feature MUST render as a daisy-cotton stat, so it can be placed in a stat group beside plain stats, and MUST pass extra attributes to its outer element. *(US2)*
- **FR-007**: Every stat component in this feature MUST accept an optional icon by name, render it through the project's icon component, hide it from assistive technology, and render nothing for it when no name is given. *(US3)*
- **FR-008**: The stacked, inline, centred and footer trend layouts, the progress stat and the counting stat MUST accept a picture in place of the icon. *(US3)*
- **FR-009**: The package MUST provide a progress stat with a real progress bar, named by the stat's title, whose value is a percentage out of 100, with the percentage also written as text. *(US4)*
- **FR-010**: The progress stat MUST accept a `variant` for the bar's colour and MUST let nothing but a number reach the bar's value. *(US4)*
- **FR-011**: The stacked, inline, corner and footer trend layouts MUST place whatever the developer puts between their tags inside the stat, and MUST render nothing for it when it is empty. *(US5)*
- **FR-012**: The package MUST NOT draw a chart or anything resembling one. *(US5)*
- **FR-013**: The package MUST provide a counting stat that counts from 0 to a given whole number when it comes into view, over a time the developer sets, with optional text before and after the number. *(US6)*
- **FR-014**: The counting stat MUST always give assistive technology the finished number, MUST show the finished number without movement to visitors who prefer reduced motion and in browsers that cannot count, and MUST never rest on a number other than the one given. *(US6)*
- **FR-015**: The package MUST provide a band section that sets figures out under an optional heading, accepts a background, can be inverted for a dark surface, and can bring its figures in one after another on request. *(US7)*
- **FR-016**: The package MUST provide a split section with copy and actions on one side and figures on the other, with the copy first in reading order. *(US7)*
- **FR-017**: The package MUST provide a headline section built round one large figure, with an optional title, supporting sentence, icon or picture, and actions. *(US7)*
- **FR-018**: Nothing in this feature may move unless the developer asks for it, except the counting stat, whose purpose is to move. *(US6, US7)*
- **FR-019**: Every component in this feature MUST take its colours from the project's active theme. *(US1, US4, US7)*
- **FR-020**: Every component in this feature MUST have a page in the example project showing it with and without an icon and in its edge cases, and MUST carry its own attribute and slot reference. *(US1–US7)*
- **FR-021**: The words the package itself supplies, which are the spoken directions of a move, MUST be translatable. *(US1)*

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A developer can change a trend stat from one layout to any other by editing the tag alone, with no attribute changes, for all six layouts.
- **SC-002**: Every stat component in the feature renders correctly both with and without an icon.
- **SC-003**: With colour removed, a reader can still tell from every trend stat which way the figure moved.
- **SC-004**: A screen reader user is given the direction of every move, the name of every progress bar and the finished number of every counting stat.
- **SC-005**: No page in the example project scrolls sideways at phone, tablet or desktop width, including with very long titles and figures.
- **SC-006**: A project that adopts these components gains no script and no chart.
- **SC-007**: A developer can assemble a statistics section for a landing page from this package without writing layout markup of their own.

## Assumptions

- daisy-cotton is already a dependency of this package and supplies the stat, stat group, badge, progress and icon components these are built from.
- The project supplies daisyUI 5 and its theme, as for every other component in the package.
- The developer formats figures before passing them. These components do no arithmetic and no number formatting, apart from rounding the number a counting stat counts to.
- Counting on scroll relies on browser features that not every browser has. Where they are missing, the finished number is shown, which is an acceptable result and not a fault.
- Layout, spacing, colour and wording were settled by eye on the prototype and are not requirements here.
- Sections for testimonials, logos and people, which the roadmap groups with statistics under R7, are separate features.
