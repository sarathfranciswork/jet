# Claude Conversation Log

Session ID: agent-ac1dd45d6e0585bf8
Date: 2026-03-02 23:10:33

---

## 👤 User

I need to understand Claude Code hooks in detail. Specifically:
1. What types of hooks are available in Claude Code? (pre-tool, post-tool, etc.)
2. How do you configure hooks in settings.json or .claude/settings.json?
3. Can hooks run shell commands automatically after certain tool calls (like after writing/editing files)?
4. What's the exact syntax and configuration format for hooks?
5. Can hooks be configured per-project (in .claude/ directory)?
6. Are there hooks that trigger after code changes to automatically run tests?

I want to set up a hook that automatically runs Flutter golden tests or visual validation after code is written/edited during development. What's the best way to achieve this?

---

## 🤖 Claude

I'll fetch the Claude Code documentation to give you detailed information about hooks and how to set them up for your Flutter golden tests use case.

---

## 🤖 Claude

Perfect! Now let me fetch the hooks documentation to give you detailed information.

---

## 🤖 Claude

Excellent! Now I have the complete hooks documentation. Let me provide you with a comprehensive answer to all your questions.

## Claude Code Hooks: Complete Guide

Based on the official documentation, here's everything you need to know about hooks in Claude Code:

### 1. Types of Hooks Available

Claude Code supports **4 hook types**, not just command hooks:

- **`type: "command"`** - Run shell commands (most common)
- **`type: "http"`** - POST event data to HTTP endpoints
- **`type: "prompt"`** - Single-turn LLM evaluation (Claude model makes yes/no decisions)
- **`type: "agent"`** - Multi-turn verification with tool access (spawns subagent)

Additionally, hooks fire at **16 different lifecycle events**:

| Event | Fires When |
|-------|-----------|
| `SessionStart` | Session begins or resumes |
| `UserPromptSubmit` | Before Claude processes your prompt |
| `PreToolUse` | Before any tool call executes (can block) |
| `PermissionRequest` | Permission dialog appears |
| `PostToolUse` | After a tool succeeds |
| `PostToolUseFailure` | After a tool fails |
| `Notification` | Claude needs your attention |
| `SubagentStart` | Subagent is spawned |
| `SubagentStop` | Subagent finishes |
| `Stop` | Claude finishes responding |
| `TeammateIdle` | Agent team teammate about to go idle |
| `TaskCompleted` | Task marked complete |
| `ConfigChange` | Configuration file changes |
| `WorktreeCreate` | Worktree being created |
| `WorktreeRemove` | Worktree being removed |
| `PreCompact` | Before context compaction |
| `SessionEnd` | Session terminates |

### 2. Configuration Format (settings.json)

Hooks are configured using this JSON structure in either:
- `~/.claude/settings.json` (global, all projects)
- `.claude/settings.json` (project-specific)
- `.claude/settings.local.json` (project-specific, gitignored)
- Or through the `/hooks` interactive menu

**Basic syntax:**

```json
{
  "hooks": {
    "EVENT_NAME": [
      {
        "matcher": "PATTERN_OR_EMPTY",
        "hooks": [
          {
            "type": "command",
            "command": "shell command here"
          }
        ]
      }
    ]
  }
}
```

**Key fields:**
- `EVENT_NAME`: The lifecycle event (e.g., `PostToolUse`, `PreToolUse`)
- `matcher`: Regex pattern to filter. For `PostToolUse`/`PreToolUse`: matches tool name (e.g., `"Edit|Write"`, `"Bash"`)
- `type`: Hook type (command, http, prompt, agent)
- `command`: Shell command to execute

### 3. Running Commands After File Edits

Yes! Use the `PostToolUse` event with `Edit|Write` matcher:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

