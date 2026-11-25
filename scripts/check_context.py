#!/usr/bin/env python3
"""检查Codex项目上下文是否齐全、够小、够新（手册附录M2）。

规则：
1. 必需文件都存在且非空；
2. 根目录AGENTS.md不超过12000字节；所有AGENTS.md合计不超过28000字节（Codex默认上限32KiB，留余量）；
3. 每个context文件第一行形如"最后更新：YYYY-MM-DD｜Owner：…｜来源：…"，且不超过各自期限。
退出码：0通过；1有错误。用法：python scripts/check_context.py [--today YYYY-MM-DD]
"""
import argparse
import datetime as dt
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAX_DAYS = {
    "context/eureka_product.md": 30,
    "context/tracking_plan.md": 7,
    "context/dw_schema.md": 7,
    "context/metrics.md": 14,
    "context/experiment_ledger.md": 7,
    "context/glossary.md": 30,
}
REQUIRED = ["AGENTS.md", "context/AGENTS.md", "experiments/AGENTS.md", *MAX_DAYS]
HEADER = re.compile(r"^最后更新：(\d{4}-\d{2}-\d{2})｜Owner：([^｜]+)｜来源：(.+)$")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", default=dt.date.today().isoformat())
    today = dt.date.fromisoformat(ap.parse_args().today)
    errs, warns = [], []

    for rel in REQUIRED:
        p = ROOT / rel
        if not p.exists() or not p.read_text(encoding="utf-8").strip():
            errs.append(f"缺少或为空：{rel}")

    root_agents = ROOT / "AGENTS.md"
    if root_agents.exists() and root_agents.stat().st_size > 12000:
        errs.append(f"根目录AGENTS.md {root_agents.stat().st_size} 字节，超过12000")
    total = sum(p.stat().st_size for p in ROOT.rglob("AGENTS.md") if ".git" not in p.parts)
    if total > 28000:
        errs.append(f"全部AGENTS.md合计 {total} 字节，超过28000（Codex默认只读32KiB）")

    for rel, days in MAX_DAYS.items():
        p = ROOT / rel
        if not p.exists():
            continue
        first = p.read_text(encoding="utf-8").splitlines()[0].strip() if p.stat().st_size else ""
        m = HEADER.match(first)
        if not m:
            errs.append(f"{rel} 第一行缺少\"最后更新：YYYY-MM-DD｜Owner：…｜来源：…\"")
            continue
        age = (today - dt.date.fromisoformat(m.group(1))).days
        if age > days:
            errs.append(f"{rel} 已 {age} 天未更新（期限 {days} 天，Owner：{m.group(2)}）")
        elif age > days - 2:
            warns.append(f"{rel} 将在 {days - age} 天后超期（Owner：{m.group(2)}）")

    for w in warns:
        print("提醒：" + w)
    if errs:
        print("\n".join("错误：" + e for e in errs))
        return 1
    print("上下文检查通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
