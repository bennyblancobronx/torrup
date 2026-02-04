# Project Rules

1. Always read about.md first
2. Always read contracts.md second
3. Prioritize pre-existing architecture/scripts BEFORE custom solutions
4. Keep it simple: one script, one command, one job
5. Present a plan before writing code on non-trivial changes
6. Default to the least complex solution that works
7. Break work into small testable steps
8. After changes update changelog.md with TL;DR
9. Custom apps/scripts get independent version numbers
10. techguide.md is the manual for core logic and CLI commands
11. Be humble - no AI attribution in notes/commits
12. NO EMOJIS EVER
13. Only update version at 0.1.X level - user controls major/minor
14. Do not add extra features without consulting user
15. Keep it simple as possible
16. NEVER change user passwords - ask for credentials if needed
17. Keep files under 400 lines - split into modules if larger
18. Test after every change before moving on
19. When stuck, suggest reverting to last working state
20. Ask for screenshots/mockups if UI result is unclear
21. Explain changes in plain language
22. Never save working files/tests to project root
23. Commit after each working change with plain-language message
24. Never run destructive operations without explicit confirmation
25. Read and understand existing code before modifying
26. Verify dependencies exist before adding them
27. Do not refactor code outside the current task
28. Never hardcode secrets or commit .env files
29. Do not silently swallow errors
30. Implement exactly what was asked - no extras

## File Organization

NEVER save to root folder. Use:
- /src - Source code
- /tests - Test files
- /docs - Documentation
- /config - Configuration
- /scripts - Utility scripts
