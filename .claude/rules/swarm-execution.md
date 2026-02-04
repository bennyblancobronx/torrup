# Claude Flow V3 - Swarm Execution Rules

## Auto-Start Swarm Protocol

When user requests complex work, spawn agents in background and WAIT:

```javascript
// STEP 1: Initialize swarm (anti-drift config)
Bash("npx @claude-flow/cli@latest swarm init --topology hierarchical --max-agents 8 --strategy specialized")

// STEP 2: Spawn ALL agents in ONE message with run_in_background: true
Task({ prompt: "...", subagent_type: "researcher", run_in_background: true })
Task({ prompt: "...", subagent_type: "coder", run_in_background: true })
// etc.

// STEP 3: STOP and tell user what's happening
```

## Spawn and Wait Pattern

After spawning background agents:
1. TELL USER what agents are doing
2. STOP - no more tool calls
3. WAIT - let agents complete
4. SYNTHESIZE when results arrive

## DO NOT
- Continuously check swarm status
- Poll TaskOutput repeatedly
- Add more tool calls after spawning
- Ask "should I check on the agents?"

## DO
- Spawn all agents in ONE message
- Tell user what's happening
- Wait for agent results
- Synthesize results when they return

## Task Complexity Detection

AUTO-INVOKE SWARM when task involves:
- Multiple files (3+)
- New feature implementation
- Refactoring across modules
- API changes with tests
- Security-related changes

SKIP SWARM for:
- Single file edits
- Simple bug fixes (1-2 lines)
- Documentation updates
- Configuration changes

## Agent Routing

| Task | Agents |
|------|--------|
| Bug Fix | coordinator, researcher, coder, tester |
| Feature | coordinator, architect, coder, tester, reviewer |
| Refactor | coordinator, architect, coder, reviewer |
| Performance | coordinator, perf-engineer, coder |
| Security | coordinator, security-architect, auditor |

## Golden Rule

1 MESSAGE = ALL RELATED OPERATIONS

- Task tool: Spawn ALL agents in ONE message
- File operations: Batch ALL reads/writes/edits
- Bash commands: Batch ALL terminal operations

## CLI Coordination

Claude Code handles execution. CLI handles coordination:

```bash
# Swarm init
npx @claude-flow/cli@latest swarm init --topology hierarchical

# Memory
npx @claude-flow/cli@latest memory store --key "x" --value "y" --namespace patterns
npx @claude-flow/cli@latest memory search --query "search terms"

# Hooks
npx @claude-flow/cli@latest hooks pre-task --description "[task]"
npx @claude-flow/cli@latest hooks post-task --task-id "[id]" --success true
```
