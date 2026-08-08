# agent-role-forge · 角色锻造炉

创建 agent 角色（persona / 系统 prompt）时，**优先从 GitHub 开源 agent 项目与构建库取材 → 检索同类 → 依据实际任务 DIY** 出通用系统 prompt 文本，并带审问流程的通用型 skill 包。

跨平台通用：适配 **Multica / WorkBuddy / Codex / Claude Code / ZCode** 等场景。

> 命名对应：本仓库（团队分享）用英文名 `agent-role-forge`；个人 ZCode 环境入库后为 `09.06·Agent治理·agent-role-forge`（同一内容，见文末「安装·本机个人版」）。

## 为什么有这个工具

凭空设计角色容易"假大空"。开源世界里每个成熟的 agent 项目（OpenHands、CrewAI、Mem0、LangGraph…）都沉淀了可借鉴的**角色机制**——指令风格、边界写法、工具策略、记忆结构。本 skill 把这一套取材流程固化下来：内置索引 + 检索方法 + 审问 + DIY + 通用 prompt 输出。

## 目录结构

```
agent-role-forge/
├── SKILL.md                              # 方法论主文件（6 步工作流 + 智能调度 single/team + 硬规则）
├── README.md                             # 本文件（安装/使用/分享）
├── references/
│   ├── agent-oss-index.md                # 内置开源 agent 项目与构建库索引（YC 系 + 框架库 + D 节设计模式）
│   ├── retrieval-methods.md              # GitHub 检索方法（gh search / API 现成命令）
│   ├── grill-questions.md                # 审问问题库（第0步角色结构判断 + 必问5项 + 团队审问 T1-T4）
│   └── output-template.md                # 通用 prompt 模板 + single/team 输出展示 + 各平台接入
├── scripts/
│   ├── check.py                          # 自检脚本（5 项校验，零依赖）
│   └── publish_check.py                  # 发布治理检查（包验证 + secret 扫描，复用 jan-meta-skill）
├── tests/
│   └── trigger_eval.py                   # 触发评测脚本（复用 jan-meta-skill，--selfcheck 自检）
├── evals/
│   └── trigger_cases.json                # 触发评测用例（应触发/近邻负例/无关 17 组）
├── reports/
│   ├── prior-art-candidates.md           # 同类研究记录（keep/adapt/reject/invent 取舍）
│   ├── eval-evidence.md                  # 评测证据（触发评测 + 人工复核 + 证据边界）
│   └── trigger-eval.json                 # 触发评测结果
└── agents/
    └── interface.yaml                    # 意图收敛记录（触发/输入/输出/边界/成功标准）
```

## 快速安装（团队推荐 ⭐）

**把下面这段整段复制，发给你的 agent（Claude / ZCode / Codex / Multica agent 任选）**——它会自动判断平台并装好：

> 请安装 agent-role-forge（角色锻造炉）skill：从 https://github.com/alicecarter199061-hue/agent-role-forge 获取全部文件（SKILL.md、references/、scripts/），按当前平台自动判断装到合适的 skills 位置。如果对装到哪个位置不确定，先问我一句确认再装。装完运行 `python3 <skill路径>/scripts/check.py` 确认输出「结果: 5/5 通过」，并告诉我装到了哪个位置。

更省事的一句：**「帮我安装 agent-role-forge 这个 skill，来源是 github.com/alicecarter199061-hue/agent-role-forge」**

## 手动备选（技术细节，需要精确控制时用）

| 方式 | 命令 / 位置 |
|---|---|
| 手动拷贝（ZCode/Claude/Codex 生态） | 拷到 `~/.agents/skills/agent-role-forge/` |
| npx skills（open agent skills 生态） | `npx skills add alicecarter199061-hue/agent-role-forge -g -y` |
| Multica | `multica skill import --url https://github.com/alicecarter199061-hue/agent-role-forge` |
| ZCode 个人版（治理入库） | `~/.zcode/skills/09.06·Agent治理·agent-role-forge/`（中文命名 + 进 `09.01·Agent治理` 伞 + 完成判据） |

> ZCode 注意：装完需**完全重启** ZCode，新 skill 才会出现在 `/` 菜单（进程级缓存）。

## 使用

调用本 skill（对话中说"帮我造个角色/设计一个 agent 角色"，或显式 `/agent-role-forge`）。核心 6 步：

1. **审问需求** — 按 `references/grill-questions.md` 确认目标/触发场景/平台/权限/风格
2. **查内置索引** — `references/agent-oss-index.md` 按任务类型匹配候选
3. **检索同类** — 内置索引不满足时用 `references/retrieval-methods.md` 的 gh search 命令
4. **取材参考** — 只读看候选仓库 README/角色定义，提炼可借鉴机制（标注来源）
5. **DIY 角色** — 按 `references/output-template.md` 产出**平台无关通用 prompt 文本**
6. **展示 + 确认** — 展示 prompt + 参考来源 + 平台接入一步，**确认后才创建**

> 设计原则：**只产出定义并展示，不实际创建**。创建动作须用户确认后执行（Multica `multica agent create` / WorkBuddy 写人格文件 / Codex 写 toml 等，见 output-template.md）。

## 自检

```bash
python3 scripts/check.py
# 期望输出: 结果: 5/5 通过
```

## 内置索引说明

内置开源库索引是 **2026-08-08 快照**（YC 系 agent + 构建框架库，含 Stars 与"可借鉴的角色机制"）。数据可能过期——索引里的检索方法（gh search）是时效性兜底；更新方法见 `references/agent-oss-index.md` 文末。

## 贡献 / 分享

- 给团队分享：把本仓库 clone 或 `npx skills add` 即可。
- 更新索引后记得同步 `SKILL.md` 的 `snapshot_date`。
- License: MIT（随仓库）。
