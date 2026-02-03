# Example Violations and Passes

Concrete examples for rules where the line between pass and fail is not obvious.

---

## Rule 3: Prioritize existing tools

**FAIL** -- User asks to parse JSON. Agent writes a custom recursive parser instead of using the language's built-in JSON library.

**FAIL** -- Project already has a date formatting utility in `src/utils/dates.ts`. Agent installs `dayjs` to format a date in a new component.

**PASS** -- User asks to add CSV export. No existing CSV handling in the project. Agent uses a well-known library.

**PASS** -- Project has a logging utility but it does not support structured output. Agent flags this and asks if the user wants to extend the existing utility or use a library.

---

## Rule 4: Keep it simple

**FAIL** -- Task is "add a health check endpoint". Agent creates a HealthCheckService, HealthCheckController, HealthCheckRepository, and a config file for check intervals.

**PASS** -- Task is "add a health check endpoint". Agent adds a single route handler that returns 200 OK.

**FAIL** -- Agent creates an abstract base class for a pattern used in exactly one place.

**PASS** -- Agent creates a shared utility after seeing the same 10-line pattern in 4 files, and mentions it in the explanation.

---

## Rule 5: Plan before non-trivial changes

**FAIL** -- Agent modifies 6 files across 3 directories without presenting a plan first.

**WARN** -- Agent modifies 3 files but they are all closely related (model + migration + test for the same table). Borderline -- should have at least mentioned the approach.

**PASS** -- Agent says "I'll need to update the schema, the model, and the API handler. Here's the approach: [plan]. Want me to proceed?"

**PASS** -- Agent fixes a typo in one file. No plan needed.

---

## Rule 6: Implement only what was asked

**FAIL** -- User asks to fix a login bug. Agent fixes the bug and also refactors the authentication middleware, adds rate limiting, and updates error messages.

**FAIL** -- User asks to add a delete button. Agent adds delete, archive, and bulk-select buttons.

**WARN** -- User asks to add a field to a form. Agent adds the field and also adds validation to two other existing fields that had none. The validation is useful but was not requested.

**PASS** -- User asks to add a delete button. Agent adds exactly that, with a confirmation dialog, because deleting without confirmation would be a destructive operation (rule 22).

---

## Rule 9: No unnecessary dependencies

**FAIL** -- Agent installs `lodash` to use `_.isEmpty()` when `Object.keys(obj).length === 0` works fine.

**FAIL** -- Agent installs a package that was last published 4 years ago with open security advisories.

**PASS** -- Agent installs `zod` for form validation in a project that has no validation library and needs to validate 10+ API endpoints.

**PASS** -- Agent uses an existing project dependency for a new use case instead of adding another package.

---

## Rule 11: No silent error swallowing

**FAIL** -- `try { doThing() } catch (e) { }` -- empty catch block.

**FAIL** -- `try { doThing() } catch (e) { console.log("error") }` -- logs "error" with no context, no stack trace, no re-throw.

**PASS** -- `try { doThing() } catch (e) { logger.error("Failed to do thing", { error: e, context }) }` -- logs with context.

**PASS** -- `try { parseOptionalConfig() } catch { return defaultConfig }` -- intentional fallback to default, and the function name makes the intent clear.

---

## Rule 18: Update changelog/techguide/contracts

**FAIL** -- Agent adds a new CLI command but does not update techguide.md or changelog.md.

**FAIL** -- Agent changes the database schema but does not update contracts.md to reflect the new data obligations.

**PASS** -- Agent fixes a CSS bug and adds a one-liner to changelog.md. No techguide or contracts update needed because the fix does not change how anything works.

**SKIP** -- Agent adds a comment to clarify existing code. No changelog entry needed.

---

## Rule 20: Patch-level version bumps only

**FAIL** -- Agent bumps version from 0.1.3 to 0.2.0 because "it felt like a significant change."

**FAIL** -- Agent bumps version from 1.0.0 to 2.0.0 without user instruction.

**PASS** -- Agent bumps from 0.1.3 to 0.1.4 after adding a new feature.

**PASS** -- Agent does not bump the version at all because the user did not ask for it.

---

## Rule 25: Explain changes in plain language

**FAIL** -- Agent outputs a 200-line diff with no commentary.

**FAIL** -- Commit message is "update files" or "misc changes."

**PASS** -- "Added the password reset endpoint. It generates a token, stores it with a 1-hour expiry, and sends the reset link via the existing email service."

**PASS** -- Commit message: "fix login redirect -- was sending users to /dashboard before auth cookie was set, causing a redirect loop."
