#!/usr/bin/env python3
"""把DW里Segment相关schema的表与字段导出为Markdown，写入context/dw_schema.md。

用法（只读账号）：
  export POSTGRES_HOST=... POSTGRES_PORT=5432 POSTGRES_DATABASE=... POSTGRES_USER=codex_ro POSTGRES_PASSWORD=...
  python scripts/refresh_dw_schema.py --schemas eureka_web [eureka_app] --owner 姓名 > context/dw_schema.md

只读取information_schema，不读取业务数据。
"""
import argparse
import datetime as dt
import os
import sys

try:
    import psycopg
except ImportError:
    sys.exit('缺少依赖：pip install "psycopg[binary]"')

SQL = """
SELECT c.table_schema, c.table_name, c.column_name, c.data_type
FROM information_schema.columns c
WHERE c.table_schema = ANY(%s)
ORDER BY c.table_schema, c.table_name, c.ordinal_position
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--schemas", nargs="+", required=True, help="Segment source对应的schema名")
    ap.add_argument("--owner", default="智慧芽数据负责人")
    args = ap.parse_args()

    if os.environ.get("POSTGRES_USER") not in {"codex_ro", "growthbook_ro"}:
        sys.exit("请使用只读账号（codex_ro）运行")

    conn = psycopg.connect(
        host=os.environ["POSTGRES_HOST"],
        port=os.environ.get("POSTGRES_PORT", "5432"),
        dbname=os.environ["POSTGRES_DATABASE"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        sslmode=os.environ.get("POSTGRES_SSLMODE", "require"),
    )
    with conn, conn.cursor() as cur:
        cur.execute(SQL, (args.schemas,))
        rows = cur.fetchall()

    today = dt.date.today().isoformat()
    out = [
        f"最后更新：{today}｜Owner：{args.owner}｜来源：DW information_schema（scripts/refresh_dw_schema.py）",
        "",
        "# DW表结构：Segment同步表",
        "",
        "由脚本生成，不要手改。列名为Segment转换后的下划线小写；排序用`timestamp`，去重用`id`。",
        "",
    ]
    current = None
    for schema, table, col, dtype in rows:
        key = f"{schema}.{table}"
        if key != current:
            out += ["", f"## {key}", "", "| 字段 | 类型 |", "|---|---|"]
            current = key
        out.append(f"| {col} | {dtype} |")
    if not rows:
        out.append("未读到任何表：核对schema名与codex_ro的USAGE权限。")
    print("\n".join(out))


if __name__ == "__main__":
    main()
