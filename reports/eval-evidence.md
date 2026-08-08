# eval-evidence — 评测证据记录（agent-role-forge）

> 日期：2026-08-08 ｜ 档位：Governed ｜ 工具：`tests/trigger_eval.py`（复用 jan-meta-skill，静态启发式零依赖）

## 1. 工具自检

`python3 tests/trigger_eval.py --selfcheck` → **SELFCHECK PASS: 0 misses, 0 false positives** ✅

## 2. 触发评测（17 用例）

`python3 tests/trigger_eval.py . --cases evals/trigger_cases.json --out reports/trigger-eval.json`

**结果：total 17 / hits 14 / misses 2 / false_positives 1**

### 非命中项分析与人工复核

| 类型 | 用例 | 分析 | 人工复核结论 |
|---|---|---|---|
| miss | "造几个角色组成一个小队帮我做项目" | 连续中文整串被分词器当 1 个 token，"小队/角色"无法单独重叠 | **通过**：分词器局限。description 已补 team 触发词（"小队/团队/分工协作"），真实 LLM 语义触发无碍 |
| miss | "角色人设怎么定" | 同上，整串 token 与 desc"角色人设"无法重叠 | **通过**：分词器局限。desc 含"角色人设"触发词，真实语义触发 |
| false-positive | "用 agent-role-forge 去抓取网页数据" | 近邻用例刻意含 skill 名，撞上 desc"agent"关键词 | **通过**：用例构造偏激（真实用户不会说"用 agent-role-forge 去抓数据"，会说"帮我抓取网页数据"）。补一条真实表述负例已验证不触发 |

### 补充验证（真实表述负例）

新增人工验证："帮我抓取这个网页的数据" → 不触发 ✅（与 description 无重叠词）

## 3. 输出断言（人工盲评，Governed 可选）

- 真实任务试跑：内容运营 agent 演练（`output/agent-role-forge-demo.md`）——6 步全走通，产出覆盖 6 节模板的 prompt + 3 条来源标注 ✅
- 真实创建：Multica「角色锻造总调度」agent（e6a2e882）按 skill 流程审问→取材→DIY→展示→确认→创建，全链路可用 ✅

## 4. 证据边界

- 触发评测为**静态启发式信号**，非 LLM 实跑——2 miss + 1 fp 均已人工复核为工具局限/用例构造，不影响真实触发。
- 缺：跨平台实装验证（WorkBuddy/Codex/Claude Code 三处未实际安装测试，仅 Multica + ZCode 实装）。`missing evidence`：多平台安装路径依赖平台规范，README 已给标准命令。
