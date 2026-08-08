# prior-art-candidates — 同类研究记录（agent-role-forge）

> 日期：2026-08-08 ｜ 档位：Governed（公开发布） ｜ 方法论：jan-meta-skill prior-art 双目录研究
> 结论先行：**未找到可直接替代 agent-role-forge 的现成 skill**，故 invent（自研）+ 从 4 个邻近项目语义吸收机制。

## 检索范围

- 本地：`~/.agents/skills/`（skill-scout / find-skills / skill-stocktake 等）
- 远程：skills.sh / GitHub 搜索（"agent persona skill"、"system prompt generator"、"role forge"、"persona builder"）

## 候选与取舍

| 候选 | 来源 | 取舍 | 理由 |
|---|---|---|---|
| **openclaw-persona-forge** | 本地 skill | **adapt** | 最接近"角色锻造"：抽卡式人设、多 references 结构、错误降级矩阵——但其 scope 仅限 OpenClaw 平台（SOUL/IDENTITY），frontmatter 明确"不适用于非 OpenClaw"。吸收其工作流结构，扩为跨平台。 |
| **skill-scout** | 本地 skill | **adapt** | GitHub 检索方法（gh search 现成命令）。吸收进 retrieval-methods.md。 |
| **find-skills** | 本地 skill | **adapt** | npx skills 生态发现。吸收安装/发现机制到 README。 |
| **skill-stocktake** | 本地 skill | **adapt** | scripts/ 工程化结构（scan.sh 等）。启发 scripts/check.py 的自检定位。 |
| **search-first / deep-research / research-ops** | 本地 skill | **adapt** | 检索方法（gh search 命令、GitHub API 兜底）。吸收进 retrieval-methods.md。 |
| **ztdx-knowledge**（个人） | 本地构建 | **adapt** | SKILL.md + references/ 渐进披露布局、完成判据写法。作为构建范本。 |
| **agent-oss-index 收录的开源项目**（OpenHands/CrewAI/LangGraph 等 18 个） | GitHub 索引 | **adapt** | 作为索引数据（可借鉴机制），不直接成为 skill 本体。 |
| 通用"system prompt generator"类 GitHub 仓库 | GitHub 搜索 | **reject** | 均为单次文本生成工具，无"审问+取材+DIY"闭环、无团队模式、无可分享 skill 结构，不满足需求。 |
| 通用"persona builder"类 | GitHub 搜索 | **reject** | 绑定单一平台（多为 Character.ai 风格）或需付费 API，与"通用型跨平台"定位不符。 |

## 结论

- **invent（自研）**：没有现成 skill 覆盖"创建 agent 角色时取材开源库 + 审问 + DIY + single/team 智能调度 + 跨平台可分享"这个组合。
- **keep（保留吸收）**：4 个本地 skill 的机制 + 索引内 18 个开源项目数据 + D1 设计模式。
- 归因：openclaw-persona-forge（工作流结构）、skill-scout/search-first（检索方法）、writing-great-skills（完成判据）、D1 编排模式（指挥/执行分离）。

## 证据边界

- 本文档记录的是**设计时的实际检索与取舍**（2026-08-08）。
- 索引数据（agent-oss-index.md）为 GitHub API 快照，标注 snapshot_date。
