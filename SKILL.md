---
name: agent-role-forge
description: 角色锻造炉。创建 agent 角色（persona）前，优先从内置 GitHub 开源 agent 项目与构建库索引取材，检索同类项目，依据实际任务 DIY 出通用系统 prompt 文本，并带审问流程。Use when user wants to 创建/设计 agent 角色、persona、系统提示词、角色人设，或说"帮我造个角色/做个 agent 角色/设计系统 prompt"。跨平台通用：适配 Multica、WorkBuddy、Codex、Claude Code、ZCode 等。
version: 1.0.0
snapshot_date: 2026-08-08
metadata:
  origin: personal
---

# 角色锻造炉 (Agent Role Forge)

## 定位

创建 agent 角色时的**取材 + 审问 + DIY** 工作台。核心主张：**不凭空造角色，先看开源世界里别人怎么造**——从 GitHub 开源 agent 项目与 agent 构建库取真实机制，再按任务定制，产出**平台无关的通用系统 prompt 文本**。

产出物是通用 prompt 文本（身份/职责/边界/工作流/风格/约束），由用户按目标平台接入（Multica / WorkBuddy / Codex / Claude Code / ZCode 的接入方式见 `references/output-template.md`）。

**只产出定义并展示，不实际创建角色**。创建动作留给用户或目标平台（除非用户明确要求直接创建）。

## When to Use

- 用户要"创建/设计一个 agent 角色 / persona / 角色人设 / 系统提示词"
- 用户要复制某个开源 agent 项目的角色机制到自己项目
- 用户在多平台（Multica / WorkBuddy / Codex / Claude / ZCode）需要同一角色的适配定义

### Avoid when

- 只改已有角色的一个小字段（直接改，不用走全流程）
- 用户明确只要快速草稿（跳过审问，直接出稿）

## 前置条件

- 网络可达 GitHub（`gh` CLI 可用或 API 直连；直连超时走代理 `ALL_PROXY=http://127.0.0.1:7897`）
- `gh auth status` 可登录（用于检索；未登录时可用 GitHub 公开 API `curl api.github.com` 替代）

## 目录约定

本 skill 路径可能随安装方式变化（`multica skill import` / `npx skills add` / 手动拷贝）。引用文件时用 `${SKILL_DIR}` 占位，实际使用时替换为 skill 真实路径：

- `${SKILL_DIR}/references/agent-oss-index.md` — 内置开源 agent 项目与构建库索引（快照，含更新方法）
- `${SKILL_DIR}/references/retrieval-methods.md` — GitHub 检索方法（gh search / GitHub API 现成命令）
- `${SKILL_DIR}/references/grill-questions.md` — 角色需求审问问题库
- `${SKILL_DIR}/references/output-template.md` — 通用 prompt 输出模板 + 各平台接入说明
- `${SKILL_DIR}/scripts/check.py` — 自检脚本（`python3 ${SKILL_DIR}/scripts/check.py`）

## 核心理念

1. **先看开源，再 DIY**：内置索引 + 检索方法保证"角色不是凭空设计"，每个机制有来源可查。
2. **审问先行**：需求不清时，角色必歪。用 grill-questions 把"要什么角色、干什么、不干什么"问清楚再动笔。
3. **通用 prompt，平台适配**：主产出是平台无关的 prompt 文本；平台格式差异放 `references/output-template.md` 适配层，不污染主产出。
4. **参考不等于照抄**：开源项目提供的是**机制灵感**（如 OpenHands 的编码 agent 指令风格、Mem0 的记忆职责），按实际任务裁剪，禁止原样拷贝版权文本。

## How It Works（6 步工作流）

### Step 1 — 审问需求（grill）

按 `references/grill-questions.md` 的 8~12 个核心问题审问，直到以下 5 项明确：

| 必问项 | 说明 |
|---|---|
| 角色目标 | 这个 agent 到底完成什么任务 |
| 触发场景 | 何时被调用（对话中/自动/定时/子代理） |
| 平台约束 | 目标平台（Multica/WorkBuddy/Codex/Claude/ZCode）+ 模型 |
| 工具权限 | 能用什么工具/命令，禁止什么 |
| 风格语气 | 语气、篇幅、输出习惯 |

审问原则：不问废话，已明确的项跳过；用户说"直接干/轻量"时降级为 1 轮快速确认（只问目标 + 边界）。

**Step 1 完成判据**：产出「角色需求卡」且必问 5 项（目标/触发场景/平台模型/权限/风格）均有明确答案；有缺项则继续审问。

### Step 2 — 查内置索引

在 `references/agent-oss-index.md` 中按**任务类型**匹配候选：

- 任务是**编码/开发** → OpenHands、smol-ai/developer、MetaGPT、OpenAI Agents SDK
- 任务是**记忆/上下文** → Mem0、Letta、Zep
- 任务是**浏览器/网页** → browser-use、Firecrawl、E2B
- 任务是**工具集成** → Composio、MCP
- 任务是**编排/多代理** → LangGraph、CrewAI、AutoGen、Agno

