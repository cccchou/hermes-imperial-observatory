---
name: multi-agent-research-pipeline
description: "Design and deploy multi-agent research pipelines with cron scheduling, context chaining, and structured output formats. Use when the user wants to build a 'research group' of cooperating agents — advisor, researcher, summarizer, executor, reporter — that run autonomously on a schedule."
version: 1.0.0
tags: [multi-agent, cron, pipeline, research, delegation, autonomous]
---

# Multi-Agent Research Pipeline

Design and deploy autonomous multi-agent pipelines where a "research group" of agents cooperate on a shared workspace through scheduled cron jobs with chained context.

## When to Use

The user wants multiple agents working together autonomously — e.g., "像课题组一样，导师分配任务、学生调研、总结、执行、汇报。"

## Architecture

```
┌──────────────────────────────────────────────┐
│            Shared Workspace                  │
│  GOALS.md    ← User writes big-picture goals │
│  TASKS.md    ← Advisor decomposes            │
│  RESEARCH.md ← Researcher writes findings     │
│  SUMMARY.md  ← Summarizer distills            │
│  REPORT.md   ← Reporter generates daily report│
│  OUTPUT/     ← Executor produces artifacts    │
└──────────────────────────────────────────────┘

  07:00 🎓 Advisor     ──→ TASKS.md
  08:00 📚 Researcher  ──→ RESEARCH.md   (ctx: advisor)
  09:00 📝 Summarizer  ──→ SUMMARY.md    (ctx: researcher)
  10:00 💻 Executor    ──→ OUTPUT/       (ctx: advisor)
  14:00 📊 Reporter    ──→ REPORT.md     (ctx: all)
```

**注意：Coder Agent（`hermes -p coder`）不在这个流水线里。** Coder 是独立的手动 profile，不属于 cron 定时任务，不读写课题组 workspace。当需要复杂编码时由用户手动唤醒。不要在执行员 cron job 里嵌入 coder 逻辑。

## Step-by-Step Deployment

### Step 1: Create shared workspace

```bash
mkdir -p /path/to/workspace/{OUTPUT,logs,skills}
touch /path/to/workspace/{GOALS,TASKS,RESEARCH,SUMMARY,REPORT}.md
```

GOALS.md is the only file the user writes manually. Everything else is agent-generated.

### Step 2: Create agent skill files

Each agent gets a SKILL.md in `workspace/skills/`. Every skill follows this template:

```markdown
---
name: role-name
description: "Brief role description"
version: 1.0.0
tags: [role, pipeline]
---

# Role Name

## Workflow
1. Read input file(s) — list exact paths
2. Perform task — be specific
3. Write output file — list exact path + format template

## Output Format
[Markdown template the agent MUST follow]

## Rules
- File constraints (read-only, write-only paths)
- Behavior when input is missing
```

See `references/agent-skills.md` for the five canonical agent skill templates.

### Step 3: Create cron jobs with context chaining

```yaml
# Advisor — no upstream
cron: "0 8 * * *"
context_from: []
workdir: /path/to/workspace

# Researcher — depends on advisor
cron: "0 9 * * *"
context_from: [advisor_job_id]

# Summarizer — depends on researcher
cron: "0 10 * * *"
context_from: [researcher_job_id]

# Executor — depends on advisor (reads TASKS.md)
cron: "0 11 * * *"
context_from: [advisor_job_id]

# Reporter — depends on all
cron: "0 17 * * *"
context_from: [advisor_job_id, researcher_job_id, executor_job_id]
```

**Key rule**: `context_from` injects the upstream job's most recent output into the downstream agent's prompt. Downstream agents can also directly read files from the shared workspace since they share `workdir`.

### Step 4: Write GOALS.md

The user writes one file. Format:

```markdown
# 本周目标

🔴 P0 Task 1 (deadline)
   → researcher: xxx
   → executor: xxx

🔴 P0 Task 2 (deadline)
   ...

🟡 P1 Task 3
   ...
```

## Design Rules

| Rule | Reason |
|------|--------|
| Agents only write to their designated files | Prevents overwrite conflicts |
| No agent deletes files | Safety; reporter handles summarization |
| All paths absolute, under workspace/ | Cron jobs need full paths |
| Output formats are structured markdown | Reporter can parse them |
| 3-minute cron timeout per job | Prevents runaway agents |
| Advisor reads GOALS.md + REPORT.md | Maintains continuity day-to-day |

## Pitfalls

- **Cron jobs don't survive session restarts.** Recreate them if they vanish. Keep a script or note of job IDs.
- **context_from injects text, not files.** The downstream agent gets the upstream's output as prompt context, not as a file. For file access, the agent must read from the shared workspace directly.
- **Don't overload the advisor.** Max 5 tasks/day, max 2 P0. Agents have 3-minute limits.
- **Skills are loaded by file path, not by skill name with skill_view.** Cron jobs reference the skill markdown file directly in their prompt.
- **Memory compacting.** When memory fills up, replace multiple entries with one compact entry rather than adding more. Use memory action=replace with old_text to consolidate.

## Files

- `references/agent-skills.md` — Five canonical agent skill templates with full output format specifications.
