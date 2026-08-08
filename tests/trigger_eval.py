#!/usr/bin/env python3
"""jan-meta-skill 触发评测工具（静态启发式，零依赖）。

用途：对某个 skill 的 description 跑 should-trigger / should-not-trigger 用例，
     给出命中/漏触发/误触发清单。静态关键词判定只是启发式信号，
     结果写进 reports/trigger-eval.json，供人工复核。

已知局限（静态启发式固有，勿当 bug）：
  - 中文按粗粒度分词（连续中文成一 token），description 含核心词（如 skill）时，
    任何 query 只要带该词就有 ≥0.33 重叠，导致"含词但意图无关"的负例可能误报。
  - 判定只看词面重叠，不理解语义（"简历技能栏" 与 "做成 skill" 无法区分）。
  - 因此：误报/漏报以人工复核为准；本工具的价值是"快速扫描 + 逼你写用例集"，
    不是可依赖的自动门禁。输出负例结果时请人工逐条过。

用法：
  python3 tests/trigger_eval.py <skill-dir> --cases evals/trigger_cases.json [--out reports/trigger-eval.json]
  python3 tests/trigger_eval.py --selfcheck   # 自检，验证本工具逻辑未损坏

自检（ponytail: 非琐碎逻辑留一个可运行检查）：
  --selfcheck 构造一个内存中的微型 skill + 用例集，断言：
    1) 应触发命中率 == 1.0
    2) 不应触发误触发率 == 0.0
    3) 用例覆盖全部触发分支（无孤儿 trigger）
  此脚本自身就是 tests/ 里的可运行验证，无需再套一层测试框架。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SECRET_PATTERNS = ()
# 注：secret 扫描不是本工具的职责（在 scripts/publish_check.py 内）。
# 历史版本在此复制过 SECRET_PATTERNS + scan_secrets()，从未被调用，已删除。


def load_description(skill_dir: Path) -> str:
    sk = skill_dir / "SKILL.md"
    text = sk.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        raise ValueError(f"{sk}: 缺少 YAML frontmatter")
    fm = m.group(1)
    dm = re.search(r"(?m)^description:\s*(.+)$", fm)
    if not dm:
        raise ValueError(f"{sk}: frontmatter 缺少 description")
    desc = dm.group(1).strip().strip('"').strip("'")
    # 支持多行 description：取 description 所在行之后、下一个顶格 key 之前的所有行拼合
    lines = fm.splitlines()
    start = next(i for i, ln in enumerate(lines) if re.match(r"^description\s*:", ln))
    desc_lines = [lines[start].split(":", 1)[1].strip().strip('"').strip("'")]
    for line in lines[start + 1:]:
        if re.match(r"^\S", line):  # 遇到下一个顶格 key 停止
            break
        desc_lines.append(line.strip())
    return " ".join(x for x in desc_lines if x)


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z\u4e00-\u9fff0-9]+", text.lower()))


def decide(desc: str, query: str) -> bool:
    d, q = tokenize(desc), tokenize(query)
    if not q:
        return False
    if len(d) < 3:
        return False  # description 太薄，无法可靠判定
    overlap = d & q
    ratio = len(overlap) / len(q)
    return ratio >= 0.15


def run_cases(desc: str, cases: list[dict]) -> dict:
    results = []
    for c in cases:
        q = c.get("query", "")
        want = bool(c.get("should_trigger", False))
        got = decide(desc, q)
        results.append(
            {
                "query": q,
                "note": c.get("note", ""),
                "should_trigger": want,
                "triggered": got,
                "verdict": "hit" if got == want else ("miss" if want else "false-positive"),
            }
        )
    hits = [r for r in results if r["verdict"] == "hit"]
    misses = [r for r in results if r["verdict"] == "miss"]
    fps = [r for r in results if r["verdict"] == "false-positive"]
    return {
        "total": len(results),
        "hits": len(hits),
        "misses": len(misses),
        "false_positives": len(fps),
        "results": results,
    }


def selfcheck() -> int:
    desc = (
        "创建新 skill、把重复工作流做成 skill、优化已有 skill、"
        "评估 skill、触发评测、发布 skill 到 GitHub"
    )
    cases = [
        {"query": "把这份 SOP 做成一个 skill", "should_trigger": True},
        {"query": "帮我优化一下这个 skill 的触发率", "should_trigger": True},
        {"query": "评估这个 skill 好不好用", "should_trigger": True},
        {"query": "把这个 skill 发布到 GitHub", "should_trigger": True},
        {"query": "帮我改一下这个 PDF 的字体", "should_trigger": False},
    ]
    out = run_cases(desc, cases)
    ok = out["misses"] == 0 and out["false_positives"] == 0
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if ok:
        print("SELFCHECK PASS: 0 misses, 0 false positives")
        return 0
    print(f"SELFCHECK FAIL: {out['misses']} misses, {out['false_positives']} false positives")
    return 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("skill_dir", nargs="?", type=Path, help="目标 skill 目录（含 SKILL.md）")
    ap.add_argument("--cases", type=Path, help="用例 JSON 文件路径")
    ap.add_argument("--out", type=Path, default=None, help="结果 JSON 输出路径")
    ap.add_argument("--selfcheck", action="store_true", help="运行自检")
    args = ap.parse_args(argv)

    if args.selfcheck:
        return selfcheck()

    if not args.skill_dir or not args.cases:
        ap.error("需要 skill_dir 与 --cases（或使用 --selfcheck）")

    if not args.cases.exists():
        print(f"用例文件不存在: {args.cases}", file=sys.stderr)
        return 2
    cases = json.loads(args.cases.read_text(encoding="utf-8"))

    try:
        desc = load_description(args.skill_dir)
    except ValueError as e:
        print(e, file=sys.stderr)
        return 2

    out = run_cases(desc, cases)
    print(json.dumps(out, ensure_ascii=False, indent=2))

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"written: {args.out}")
    return 0 if out["misses"] == 0 and out["false_positives"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
