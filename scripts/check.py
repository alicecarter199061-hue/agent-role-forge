#!/usr/bin/env python3
"""agent-role-forge 自检脚本（零依赖，ponytail 规则：留一个可运行 check）。

校验 5 项：
1. 包结构完整（SKILL.md + 4 references + 1 script 存在）
2. SKILL.md frontmatter 含必要字段（name/description/metadata.version/snapshot_date）
3. 内置索引条目字段完整（每个 `| 项目 |` 行含 仓库名/Stars/定位/可借鉴机制 四列）
4. references 互相引用一致（SKILL.md 引用的文件都存在）
5. 输出模板含必备章节（Identity/Responsibilities/Boundaries/Style/Constraints）

用法: python3 scripts/check.py   （在 skill 包根目录运行，或 python3 <path>/scripts/check.py）
"""

import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent

EXPECTED_FILES = [
    "SKILL.md",
    "references/agent-oss-index.md",
    "references/retrieval-methods.md",
    "references/grill-questions.md",
    "references/output-template.md",
    "scripts/check.py",
]

FRONTMATTER_FIELDS = ["name", "description", "version", "snapshot_date"]

# output-template.md 必备章节
TEMPLATE_SECTIONS = [
    "Identity", "Responsibilities", "Boundaries",
    "Style", "Constraints", "参考来源",
]


def check_files() -> tuple[bool, str]:
    missing = [f for f in EXPECTED_FILES if not (SKILL_DIR / f).exists()]
    if missing:
        return False, f"缺失文件: {', '.join(missing)}"
    return True, f"{len(EXPECTED_FILES)} 个文件齐全"


def check_frontmatter() -> tuple[bool, str]:
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return False, "SKILL.md 无 frontmatter"
    fm = m.group(1)
    for field in FRONTMATTER_FIELDS:
        if not re.search(rf"^{re.escape(field)}:", fm, re.M):
            return False, f"frontmatter 缺字段: {field}"
    return True, "frontmatter 字段齐全"


def check_index() -> tuple[bool, str]:
    text = (SKILL_DIR / "references/agent-oss-index.md").read_text(encoding="utf-8")
    rows = [ln for ln in text.splitlines() if ln.startswith("|") and "**" in ln and ln.count("|") >= 6]
    if not rows:
        return False, "索引表无数据行"
    bad = []
    for ln in rows:
        cells = [c.strip() for c in ln.strip("|").split("|")]
        # 期望: 项目 | Stars | YC批次 | 定位 | 可借鉴机制
        if len(cells) < 5 or any(not c for c in cells[:2]):
            bad.append(ln[:60])
    if bad:
        return False, f"索引条目字段不完整({len(bad)}行): {bad[0]}..."
    return True, f"索引 {len(rows)} 条条目字段完整"


def check_refs_consistent() -> tuple[bool, str]:
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    refs = set(re.findall(r"references/([\w.-]+\.md)", text))
    missing = [r for r in refs if not (SKILL_DIR / "references" / r).exists()]
    if missing:
        return False, f"SKILL.md 引用的文件缺失: {', '.join(missing)}"
    return True, f"SKILL.md 引用一致（{len(refs)} 个 references）"


def check_template() -> tuple[bool, str]:
    text = (SKILL_DIR / "references/output-template.md").read_text(encoding="utf-8")
    missing = [s for s in TEMPLATE_SECTIONS if s not in text]
    if missing:
        return False, f"输出模板缺章节: {', '.join(missing)}"
    return True, f"输出模板 {len(TEMPLATE_SECTIONS)} 个必备章节齐全"


def main() -> int:
    checks = [
        ("包结构完整", check_files),
        ("frontmatter 字段", check_frontmatter),
        ("内置索引条目", check_index),
        ("references 引用一致", check_refs_consistent),
        ("输出模板章节", check_template),
    ]
    passed = 0
    for name, fn in checks:
        ok, msg = fn()
        mark = "PASS" if ok else "FAIL"
        print(f"[{mark}] {name}: {msg}")
        passed += ok
    print(f"\n结果: {passed}/{len(checks)} 通过")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
