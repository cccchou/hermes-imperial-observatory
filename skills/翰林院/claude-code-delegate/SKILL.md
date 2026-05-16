---
name: claude-code-delegate
description: "Delegate complex coding tasks to Claude Code CLI (best model). Agent acts as reviewer/messenger, not coder."
version: 1.0.0
tags: [claude-code, delegation, coding, agent-tool]
---

# Claude Code 委托编码

**原则：把专业编码工作交给 Claude Code，Agent 只做审查和报信。**

## 何时调用

- 用户说"用 claude code 写/修/重构/debug"
- 复杂工程任务（多文件、架构设计、算法实现）
- 不主动调用，除非用户明确要求

## 调用方式

```bash
 claude -p "prompt" --output-format text --max-turns 5
```

## 模型选择

优先用最好模型：`--model claude-sonnet-4-20250514`（或当前最新）

## Agent 的职责

1. **派活** → 把用户需求翻译为清晰的 prompt 发给 Claude Code。prompt 中必须要求 Claude Code 输出"逐步调试结果"（用具体例子展示中间状态），不只是算法逻辑。
2. **审查** → 检查 Claude Code 输出是否正确、完整，是否包含了逐步调试过程
3. **报信** → 简洁汇报结果，不重复灌代码。如果 Claude Code 没给调试过程，补充或重新要求。

## 能力边界

**Claude Code 内置能力已覆盖以下领域，无需外部 skill 注入：**
- ACM 竞赛算法（DP/贪心/二分/图论/字符串）
- 深度学习模型（Transformer/MoE/扩散模型）

**不要浪费时间在 GitHub 搜索"Claude Code algorithm skills"**——已验证不存在专门的 ACM/算法 repo，Claude Code 自身能力足够。外部 repo 只提供流程包装（如测试先行），不增加算法知识。

## Pipeline

1. **派活** → 把用户需求翻译为清晰的 prompt（中文/英文均可），发给 Claude Code
2. **审查** → 检查输出是否正确、完整，发现错误时告诉 Claude Code 修正
3. **报信** → 简洁汇报结果，引用 Claude Code 原话，不重复灌代码

## 陷阱：bash 引号吞代码

`claude -p "包含 Python 代码"` 会触发 bash 语法错误，因为代码里的单引号、括号被 shell 解释。

**正确做法：heredoc**
```bash
cat << 'PROMPT' | claude -p "$(cat)" --output-format text --max-turns 5
<prompt文本和代码>
PROMPT
```

## 陷阱：DeepSeek 不支持图片 → Claude Code 看图

当前主模型 deepseek-v4-pro 不支持多模态（image_url），`vision_analyze` 报 400。需要分析图片时，把本地文件路径直接传给 Claude Code：
```bash
claude -p "分析这张图片：/path/to/image.jpg" --output-format text
```

## 代码来源声明（强制）

**每次写代码前，必须在代码块前声明来源。**

```
✍️ Agent直接手写    → Agent 自己写的
🤖 Claude Code CLI  → 调用了 claude
🔀 delegate_task    → 委派给子智能体
```

声明格式：代码块前一行加粗标注，如 `**✍️ Agent直接手写：**`

## Notes

- Claude Code 输出直接引用给用户看，Agent 不逐行解释
- 如果 Claude Code 出错，告诉用户错误信息 + 重试建议
- 简单脚本（<30行）Agent 自己写，不调 Claude Code
- 已验证可用：`claude` v2.1.141
- 关联 skill：`coder` — 更完整的编码人格（ACM算法 + 工程纪律 + 输出规范）
- **外网数据聚合**：terminal curl 超时时，用 execute_code + Python urllib 替代 → `references/execute-code-fallback.md`

## 陷阱：Coder Profile 认证失败

`hermes -p coder chat -q "..."` 可能因 API key 未从 .env 继承而报 401。修复：显式传入环境变量。

```bash
DEEPSEEK_API_KEY=$(grep DEEPSEEK_API_KEY ~/.hermes/.env | cut -d= -f2) hermes -p coder chat -q "..." --quiet
```

如果 coder profile 超时（>120s），说明任务太复杂或网络不稳 → 改用 heredoc 直接调 Claude Code CLI，不经过 profile。
