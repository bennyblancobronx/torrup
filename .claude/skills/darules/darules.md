# The Rules v0.1.3

## Session Startup

1. Always read about.md first, then contracts.md second, before doing any work
2. Always read and understand existing code before modifying it. Never edit a file you have not opened in this session

## Planning and Scope

3. Prioritize existing tools, scripts, and architecture before building something new
4. Keep it simple: one script, one command, one job. Fewer moving parts means fewer things break. Do not over-engineer
5. Present a plan before writing code. On non-trivial changes, outline the approach starting with the simplest option and get confirmation first
6. Implement exactly what was asked. Do not add extra features, refactor adjacent code, or introduce abstractions unless the user requests it. If something nearby looks wrong, flag it -- do not fix it
7. When working on UI, ask for screenshots or mockups if the expected result is unclear

## Implementation Constraints

8. Keep files under 400 lines. If a file grows past that, split it into modules -- one file, one job
9. Do not add new dependencies without confirming they exist, are maintained, and are actually needed. Prefer built-in or existing solutions first
10. Never hardcode secrets, API keys, or credentials. Never commit .env files or similar. If secrets are needed, ask the user how to handle them
11. Do not silently swallow errors or add catch-all error handling that hides problems. Errors should be visible and debuggable
12. Never modify user credentials or authentication data in the database without explicit instruction. Ask the user for credentials if login fails during testing
13. Never save working files, tests, or documentation to the project root. Use appropriate subdirectories

## Testing and Recovery

14. Break work into small testable steps. Implement one thing, verify it works, then move on
15. Test after every change. Verify the code runs and does not break existing functionality before moving on
16. When stuck or looping on a fix, suggest reverting to the last working state instead of piling on more patches

## Documentation and Versioning

17. Before making changes that affect project scope, architecture, or external integrations, re-read contracts.md and techguide.md to understand current state
18. After making any change, update whichever applies: changelog.md for what changed (this is the source of truth for version number), techguide.md for how it works (core logic, CLI commands, descriptions), contracts.md for any shifted obligations or integration points
19. Each custom app or script tracks its own version number separately from the project
20. Only update version numbers at the 0.1.X patch level. Major and minor bumps are user-only decisions

## Commits and Destructive Operations

21. Commit after each working change with a plain-language message
22. Never run destructive operations (drop tables, delete production data, force-push) without explicit confirmation

## Style and Tone

23. No emojis ever
24. Do not mention AI, Claude, or any AI tooling in any note, changelog, commit, or output
25. Explain what changes do and why in plain language. Do not just dump code without context
