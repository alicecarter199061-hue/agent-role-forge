# GitHub 检索方法

内置索引未命中或需要更多同类项目时，用本文件的方法检索。优先 `gh` CLI；不可用时降级 GitHub 公开 API。

## 0. 前置检查

```bash
gh auth status          # 确认已登录
# 未登录时可用公开 API（限速 ~10 次/分钟，够用）：
#   curl -s "https://api.github.com/search/repositories?q=..."
```

GitHub 直连超时：`export ALL_PROXY=http://127.0.0.1:7897` 后重试（本机已知经验）。

## 1. 找同类 agent 项目（最常用）

```bash
# 按任务关键词找 agent 项目，按 Star 排序
gh search repos "<任务关键词> agent" --limit 10 --sort stars

# 例：要找"浏览器自动化角色"的参考
gh search repos "browser automation agent" --limit 10 --sort stars
```

输出解读：看 name + description + language + stars，选出与任务最贴近的 2~3 个。

## 2. 找 agent 构建库 / 框架

```bash
gh search repos "<关键词> agent framework" --limit 10 --sort stars
gh search repos "<关键词> multi agent" --limit 10 --sort stars
```

## 3. 找系统 prompt / 角色定义参考

```bash
# 系统 prompt 合集仓库
gh search repos "system prompt collection" --limit 10 --sort stars
# 特定工具的角色定义（如 Claude Code subagents）
gh search repos "claude code subagents" --limit 10 --sort stars
# agent 角色/人设仓库
gh search repos "agent personas" --limit 10 --sort stars
```

## 4. 直接看候选仓库的真实内容（只读，不 clone）

```bash
# README（提炼定位与机制）
curl -sL "https://raw.githubusercontent.com/<owner>/<repo>/main/README.md"

# 列出仓库根目录（找 AGENTS.md / agents/ / .claude/ / prompts/ 等角色定义位置）
gh api repos/<owner>/<repo>/contents --jq '.[].name'

# 常见角色定义路径（按需拼接浏览）
#   .claude/agents/*.md        Claude Code subagents
#   agents/*.toml              Codex agents
#   AGENTS.md                  agent 方法论
#   prompts/*.md               prompt 库
gh api repos/<owner>/<repo>/contents/.claude/agents --jq '.[].name'
```

## 5. 通用 GitHub API 备查（无 gh 时）

```bash
# 按 Star 找热门 agent 项目
curl -s "https://api.github.com/search/repositories?q=<关键词>+agent&sort=stars&order=desc&per_page=10" \
  | python3 -c "import json,sys; [print(f\"{r['stargazers_count']:>7}  {r['full_name']:<40} {(r['description'] or '')[:70]}\") for r in json.load(sys.stdin)['items']]"
```

## 提炼机制的原则

1. 读 README 提炼**定位**（一句话）与**角色机制**（这个项目里的角色怎么定义：指令结构/边界/工具策略/记忆结构）。
2. 每个候选最多提炼 3 条可借鉴机制，标注来源。
3. 机制可借鉴，文本自己写——禁止原样拷贝大段版权文本。
4. 参考组合：通常 1 个主参考（高度相关）+ 1~2 个补充参考即可，不要贪多。
