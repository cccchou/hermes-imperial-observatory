---
name: codefun-problem-solving
description: "Navigate CodeFun2000 (codefun2000.com), extract problem descriptions, and create solution templates for coding interview preparation."
version: 1.0.0
tags: [codefun, coding-interview, algorithm, ml, chinese-platform]
---

# CodeFun2000 Problem Solving

CodeFun2000 is a Chinese coding interview preparation platform focused on 校招 (campus recruitment). It features company-specific problem sets (华为, 美团, 阿里, 腾讯, 字节, etc.) with categorized difficulty (简单/中等/困难).

## Trigger

Use this skill when:
- User asks to open CodeFun, find problems, or start 刷题 (coding practice)
- User mentions "codefun2000", "codefun.com", or any variation
- User wants to practice coding interview problems from specific companies
- User asks for algorithm templates, cheatsheets, or problem-type reviews (二分/DP/贪心/树/图 etc.)
- Any coding interview prep output (solutions, templates, mock answers) should use this skill's conventions

## Platform URL

**Correct URL:** `https://codefun2000.com`  
**Common pitfall:** `codefun.com` is WRONG — it's an unrelated dead site. Always use `codefun2000.com`.

## Workflow

### Step 1: Navigate to Problem Set

Open `https://codefun2000.com/p` (redirects to `/pset`). This shows all company-specific problem sets.

### Step 2: Select Company and Problem

Click a company题库 (e.g., 美团机考编程题库). The problem list shows:
- Date of exam round
- Problem ID (e.g., P4911)
- Difficulty (简单/中等/困难)

### Step 3: Open Problem

Click the problem link. The IDE loads at `https://codefun2000.com/ide/PXXXX`.

### Step 4: Extract Problem Description

From the page snapshot, capture:
- Title, company, exam date, difficulty
- Time/memory limits, acceptance rate
- Full problem description (all sections)
- Input/output formats
- Example test cases

### Step 5: Create Solution Template

Save to `/mnt/d/hermes_output/YYYYMMDD/PXXXX_<problem_name>.py` (date folder convention — see Output Directory). Include:
1. **Header comment block**: problem metadata (source, company, difficulty, limits)
2. **Full problem description** as comments (all sections: preprocessing, model, optimizer, early-stopping, inference)
3. **Input/output format** with example
4. **Solution skeleton**: `solve()` function with numpy imports, stdin JSON parsing, stdout JSON output

### Step 6: Test Locally

```bash
echo '<json_input>' | python3 /mnt/d/hermes_output/PXXXX_<name>.py
```

Verify output matches expected.

## Output Directory

**ALL output goes to `/mnt/d/hermes_output/YYYYMMDD/`** — date-based subdirectory. Never use flat `/mnt/d/hermes_output/` or `/home/alex/`.

Example: today's outputs go to `/mnt/d/hermes_output/20260516/`.

When writing a file, ALWAYS create the date directory first if it doesn't exist. The user explicitly asked for this organization so they can browse by date.

## User Preferences

- User may ask the agent to write the full solution (not just a template) — comply directly, no pushback
- **Show code inline**: When user asks to "show" or "present" code, display it in the chat, not just the file path. The user reads on Feishu mobile/tablet and wants to see the content immediately. A file path alone is not enough — always include the full code in the response.
- Use concise explanations; the user values Impact over Novelty
- When explaining ML concepts (Adam, AdamW, etc.), use formula-first style with short intuitive summaries

## PDD 笔试模式（`小p` Trigger）

When the user says **「小p」** (or "小p + 题目"), switch to PDD live-exam mode. This is a high-stakes, time-critical sub-mode distinct from normal problem-solving:

### Mode Constraints
- **Time**: 10 minutes per problem MAX. The user has 4 problems × 2 hours and needs review time.
- **Output**: Pure code, zero explanation. No markdown, no commentary, no "let me explain".
- **Language**: Python 3 / PyPy3. No experimental features.

### I/O Convention (user-specified, do NOT change)

```python
import sys, json

data = sys.stdin.read().split()
it = iter(data)
# consume with: n = int(next(it)), x = next(it), etc.
# OR index with: data[0], data[1], ...

# ... solve ...

print(json.dumps(result))
```

**Pitfall**: Do NOT use `sys.stdin.readline()` or `input()` — user explicitly corrected this. Always `read().split()` + `iter()`/`next()` or index access.

### Debug Capability
If user provides a failing test case after initial code output:
1. Run the code against it mentally or via terminal
2. Identify the bug
3. Output corrected version — still pure code, no explanation

### Post-Mode: Save to Date Folder
After the exam session, all codes go to `/mnt/d/hermes_output/YYYYMMDD/`.

## Platform Notes

- 笔试题库（company-specific problem sets like 拼多多/华为/美团）may require **会员 (paid membership)** to view individual problem descriptions. The problem listing page (titles + difficulty) is visible, but clicking into specific problems may redirect to an error page or purchase prompt. When blocked:
  - Use problem titles from the listing page to infer the algorithm type (二分答案/滑动窗口/DP/etc.)
  - Write solutions based on standard algorithmic patterns matching the inferred type
  - Clearly annotate in output: "题目描述基于名称推断，完整描述需 CodeFun2000 会员"
- Problems require login to submit/self-test
- Supported languages: Python 3, PyPy3, C++17(O2), Java, Rust, Go, and more
- Input is single-line JSON via stdin; output is JSON via stdout
- Time limit typically 1000ms; memory not explicitly shown
- Some problems restrict imports (e.g., "仅依赖 numpy")

## References

- `references/adam-optimizer.md` — Adam & AdamW optimizer formulas, intuition, and interview talking points. Load when user asks about optimizers or when implementing ML-from-scratch problems.
- `references/pdd-algorithm-cheatsheet.md` — PDD 笔试 50+ algorithm templates across 12 categories (DP, 二分, 贪心, 树, 图, etc.). Load when user asks for algorithm templates, cheatsheets, or PDD-specific prep. Points to the full runnable file at `/mnt/d/hermes_output/YYYYMMDD/PDD_algorithm_cheatsheet.py`.