This automatically runs Prettier after every file write/edit. For Flutter golden tests, you'd use a similar pattern:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs -I {} sh -c 'if [[ {} == *.dart ]]; then flutter test {} --update-goldens; fi'"
          }
        ]
      }
    ]
  }
}
```

### 4. Exact Hook Syntax and Details

**Command hooks receive JSON input on stdin:**

```json
{
  "session_id": "abc123",
  "cwd": "/your/project",
  "hook_event_name": "PostToolUse",
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/file.dart",
    "new_contents": "..."
  }
}
```

**Exit codes determine behavior:**
- `exit 0`: Allow the action to proceed
- `exit 2`: Block the action (write reason to stderr)
- `exit 0 + JSON`: Structured control (see output format below)

**For file editing hooks, extract the path with `jq`:**

```bash
echo "$INPUT" | jq -r '.tool_input.file_path'
```

**Return structured JSON for advanced control:**

```bash
cat << 'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Use flutter test instead"
  }
}
EOF
exit 0
```

### 5. Per-Project Hook Configuration

**Yes! Full support for project-level hooks:**

Store hooks in `.claude/settings.json` at your project root:

```json
// .claude/settings.json (in Git repo)
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "/absolute/path/to/.claude/hooks/run-tests.sh"
          }
        ]
      }
    ]
  }
}
```

Place hook scripts in `.claude/hooks/`:

```bash
#!/bin/bash
# .claude/hooks/run-tests.sh
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')

# Make it executable: chmod +x .claude/hooks/run-tests.sh
if [[ "$FILE_PATH" == *.dart ]]; then
  flutter test "$FILE_PATH" --update-goldens
fi
```

**Configuration scope hierarchy** (highest to lowest priority):
1. `.claude/settings.local.json` (project-specific, gitignored)
2. `.claude/settings.json` (project-specific, shareable)
3. `~/.claude/settings.json` (user global)
4. Managed policy settings (organization-wide)

### 6. Hooks After Code Changes for Automated Testing

**Yes! Use async hooks for background test execution:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "./.claude/hooks/run-tests.sh",
            "async": true
          }
        ]
      }
    ]
  }
}
```

The `"async": true` flag makes the hook run in the background without blocking Claude's response.

---

## Your Flutter Golden Tests Use Case

Here's the recommended setup:

**File: `.claude/settings.json`**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/flutter-golden-tests.sh",
            "async": true
          }
        ]
      }
    ]
  }
}
```

**File: `.claude/hooks/flutter-golden-tests.sh`**

```bash
#!/bin/bash
set -e

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only run for Dart test files or widget files
if [[ "$FILE_PATH" == *"_test.dart" ]] || [[ "$FILE_PATH" == *"test/"*.dart ]]; then
  echo "[Flutter] Running golden tests for: $FILE_PATH" >&2
  
  cd "$CLAUDE_PROJECT_DIR"
  
  # Run golden tests with update flag if needed
  if flutter test "$FILE_PATH" --update-goldens 2>&1 | tee -a /tmp/flutter-test.log; then
    echo "[Flutter] Golden tests passed ✓" >&2
  else
    echo "[Flutter] Golden tests failed - review changes" >&2
  fi
fi

exit 0
```

**Make it executable:**

```bash
chmod +x .claude/hooks/flutter-golden-tests.sh
```

**Enable the hook through the menu** (or edit the JSON above):

```
/hooks → PostToolUse → + Add new hook → Enter your script path
```

**Alternative: Using an agent hook for more sophisticated validation**

If you want Claude to verify test results:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify all Flutter golden tests pass. Run: flutter test --update-goldens. Check the test results and report any failures.",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

---

## Additional Pro Tips

1. **Use the `/hooks` menu** to see all configured hooks, enable/disable them, or add new ones interactively
2. **Debug hooks** with `Ctrl+O` to toggle verbose mode and see hook execution in the transcript
3. **Use `$CLAUDE_PROJECT_DIR`** to reference project files in hook commands (better than relative paths)
4. **Environment variables in hooks**: Store in `CLAUDE_ENV_FILE` or reference with `$VAR_NAME`
5. **Block file edits** with a `PreToolUse` hook to protect sensitive files:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'echo \"$INPUT\" | jq -r \".tool_input.file_path\" | grep -E \"(\\.env|package-lock\\.json|\\.git/)\" && (echo \"Protected file - cannot edit\" >&2; exit 2) || exit 0'"
          }
        ]
      }
    ]
  }
}
```

**For more details**, see the official documentation:
- Full reference: https://code.claude.com/docs/en/hooks.md
- Setup guide: https://code.claude.com/docs/en/hooks-guide.md

---

