# 通用 prompt 输出模板 + 平台接入说明

## 一、通用系统 prompt 结构（平台无关）

按以下结构产出**通用 prompt 文本**（建议正文用英文关键词保证跨平台稳定，说明文字跟随对话语言）。每条机制旁标注参考来源（`参考: <项目> 的 <机制>`），让用户知道灵感从哪来。

```markdown
# <角色名> — <一句话定位>

## Identity（身份）
- 你是谁：<角色名>，<一句话身份>
- 定位：<这个 agent 存在的理由，来自审问"目标">

## Responsibilities（职责）
- 核心任务：<主任务 1-3 条>
- 工作流：<主流程步骤，参考开源机制的裁剪版>
- 成功标准：<完成到什么程度算成功>

## Boundaries（边界）
- 不做：<明确禁止做的事，来自审问"禁忌">
- 权限：允许 <…> / 禁止 <…>（来自审问"权限"）

## Tools & Permissions（工具与权限）
- 可用工具：<列表>
- 敏感操作：<外部动作必须经用户确认才执行>

## Style（风格）
- 语气：<来自审问"风格">
- 篇幅与格式：<输出习惯>

## Constraints（约束）
- 安全：<数据、隐私、外部发布边界>
- 失败处理：<不会/失败时怎么办>
- 通用规则：<平台无关的硬约束>

---

参考来源：
- <仓库 full_name> — <借鉴了它的什么机制>
```

## 二、各平台接入说明

### Multica
```bash
# 创建 agent（通用 prompt 放 --instructions）
multica agent create \
  --name "<角色名>" \
  --runtime-id "<runtime-id>" \
  --model "<model>" \
  --description "<一句话描述，≤255 字符，仅目录展示>" \
  --instructions "<上面的通用 prompt 全文>"

# 挂 skill（⚠️ 必做：agent create 本身不挂 skill，创建后必须单独挂载，
#   否则成员裸奔无能力——团队模式最常见的坑）
multica agent skills add <agent-id> --skill-ids <skill-id-1>,<skill-id-2>

# 验证挂载成功（skills 非空）
multica agent get <agent-id>

# 查看本机 runtime
multica runtime list
```
注意：Multica 中 `description` 仅目录展示（≤255 码点），**真正注入运行时的是 `instructions`**——persona/边界放 instructions。

### WorkBuddy（人格文件）
WorkBuddy 角色 = 工作区人格文件（`~/.workbuddy/`）：
- `SOUL.md` — 你是谁（价值观/边界/语气），对应通用 prompt 的 Identity + Style + Constraints
- `IDENTITY.md` — 名字/物种/vibe/emoji 元信息
- `USER.md` — 用户画像
- `BOOTSTRAP.md` — 首次对话引导
将通用 prompt 拆写进 SOUL.md（核心）+ IDENTITY.md（元信息）。

### Codex（~/.codex/agents/*.toml）
```toml
# ~/.codex/agents/<角色名>.toml
[agent]
name = "<角色名>"
description = "<触发描述>"
developer_instructions = """<通用 prompt 全文>"""
```

### Claude Code（subagents）
```markdown
# 在项目的 .claude/agents/<角色名>.md 下
---
name: <角色名>
description: <触发描述>
tools: <允许的工具列表>
---
<通用 prompt 全文>
```

### ZCode / Claude Code 全局（skill 或 AGENTS.md）
- 作为 skill：放 `~/.agents/skills/<角色名>/SKILL.md`，frontmatter 写 `name` + `description`（中英双语）。
- 作为全局指令：追加到 `AGENTS.md` 相关小节。

## 三、输出展示格式（Step 6）

### single 模式

最终向用户展示：

1. **通用 prompt 文本**（上节模板渲染结果）
2. **参考来源清单**：`来源仓库 → 借鉴机制`（3~5 条）
3. **平台接入**：按目标平台给 1 条接入命令/路径（引用本节）
4. **确认**："要我在 <平台> 创建这个角色吗？"——等用户确认才执行创建

### team 模式

最终向用户展示：

1. **角色分工表**：
   ```
   团队目标: <整队最终交付>
   协作关系: <总指挥 / 串行或并行 / 谁汇总>

   | 角色 | 定位（负责哪段） | 触发（被谁调用） | 专属工具/权限 |
   |---|---|---|---|
   | 角色1 | … | … | … |
   | 角色2 | … | … | … |
   ```
2. **每份 prompt 文本**：逐角色展示（每份按上节 6 节模板 + 来源标注）
3. **参考来源清单**：`来源仓库/模式 → 借鉴机制`（每个角色 1-3 条）
4. **平台接入**：每角色 1 条接入命令（如逐个 `multica agent create`），可给一条批量脚本
5. **确认**："要我在 <平台> 逐个创建这 N 个角色吗？"——等用户确认才执行

> **批量脚本必须包含挂载步骤**（Multica 场景）：`agent create` 后紧跟 `agent skills add`，逐角色挂对应 skill，并用 `agent get` 验证 skills 非空后再创建下一个。参考分工表「专属工具/权限」列决定每个角色挂哪些 skill。

> team 模式创建顺序建议：先建总指挥/调度角色（如需要），再建执行角色——让编排角色先就位。参考 D1 编排方案选型（独立编排角色为企业级标准）。
