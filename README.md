# 🔭 司天监 · Hermes Agent 六部协作框架

> *「仰观天文，俯察地理，六官各司其职，日复一日，未尝懈怠。」*
>
> 以明代司天监官制为纲，六位 AI Agent 各守其位，构建全自动学术研究流水线。
> 每日 07:00 至 14:00，七小时内完成文献搜录、知识建库、交叉验证、代码执行、报告生成。

---

## 🏛️ 架构

```
                         ┌──────────────────┐
                         │   监正 · Advisor │  ← 07:00 读邮件，制定当日计划
                         └────────┬─────────┘
                                  │ TASKS.md
          ┌───────────────────────┼───────────────────────┐
          ▼                       ▼                       ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│ 灵台郎 · Researcher│   │ 主簿 · Wiki     │   │ 五官正 · Summarizer│
│ 08:00 搜录论文    │   │ 08:30 建知识页   │   │ 09:00 交叉校验    │
└────────┬────────┘   └────────┬────────┘   └────────┬────────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               │ context_from 全链串联
                               ▼
                    ┌─────────────────────┐
                    │ 挈壶正 · Executor    │  ← 10:00 执行代码
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ 司历 · Reporter      │  ← 14:00 生成日报
                    └─────────────────────┘
```

---

## 👥 六部职官

| 官职 | Agent | 时辰 | 职责 | 产出 |
|------|-------|------|------|------|
| **监正** | `advisor` | 辰时 (07:00) | 批阅邮件，洞察全局，制定一日方略 | `TASKS.md` |
| **灵台郎** | `researcher` | 辰时三刻 (08:00) | 遍搜 arXiv、Scholar，博采众长 | `raw/+RESEARCH.md` |
| **主簿** | `wiki` | 巳时 (08:30) | 考据校勘，建档入库，垂范后世 | `wiki/` 知识页 |
| **五官正** | `summarizer` | 巳时 (09:00) | 交叉引证，去芜存菁，明辨真伪 | `SUMMARY.md` |
| **挈壶正** | `executor` | 巳时三刻 (10:00) | 算学推演，代码运行，验之以实 | `OUTPUT/` |
| **司历** | `reporter` | 未时 (14:00) | 汇整奏报，上达天听，一日之功 | `REPORT.md` |

---

## ⚙️ 调度

以 Hermes Agent `cronjob` 驱动，`context_from` 串接上下环节：

```yaml
advisor (07:00) → researcher (08:00) → wiki (08:30)
                                      → summarizer (09:00)
                                      → executor (10:00)
                                      → reporter (14:00)
```

四大领域定轨：**LLM · 广告算法 · 气象 AI · 量化 AI**，每日每领域至多三篇 TOP 论文入阁。

---

## 📚 翰林院 · 辅助 Skill

除六部之外，尚有三名「翰林院编修」，供不时之需：

| 官职 | Skill | 说明 |
|------|-------|------|
| **算学博士** | `coder` | ACM 算法大神人格，Karpathy 纪律 + Addyosmani 工程，代码即文章 |
| **行人司** | `claude-code-delegate` | 出使外邦（Claude Code），代行复杂编码、图片分析之事 |
| **武举** | `codefun-problem-solving` | 应战校招笔试，CodeFun2000 题库，见题即破 |

---

## 📦 安装

```bash
# 1. 克隆
git clone git@github.com:cccchou/hermes-imperial-observatory.git

# 2. 将 skills/ 下的目录复制到 Hermes skill 目录
cp -r skills/司天监/* ~/.hermes/skills/autonomous-ai-agents/
cp -r skills/司天监/* ~/.hermes/skills/research-group/
cp -r skills/翰林院/* ~/.hermes/skills/software-development/

# 3. 重启 Hermes
hermes gateway restart
```

---

## 📜 说明

- 本框架已在 **上交大物理海洋博士** 的实际科研环境中稳定运行
- 四大领域知识库持续积累，Obsidian 双向链接打通
- 每日产出存储在 `/mnt/d/hermes_output/YYYYMMDD/`
- 兼容 Hermes Agent v0.11+

---

> *「天行有常，不为尧存，不为桀亡。制天命而用之。」——《荀子·天论》*
>
> 六部协作，日拱一卒，功不唐捐。