选中 1~3 个高度相关条目，记录其"可借鉴机制"。

**Step 2 完成判据**：已选中 1~3 个候选并写下各自"可借鉴机制"；索引未命中则显式标注"未命中，走 Step 3"。

### Step 3 — 检索同类（兜底 + 补充）

内置索引不满足，或需要更多同类项目时，按 `references/retrieval-methods.md` 执行：

```bash
# 按关键词找同类 agent 项目（最常用）
gh search repos "<任务关键词> agent" --limit 10 --sort stars

# 找 agent 构建库/框架
gh search repos "<关键词> agent framework" --limit 10 --sort stars

# 找系统 prompt 参考
gh search repos "<关键词> system prompt" --limit 10 --sort stars
```

无 gh 时用 GitHub API：`curl -s "https://api.github.com/search/repositories?q=<关键词>+agent&sort=stars&per_page=10"`。

**Step 3 完成判据**：检索返回 ≥1 个可用候选；网络失败则记录降级（标注"无检索结果，基于通用模板 DIY"）后进入 Step 4。

### Step 4 — 取材参考

对 Step 2/3 选中的候选，用只读方式取真实内容（**不 clone 全库**）：

```bash
# 看 README 提炼定位与机制
curl -sL "https://raw.githubusercontent.com/<owner>/<repo>/main/README.md"

# 找角色/prompt 定义文件（如 .claude/、AGENTS.md、agents/ 目录）
gh api repos/<owner>/<repo>/contents --jq '.[].name'
```

提炼 3~5 条**可借鉴机制**（角色指令风格 / 边界写法 / 工具策略 / 记忆结构），记录来源。

**Step 4 完成判据**：已提炼 3~5 条机制且每条带来源标注；不足 3 条则回 Step 3 补充候选或接受 1~2 条。

### Step 5 — DIY 角色（产出通用 prompt）

按 `references/output-template.md` 的结构产出**平台无关通用 prompt 文本**：

- **身份**：角色名 + 一句话定位（来自审问目标 + 开源参考）
- **职责**：核心任务 + 主工作流（参考开源机制裁剪）
- **边界**：明确不做的事（防越权，审问里的"禁忌"）
- **工具与权限**：允许/禁止（审问确认）
- **风格**：语气、篇幅、输出格式（审问确认）
- **约束**：安全、数据、外部动作确认制

每条机制在 prompt 旁标注来源（`参考: OpenHands 的 <机制>`），让用户知道灵感从哪来。

**Step 5 完成判据**：产出 prompt 覆盖 output-template 的全部 6 节（Identity/Responsibilities/Boundaries/Tools/Style/Constraints），且每条借鉴机制带来源标注。

### Step 6 — 展示 + 确认

- 输出：完整通用 prompt 文本 + 参考来源清单 + 可借鉴机制摘要
- 附各平台接入一步（引用 `references/output-template.md` 的适配小节，如 `multica agent create --instructions "..."`、WorkBuddy 写 SOUL.md 等）
- **不实际创建**，等用户确认；用户说"创建"才调平台命令

**Step 6 完成判据**：已展示 prompt + 来源 + 平台接入一步，且未执行任何创建动作（除非用户显式确认）。

## 硬规则

- 只产出定义并展示；创建动作须用户明确确认后才执行。
- 参考开源项目时标注来源；禁止原样拷贝大段版权文本（机制可借鉴，文本自己写）。
- 内置索引是快照（`snapshot_date: 2026-08-08`），数据可能过期——Step 3 的检索方法是时效性兜底；更新索引见 `references/agent-oss-index.md` 末尾。
- 审问不啰嗦：已明确的不问，用户说"直接干"就跳过审问。
- 产出语言跟随用户（中文对话 → 中文 prompt；但 prompt 正文建议保留英文关键字段名以便跨平台）。

## 错误处理（降级，不中断）

| 故障 | 降级方案 |
|---|---|
| `gh` 未登录/不可用 | 用 `curl api.github.com/search/repositories` 替代（限速但可用） |
| GitHub 直连超时 | `ALL_PROXY=http://127.0.0.1:7897` 走代理重试 |
| 内置索引未命中 | 直接跳 Step 3 检索；仍无结果则基于通用模板 DIY 并标注"无直接参考" |
| `check.py` 不可用 | 跳过自检，人工核对文件存在 |

> [警告] **[步骤名] 已降级** — 统一错误模板，说明降级原因与影响。

## 注意事项

- 本 skill 自带审问问题库（`references/grill-questions.md`），不依赖任何本地 grill skill，可跨平台分享。
- 输出 prompt 正文建议英文（跨平台稳定），解释与讨论用对话语言。
- 试跑验收：对任一真实任务走完 6 步，索引命中 + 产出通用 prompt + 展示参考来源。
