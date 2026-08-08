# 开源 Agent 项目与构建库索引

> 快照日期：2026-08-08。Stars 为快照时点 GitHub 数据，可能已变化。
> 数据来源：GitHub API 实时检索 + YC 官网/公司官网验证。
> 用途：创建角色时的**取材候选**。每条给出"可借鉴的角色机制"，供 DIY 时引用。
> **时效性兜底**：索引过期或未命中时，用 `retrieval-methods.md` 的检索方法查最新同类项目；更新本索引见文末。

---

## A. YC 系开源 Agent 项目

| 项目 | Stars | YC 批次 | 定位 | 可借鉴的角色机制 |
|---|---|---|---|---|
| **OpenHands** (All-Hands-AI/OpenHands) | ~83K | W24 | AI 软件工程代理，全开源 MIT | 编码 agent 的指令风格：任务拆解 → 环境交互 → 验证闭环；"AI 开发者"角色的职责边界写法 |
| **smol-ai/developer** | ~12K | W24 | 第一个把开发 agent 嵌入自己 App 的库（swyx 创办） | 极简 prompt 哲学：小角色、单任务、可组合；smol developer 的系统提示词结构 |
| **Mem0** (mem0ai/mem0) | ~30K | S24 | Agent 记忆层，graph+vector+KV 混合存储 | "记忆管家"角色的职责：读/写/检索/遗忘策略、记忆与主 agent 的分工边界 |
| **Firecrawl** (firecrawl/firecrawl) | ~160K | W25 | 网页转 LLM-ready 数据 API（搜索/爬取/抓取） | 网页数据 agent 的工具策略：搜索→抓取→清洗→结构化输出链路 |
| **E2B** (e2b-dev/E2B) | ~13K | S23 | 开源沙箱，给 agent 真实执行环境（Firecracker） | 执行环境角色的边界：沙箱隔离、工具调用策略、安全约束写法 |
| **Dust** (dust-tt/dust) | ~1.4K | W23 | 自定义 AI agent 平台 | 自定义 agent 的模块化：拆块（model/tool/memory）组合成角色的思路 |
| **Superagent** (superagent-ai/superagent) | ~6.7K | W23 | 已转型：防 prompt injection/数据泄漏的安全库 | 安全边界的强制写法：输入校验、输出过滤、敏感动作确认制 |

> 同类 YC 生态（非纯开源/商用为主，配套开源 SDK）：Tavily（agent 搜索 API）、LiteLLM/BerriAI（LLM 统一网关）、Zep（记忆层）、Braintrust（agent 评估）。

---

## B. Agent 构建框架与库

| 项目 | Stars | 定位 | 可借鉴的角色机制 |
|---|---|---|---|
| **LangGraph** (langchain-ai/langgraph) | ~39K | 图状态机式 agent 编排，"构建有韧性的 agent" | 角色 = 状态机：定义状态、节点、边；把角色拆成"状态-转移"的写法 |
| **CrewAI** (crewAIInc/crewAI) | ~57K | 角色扮演多 agent 协作框架 | 角色 = Role/Goal/Backstory 三段式定义（最贴近"角色"的模板）；多角色协作分工 |
| **Microsoft AutoGen** (microsoft/autogen) | ~60K | agentic AI 编程框架 | 对话式多 agent：角色之间以消息交互的模式 |
| **MetaGPT** (FoundationAgents/MetaGPT) | ~70K | 多 agent 框架，"AI 软件公司"，SOP 驱动 | 角色 = 标准作业程序（SOP）：每个角色的输入/输出/交付物模板化 |
| **OpenAI Agents SDK** (openai/openai-agents-python) | ~28K | 轻量多 agent 工作流框架 | 角色 = instructions + tools + handoff 的结构；官方 prompt 写法 |
| **Agno** (agno-agi/agno，原 Phidata) | ~41K | "agent 的编程语言"，构建/运行/管理 | 角色 = 知识+工具+记忆+模型 的组合声明式定义 |
| **smolagents** (huggingface/smolagents) | ~29K | 极简 agent 库，"agent 用代码思考" | 极简主义：角色 prompt 短小，逻辑交给代码工具 |
| **Pydantic AI** (pydantic/pydantic-ai) | ~19K | Pydantic 风格 agent 框架 | 角色输出 = 类型化结构（schema），结构化输出的写法 |
| **Letta** (letta-ai/letta，原 MemGPT) | ~24K | 有状态 agent 平台，高级记忆 | "记忆分层"角色机制：核心记忆/工作记忆/归档的职责划分 |
| **Composio** (ComposioHQ/composio) | ~30K | 1000+ 工具集成的 agent 工具层 | 工具接入角色的策略：工具发现→鉴权→调用→结果回填 |
| **MCP** (modelcontextprotocol/modelcontextprotocol) | ~9K | Agent 工具协议标准（Anthropic） | 工具协议角色：把"能用什么工具"标准化声明，角色与工具解耦 |

> 其他常用参考：browser-use（网页自动化 agent）、google/adk-python（Google 开源 agent 工具包）、vercel/ai（TS AI 工具包）、microsoft/semantic-kernel、mastra-ai/mastra（TS agent 框架）。

---

## C. 按任务类型快速匹配表

| 任务类型 | 优先参考（索引内） |
|---|---|
| 编码 / 开发 | OpenHands、smol-ai/developer、MetaGPT、OpenAI Agents SDK |
| 记忆 / 上下文 | Mem0、Letta、Zep |
| 浏览器 / 网页 | browser-use、Firecrawl、E2B |
| 工具集成 / API | Composio、MCP |
| 多代理 / 编排 | LangGraph、CrewAI、AutoGen、Agno |
| 结构化输出 | Pydantic AI |
| 安全 / 防御 | Superagent |
| 通用工作流 agent | OpenAI Agents SDK、Dust、Agno |

---

## 更新本索引的方法

1. 检索最新热门：`gh search repos "<关键词> agent" --sort stars --limit 20`
2. 按 Stars 排序取头部，读 README 提炼定位 + 角色机制。
3. 更新表格（项目/Stars/定位/可借鉴机制），并把 `SKILL.md` 的 `snapshot_date` 改为当天日期。
4. 若数据变化大，同步更新 C 节匹配表。
