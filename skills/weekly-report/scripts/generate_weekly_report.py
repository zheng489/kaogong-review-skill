#!/usr/bin/env python3
"""
考公周报自动生成脚本

Usage:
    python generate_weekly_report.py

Scans the Obsidian 考公笔记 vault for error files modified in the past 7 days,
computes statistics, and generates a weekly report markdown file.

Edit VAULT_PATH to match your Obsidian vault location.
"""

import re
import yaml
from pathlib import Path
from datetime import datetime, timedelta

# ============================================================
# CONFIG — Edit these paths to match your setup
# ============================================================
VAULT_PATH = Path("E:/obsidian/Obsidian Vault/考公笔记")
OUTPUT_DIR = VAULT_PATH / "周报"

# Error directories to scan
ERROR_DIRS = {
    "行测/错题汇总/判断推理": "判断推理",
    "行测/错题汇总/言语理解": "言语理解",
    "行测/错题汇总/图形推理": "图形推理",
}


def parse_frontmatter(filepath):
    """Extract YAML frontmatter from an Obsidian markdown file."""
    content = filepath.read_text(encoding="utf-8")
    if content.startswith("---"):
        end = content.find("---", 3)
        if end > 0:
            try:
                return yaml.safe_load(content[3:end])
            except Exception:
                return {}
    return {}


def get_module_from_path(rel_path):
    """Determine the module name from the relative directory path."""
    for dir_prefix, module in ERROR_DIRS.items():
        if rel_path.startswith(dir_prefix):
            return module
    return "其他"


def collect_weekly_data(week_ago):
    """Scan all error directories and return structured data."""
    data = {
        "判断推理": {"count": 0, "files": [], "types": {}, "errors": {}},
        "言语理解": {"count": 0, "files": [], "types": {}, "errors": {}},
        "图形推理": {"count": 0, "files": [], "types": {}, "errors": {}},
    }

    for rel_path, module in ERROR_DIRS.items():
        target = VAULT_PATH / rel_path
        if not target.exists():
            print(f"  [WARN] Directory not found: {target}")
            continue

        for f in sorted(target.rglob("*.md")):
            if f.name.startswith("_") or f.name.startswith("imgs"):
                continue
            if f.stat().st_mtime < week_ago.timestamp():
                continue

            data[module]["count"] += 1
            data[module]["files"].append(f)

            # Parse type and error cause from frontmatter
            fm = parse_frontmatter(f)
            t = fm.get("题型", "其他")
            data[module]["types"][t] = data[module]["types"].get(t, 0) + 1

            err = fm.get("错因", "")
            if err:
                data[module]["errors"][err] = data[module]["errors"].get(err, 0) + 1

    return data


def generate_report(data, year_week, week_start, week_end):
    """Generate the weekly report markdown content."""
    total = sum(m["count"] for m in data.values())
    module_order = ["言语理解", "判断推理", "图形推理"]

    # Module name mapping for display
    module_display = {
        "言语理解": "言语理解",
        "判断推理": "判断推理",
        "图形推理": "图形推理",
    }

    lines = []
    lines.append("---")
    lines.append(f"tags: [考公, 周报, 行测]")
    lines.append(f"date: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"week: {year_week}")
    lines.append("---")
    lines.append("")
    lines.append(f"# 考公周报 {year_week}（{week_start.strftime('%-m/%-d')} - {week_end.strftime('%-m/%-d')}）")
    lines.append("")
    lines.append("> [[做题总纲]] ← [[行测]]")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 1: Overview
    lines.append("## 一、本周概览")
    lines.append("")
    lines.append("| 模块 | 新增错题数 | 占比 |")
    lines.append("|------|-----------|------|")
    for mod in module_order:
        if mod in data:
            pct = f"{data[mod]['count'] / total * 100:.0f}%" if total > 0 else "0%"
            lines.append(f"| {module_display.get(mod, mod)} | {data[mod]['count']} | {pct} |")
    lines.append(f"| **合计** | **{total}** | **100%** |")
    lines.append("")

    # Section 2-4: Detailed per module
    for mod in module_order:
        if mod not in data or data[mod]["count"] == 0:
            continue

        module_label = {"判断推理": "判断推理"}.get(mod, mod)
        lines.append(f"## 二、{module_label} — 详细统计")
        lines.append("")

        if data[mod]["types"]:
            lines.append("| 题型 | 数量 |")
            lines.append("|------|------|")
            for t, c in sorted(data[mod]["types"].items(), key=lambda x: -x[1]):
                lines.append(f"| {t} | {c} |")
            lines.append("")

    # Section 5: Error cause analysis
    all_errors = {}
    for mod in data.values():
        for err, count in mod.get("errors", {}).items():
            all_errors[err] = all_errors.get(err, 0) + count

    if all_errors:
        lines.append("## 五、错因趋势")
        lines.append("")
        lines.append("| 本周高频错因 | 出现次数 |")
        lines.append("|-------------|---------|")
        for err, count in sorted(all_errors.items(), key=lambda x: -x[1]):
            lines.append(f"| {err} | {count} |")
        lines.append("")

    # Section 6: Output files
    all_files = []
    for mod in data.values():
        all_files.extend(mod["files"])

    if all_files:
        lines.append("## 六、本周产出文件清单")
        lines.append("")
        lines.append("| 路径 | 说明 |")
        lines.append("|------|------|")
        for f in sorted(all_files):
            rel = f.relative_to(VAULT_PATH)
            lines.append(f"| {rel} | |")
        lines.append("")

    # Section 7: Suggestions
    lines.append("## 七、下周建议")
    lines.append("")
    lines.append("1. **专项突破**：根据错题最多的模块安排针对性练习")
    lines.append("")
    lines.append("2. **限时训练建议**：")
    lines.append("   - 判断推理 15题限时 20分钟")
    lines.append("   - 图形推理 10题限时 10分钟")
    lines.append("   - 言语理解 15题限时 16分钟")
    lines.append("")
    lines.append("3. **错题重做**：隔日重做本周错题")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*自动生成于 {datetime.now().strftime('%Y-%m-%d')} 由 Hermes*")
    lines.append("")

    return "\n".join(lines)


def main():
    print("=== 考公周报生成器 ===", flush=True)

    # Calculate this week's Monday and Sunday
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    year_week = today.strftime("%Y-W%W")

    print(f"本周: {year_week} ({monday.strftime('%-m/%-d')} - {sunday.strftime('%-m/%-d')})", flush=True)
    print(f"扫描目录: {VAULT_PATH}", flush=True)

    # Collect data
    data = collect_weekly_data(monday)
    total = sum(m["count"] for m in data.values())
    print(f"\n扫描完成: {total} 道错题", flush=True)

    for mod, mdata in data.items():
        if mdata["count"] > 0:
            print(f"  {mod}: {mdata['count']} 题", flush=True)

    # Generate report
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{year_week}_考公周报.md"
    report = generate_report(data, year_week, monday, sunday)
    output_path.write_text(report, encoding="utf-8")
    print(f"\n周报已生成: {output_path}", flush=True)


if __name__ == "__main__":
    main()
