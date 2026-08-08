#!/usr/bin/env python3
"""jan-meta-skill 发布治理链检查器（零依赖，只检查不写 GitHub）。

用法：
  python3 scripts/publish_check.py <skill-dir>            # 包验证（结构/frontmatter/版本/引用）
  python3 scripts/publish_check.py <skill-dir> --scan-secrets  # 外加 secret 扫描
  python3 scripts/publish_check.py --selfcheck            # 自检
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKILL_FILE = "SKILL.md"
MAX_BODY_LINES = 500

SECRET_PATTERNS = (
    r"(?i)(api[_-]?key|secret|token|password|passwd|bearer)\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{12,}",
    r"(?i)sk-[A-Za-z0-9_\-]{20,}",
    r"(?i)ghp_[A-Za-z0-9]{30,}",
    r"AKIA[0-9A-Z]{16}",
    r"/Users/[A-Za-z0-9_\-]+/",          # 绝对本机路径
)


def load_skill(root: Path) -> dict:
    """返回 frontmatter 字段 + 统计信息；任何缺失/畸形以 error 列出。"""
    errors: list[str] = []
    sk = root / SKILL_FILE
    if not sk.exists():
        return {"errors": [f"缺少 {SKILL_FILE}"]}
    text = sk.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {"errors": ["SKILL.md 缺少 YAML frontmatter"]}
    fm = m.group(1)
    body = text[m.end():]
    fields: dict[str, str] = {}
    for name in ("name", "description"):
        dm = re.search(rf"(?m)^{name}:\s*(.+)$", fm)
        if not dm:
            errors.append(f"frontmatter 缺少 {name}")
        else:
            fields[name] = dm.group(1).strip().strip('"').strip("'")
    dm = re.search(r"(?m)^version:\s*(.+)$", fm)  # version 可选：缺失不报错，有则纳入一致性检查
    if dm:
        fields["version"] = dm.group(1).strip().strip('"').strip("'")
    if fields.get("name", "") != root.name:
        errors.append(f"frontmatter name '{fields.get('name')}' 与目录名 '{root.name}' 不一致")
    body_lines = len(body.strip().splitlines()) if body.strip() else 0
    if body_lines > MAX_BODY_LINES:
        errors.append(f"SKILL.md body {body_lines} 行，超过 {MAX_BODY_LINES} 行限制")
    return {"fields": fields, "body_lines": body_lines, "errors": errors}


def check_references(root: Path) -> list[str]:
    """孤儿引用检查：references/ 下未被 SKILL.md 点名的文件算警告。"""
    warnings: list[str] = []
    sk = root / SKILL_FILE
    if not sk.exists():
        return warnings
    text = sk.read_text(encoding="utf-8")
    refs_dir = root / "references"
    if refs_dir.exists():
        for ref in sorted(refs_dir.rglob("*.md")):
            rel = ref.relative_to(root)
            if ref.name not in text:
                warnings.append(f"{rel}: SKILL.md 未点名该引用（孤儿文件？）")
            ref_text = ref.read_text(encoding="utf-8")
            lines = len(ref_text.splitlines())
            if lines > 300 and "## " not in ref_text:
                warnings.append(f"{rel}: {lines} 行且无标题目录，建议加目录")
    return warnings


def check_version_consistency(root: Path, fm: dict) -> list[str]:
    """版本一致性检查：frontmatter version 与 manifest.json / VERSION / git tag 对齐。

    manifest.json 或 VERSION 存在才检查（缺失时警告不报错，避免对无版本管理
    的本地 skill 误阻断）。
    """
    errors: list[str] = []
    fm_ver = fm.get("fields", {}).get("version")
    manifest = root / "manifest.json"
    if manifest.exists():
        try:
            m_ver = json.loads(manifest.read_text(encoding="utf-8")).get("version")
            if m_ver and fm_ver and m_ver != fm_ver:
                errors.append(f"manifest.json version '{m_ver}' 与 frontmatter '{fm_ver}' 不一致")
        except (json.JSONDecodeError, OSError) as e:
            errors.append(f"manifest.json 无法解析: {e}")
    ver_file = root / "VERSION"
    if ver_file.exists():
        v_ver = ver_file.read_text(encoding="utf-8").strip()
        if v_ver and fm_ver and v_ver != fm_ver:
            errors.append(f"VERSION 文件 '{v_ver}' 与 frontmatter '{fm_ver}' 不一致")
    return errors


def scan_secrets(root: Path) -> list[str]:
    findings: list[str] = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.name in {"publish_check.py"}:
            continue
        if p.suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".zip", ".pyc"}:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if any(re.search(pat, line) for pat in SECRET_PATTERNS):
                findings.append(f"{p.relative_to(root)}:{i}")
    return findings


def selfcheck() -> int:
    import tempfile

    problems = 0
    with tempfile.TemporaryDirectory() as td:
        good = Path(td) / "good-skill"
        (good / "references").mkdir(parents=True)
        (good / "SKILL.md").write_text(
            "---\nname: good-skill\ndescription: 一个正常 skill\nversion: 1.0.0\n---\n\n# Body\n\n短正文。\n",
            encoding="utf-8",
        )
        (good / "manifest.json").write_text('{"version": "1.0.0"}', encoding="utf-8")
        info = load_skill(good)
        if info["errors"]:
            print(f"FAIL good-skill: {info['errors']}")
            problems += 1
        if check_version_consistency(good, info):
            print(f"FAIL good-skill version 一致: 不应有告警")
            problems += 1
        if scan_secrets(good):
            print("FAIL good-skill secret scan: 不应有命中")
            problems += 1

        bad = Path(td) / "bad-skill"
        bad.mkdir()
        (bad / "SKILL.md").write_text(
            "---\nname: other-name\ndescription: api_key=sk-abcdefghijklmnopqrstuvwxyz123456\nversion: 1.0.0\n---\n\nx\n",
            encoding="utf-8",
        )
        (bad / "manifest.json").write_text('{"version": "2.0.0"}', encoding="utf-8")
        info = load_skill(bad)
        if not info["errors"]:
            print("FAIL bad-skill: 应报 name 不一致")
            problems += 1
        vc = check_version_consistency(bad, info)
        if not vc:
            print("FAIL bad-skill: 应报版本不一致")
            problems += 1
        sec = scan_secrets(bad)
        if not sec:
            print("FAIL bad-skill secret scan: 应命中 key 泄露")
            problems += 1

    if problems == 0:
        print("SELFCHECK PASS: good 通过 / bad 被拦截")
        return 0
    print(f"SELFCHECK FAIL: {problems} 处不符合预期")
    return 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("skill_dir", nargs="?", type=Path, help="目标 skill 目录")
    ap.add_argument("--dry-run", action="store_true", help="仅检查不写 GitHub（默认即只检查，保留该旗标以匹配 release-gates 文档）")
    ap.add_argument("--scan-secrets", action="store_true", help="额外做 secret 扫描")
    ap.add_argument("--selfcheck", action="store_true", help="运行自检")
    args = ap.parse_args(argv)

    if args.selfcheck:
        return selfcheck()
    if not args.skill_dir:
        ap.error("需要 skill_dir（或使用 --selfcheck）")

    root = args.skill_dir.resolve()  # 相对路径（如 `.`）会得到空目录名，resolve 后防假报警
    info = load_skill(root)
    errors = list(info["errors"])
    warnings = check_references(root)
    warnings += check_version_consistency(root, info)

    sec: list[str] = []
    if args.scan_secrets:
        sec = scan_secrets(root)
        errors += [f"SECRET: {f}" for f in sec]

    report = {
        "skill_dir": str(root),
        "name": info.get("fields", {}).get("name"),
        "body_lines": info.get("body_lines"),
        "errors": errors,
        "warnings": warnings,
        "secrets": sec,
        "verdict": "blocked" if errors else ("ok" if not warnings else "ok-with-warnings"),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
