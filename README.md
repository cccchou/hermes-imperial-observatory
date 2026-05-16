# 🔭 司天监 · AI 科研助手

> 一个基于 Hermes Agent 的全自动学术论文追踪与知识管理工具。六个 AI Agent 按固定时刻表协作，自动完成文献搜录、知识建库、交叉验证、代码执行、日报生成。

---

## 这是什么？

每天清晨到下午，六位 AI Agent 自动接力工作：

```
07:00  读邮件 → 制定当日计划
08:00  搜 arXiv、Google Scholar → 找新论文
08:30  建知识库页面 → 存档
09:00  交叉校验 → 去重补漏
10:00  跑代码 → 复现实验
14:00  出日报 → 汇总推送
```

你睡醒就能看报告，不用手动搜论文。

---

## 👥 六位 Agent 各司其职

| Agent | 做什么 | 产出 |
|-------|--------|------|
| **advisor**（监正） | 读 arXiv 邮件，定当日关注方向 | `TASKS.md` |
| **researcher**（灵台郎） | 搜 arXiv + Google Scholar | `RESEARCH.md` |
| **wiki**（主簿） | 论文存档到 Obsidian 知识库 | `wiki/` 页面 |
| **summarizer**（五官正） | 交叉引用，去重去噪 | `SUMMARY.md` |
| **executor**（挈壶正） | 跑代码复现，验证结果 | `OUTPUT/` |
| **reporter**（司历） | 汇总当天产出，生成日报 | `REPORT.md` |

覆盖四大领域：**LLM · 广告/推荐算法 · 气象 AI · 量化金融 AI**。

---

## ⚙️ 怎么跑的

用 Hermes Agent 的 `cronjob` 定时触发，`context_from` 把上一个 Agent 的输出喂给下一个：

```yaml
advisor (07:00) → researcher (08:00) → wiki (08:30)
                                      → summarizer (09:00)
                                      → executor (10:00)
                                      → reporter (14:00)
```

每天自动运行，无需人工干预。

---

## 📚 翰林院 · 辅助工具

三个独立 Skill，需要时手动触发：

| Skill | 做什么 |
|-------|--------|
| **coder** | ACM 算法风格编码，解题、写项目 |
| **claude-code-delegate** | 调用 Claude Code 处理复杂代码任务 |
| **codefun-problem-solving** | 校招笔试题库刷题（CodeFun2000） |

---

## 📦 安装

```bash
git clone git@github.com:cccchou/hermes-imperial-observatory.git

# 复制 skill 到 Hermes 目录
cp -r skills/司天监/* ~/.hermes/skills/
cp -r skills/翰林院/* ~/.hermes/skills/

hermes gateway restart
```

需要 Hermes Agent v0.11+。定时任务需自行配置 `cronjob`，参考各 `SKILL.md` 内的说明。

---

## 📁 目录

```
skills/
├── 司天监/
│   ├── multi-agent-research-pipeline/   ← 六 Agent 流水线
│   └── research-executor/               ← 代码执行员
└── 翰林院/
    ├── coder/                           ← 算法编码
    ├── claude-code-delegate/            ← Claude Code 桥接
    └── codefun-problem-solving/         ← 笔试刷题
```
