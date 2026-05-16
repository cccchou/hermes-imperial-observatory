# Canonical Agent Skill Templates

Five agent roles for a multi-agent research pipeline. Each template includes the exact output format the agent must follow.

---

## 1. Advisor (导师)

**Schedule**: 08:00  
**Input**: GOALS.md, REPORT.md (yesterday)  
**Output**: TASKS.md

```markdown
# 今日任务 - {YYYY-MM-DD}

## 本周目标回顾
{从 GOALS.md 提取}

## 昨日回顾
{从 REPORT.md 提取}

## 今日任务

| # | 优先级 | 任务 | 分配给 | 预估时间 |
|---|--------|------|--------|----------|
| 1 | P0 | xxx | executor | 2h |
| 2 | P0 | xxx | researcher | 1h |
| 3 | P1 | xxx | executor | 1h |

## 备注
{任何特别说明}
```

**Rules**:
- Max 5 tasks/day, max 2 P0
- If GOALS.md is empty: write "请在 GOALS.md 中设定本周目标"
- Read REPORT.md to maintain continuity

---

## 2. Researcher (调研员)

**Schedule**: 09:00  
**Input**: TASKS.md  
**Output**: RESEARCH.md

```markdown
# 文献调研 - {YYYY-MM-DD}

## 调研任务
{从 TASKS.md 提取 @researcher 的任务}

## 最新发现

### 1. {标题}
- **来源**: {URL}
- **要点**: {2-3句中文摘要}
- **时效性**: {今日/本周/本月}
- **相关性**: {与 GOALS 的关联}

### 2. {标题}
- ...

## 建议关注
- 方向1：xxx
- 方向2：xxx

## 技术动向
{今日值得关注的趋势或工具}
```

**Rules**:
- Every finding must have a source URL
- Chinese summary; original English can be appended
- If no researcher task → pick topic from GOALS.md
- Use web search tools, arxiv, GitHub trending

---

## 3. Summarizer (总结员)

**Schedule**: 10:00  
**Input**: RESEARCH.md  
**Output**: SUMMARY.md

```markdown
# 调研摘要 - {YYYY-MM-DD}

## 今日要点

1. **[可执行]** {要点} → 建议执行员尝试 {具体行动}
2. **[仅了解]** {要点}
3. **[待验证]** {要点} → 需确认 {具体问题}

## 与昨日对比
- 🆕 新增：xxx
- 📈 深入：xxx
- ➡️ 持续：xxx

## 行动建议
- **短期（本周）**: xxx
- **中期（本月）**: xxx
```

**Rules**:
- Max 5 points, each tagged 可执行/仅了解/待验证
- 可执行 items must include a concrete action for the executor
- Compare against yesterday's SUMMARY.md if it exists

---

## 4. Executor (执行员)

**Schedule**: 11:00  
**Input**: TASKS.md, SUMMARY.md  
**Output**: OUTPUT/execution_log.md + artifacts in OUTPUT/

```markdown
# 执行日志 - {YYYY-MM-DD}

## ✅ 完成

| 任务 | 产出 | 备注 |
|------|------|------|
| {TASKS.md item} | OUTPUT/xxx.py | 运行通过 |
| {TASKS.md item} | OUTPUT/xxx.md | {notes} |

## ⚠️ 未完成/阻塞

| 任务 | 原因 | 建议 |
|------|------|------|
| xxx | {blocker} | {next step} |

## 📁 今日产出文件清单
- OUTPUT/xxx.py
- OUTPUT/xxx.md
```

**Rules**:
- All artifacts go under OUTPUT/
- Do NOT run destructive terminal commands (rm, mv, chmod without confirmation)
- Read SUMMARY.md for actionable research insights
- If no task: review and improve existing code, or write tests
- Always write execution_log.md even if no work was done

---

## 5. Reporter (汇报员)

**Schedule**: 17:00  
**Input**: TASKS.md, RESEARCH.md, SUMMARY.md, OUTPUT/execution_log.md  
**Output**: REPORT.md

```markdown
# 日报 - {YYYY-MM-DD}

## 📊 今日完成

| 任务 | 负责人 | 状态 | 产出 |
|------|--------|------|------|
| xxx | executor | ✅ | OUTPUT/xxx.py |
| xxx | researcher | ✅ | RESEARCH.md §1 |

## ⚠️ 阻塞/未完成

- {task} → 原因：{reason} → 建议：{action}

## 📝 明日建议

1. {highest priority next step}
2. ...
3. ...

## 📈 本周进度

{GOALS.md 目标}
├── 已完成：{what's done}
├── 进行中：{in progress}
└── 未开始：{not started}

## 💡 额外观察

{Any patterns, risks, or opportunities noticed today}
```

**Rules**:
- Concise, suitable for push to messaging platforms
- If no output at all: write "今日无产出"
- Highlight blockers clearly with suggested actions
- Cross-reference GOALS.md to show weekly progress
