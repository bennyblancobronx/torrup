# Scoping Guide -- Ambiguous Rule Interpretation

How to interpret rules that require judgment calls.

---

## "Non-trivial" (Rule 5: Plan before non-trivial changes)

A change is non-trivial if any of these are true:

- Touches 3 or more files
- Adds a new module, class, or component
- Changes public API surface (function signatures, route paths, database schema)
- Involves a dependency addition or removal
- Affects authentication, authorization, or payment logic
- Requires coordinated changes across layers (frontend + backend, schema + model + API)

A change is trivial if all of these are true:

- Touches 1-2 files
- The fix or addition is obvious and localized
- No API surface changes
- No new dependencies
- A one-line description fully captures what needs to happen

When in doubt, it is non-trivial.

---

## "Over-engineering" (Rule 4: Keep it simple)

Signs of over-engineering:

- Abstractions with only one implementation (interfaces wrapping a single class)
- Configuration for things that will never change
- "Future-proofing" for requirements nobody asked for
- Helper utilities used exactly once
- Generic solutions when a specific one would work
- Multi-layer indirection that adds no value (service -> manager -> handler -> executor when one function would do)
- Feature flags for features that are not optional

Not over-engineering:

- Error handling at system boundaries
- Input validation on user-facing endpoints
- Splitting a 500-line file into modules
- Using an existing abstraction from the codebase
- A config file for values that differ between environments

---

## "Implement only what was asked" (Rule 6)

Violations:

- Adding a feature the user did not request
- Refactoring adjacent code that was not part of the task
- Adding type annotations to files you did not otherwise change
- Creating utility functions "while you're in there"
- Upgrading dependencies not related to the task
- Adding comments or docstrings to unchanged code

Not violations:

- Fixing a bug you introduced with your change
- Updating imports when you move/rename something
- Adjusting a test that breaks because of your change
- Formatting code you actually modified (if the project uses a formatter)

When something adjacent looks wrong, the correct action is to flag it to the user, not fix it.

---

## "Test after every change" (Rule 15)

What counts as testing:

- Running the existing test suite and confirming it passes
- Manual verification that the change works as expected
- Running a linter or type checker if the project uses one
- For UI changes: loading the page and confirming it renders correctly

What does not count:

- Assuming it works because it looks right
- Only testing the new code but not checking for regressions
- Skipping tests because "it's just a small change"

For changes that cannot be tested (documentation, comments): this rule does not apply.

---

## "Revert when stuck" (Rule 16)

Indicators of being stuck:

- Third attempt at fixing the same error
- Fix for fix-A broke thing-B, fix for thing-B broke thing-C
- The diff has grown significantly beyond the original task scope
- You are adding workarounds for workarounds

The correct action is to suggest reverting to the last known working state, not to keep patching.

---

## "Destructive operations" (Rule 22)

Always require explicit confirmation:

- DROP TABLE, DELETE FROM (without WHERE or with broad WHERE)
- git reset --hard, git push --force, git clean -f
- rm -rf on directories
- Database migrations that drop columns or tables
- Overwriting production config files
- Revoking access tokens or API keys

Do not require confirmation:

- git add, git commit, git push (normal push)
- CREATE TABLE, ALTER TABLE ADD COLUMN
- File writes to new files
- Running tests
