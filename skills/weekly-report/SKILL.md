---
name: kaogong-weekly-report
description: "自动生成考公周报 — 扫描Obsidian考公笔记的错题数据，汇总统计本周新增错题数/错因分布/高频题型，生成结构化周报。"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [考公, 周报, 统计, 复盘]
    related_skills: [panduan-tuili-review, yanyu-lijie-review, tutu-review]
---

# 考公周报自动生成

扫描Obsidian考公笔记的错题数据，自动汇总本周新增错题，按模块/题型/错因统计，生成结构化周报。

## Trigger Conditions

当用户提出以下内容时加载：
- "生成这周的考公周报" / "周报"
- "汇总本周错题数据"
- "复盘这周的学习情况"
- "本周考公总结"

## Phase 1: Weekly Report Structure

周报遵循以下模板：

```markdown
---
tags: [考公, 周报, 行测]
date: YYYY-MM-DD
week: YYYY-Www
---

# 考公周报 YYYY-Www（M/D - M/D）

> [[做题总纲]] ← [[行测]]

---

## 一、本周概览

| 模块 | 新增错题数 | 占比 |
|------|-----------|------|
| 言语理解 | N | XX% |
| 判断推理 | N | XX% |
| 图形推理 | N | XX% |
| **合计** | **N** | **100%** |

## 二、判断推理 — 详细统计

（按日期列出子模块细分）

## 三、言语理解 — 详细统计

（按题型列出数量和高频题型 TOP3）

## 四、图形推理 — 详细统计

（按规律类型列出数量和高频规律）

## 五、错因趋势

| 本周高频错因 | 出现次数 |
|-------------|---------|
| ① 不理解题干推理 | N |
| ② 不明白选项功能 | N |
| ... | |

## 六、本周产出文件清单

| 路径 | 说明 |
|------|------|
| ... | ... |

## 七、下周建议

1. **专项突破**：...
2. **限时训练建议**：...
3. **错题重做**：...

---

*自动生成于 YYYY-MM-DD 由 Hermes*
```

## Phase 2: Data Collection

从Obsidian vault中收集数据：

### 错题文件扫描

```python
import re
from pathlib import Path

VAULT = Path("E:/obsidian/Obsidian Vault/考公笔记")
ERROR_DIRS = [
    "行测/错题汇总/判断推理",
    "行测/错题汇总/言语理解",
    "行测/错题汇总/图形推理",
]

def count_errors_since(path, since_date):
    """Count error files modified since a given date."""
    target = VAULT / path
    if not target.exists():
        return 0, []
    files = [f for f in target.rglob("*.md")
             if not f.name.startswith("_")]
    recent = [f for f in files
              if f.stat().st_mtime > since_date.timestamp()]
    return len(recent), recent
```

### YAML头解析

```python
import yaml

def parse_frontmatter(filepath):
    """Extract YAML frontmatter from an Obsidian markdown file."""
    content = filepath.read_text(encoding="utf-8")
    if content.startswith("---"):
        end = content.find("---", 3)
        if end > 0:
            try:
                return yaml.safe_load(content[3:end])
            except:
                return {}
    return {}
```

## Phase 3: Weekly Report Generation

### 收集命令

```python

def collect_weekly_data():
    """Scan all error directories for the past week and return structured data."""
    from datetime import datetime, timedelta
    week_ago = datetime.now() - timedelta(days=7)
    
    data = {
        "言语理解": {"count": 0, "files": [], "types": {}},
        "判断推理": {"count": 0, "files": [], "types": {}},
        "图形推理": {"count": 0, "files": [], "types": {}},
    }
    
    # Map directories to module names
    dir_map = {
        "行测/错题汇总/判断推理": "判断推理",
        "行测/错题汇总/言语理解": "言语理解",
        "行测/错题汇总/图形推理": "图形推理",
    }
    
    for rel_path, module in dir_map.items():
        target = VAULT / rel_path
        if not target.exists():
            continue
        for f in target.rglob("*.md"):
            if f.name.startswith("_"):
                continue
            if f.stat().st_mtime < week_ago.timestamp():
                continue
            data[module]["count"] += 1
            data[module]["files"].append(f)
            
            # Parse type from frontmatter
            fm = parse_frontmatter(f)
            t = fm.get("题型", "其他")
            data[module]["types"][t] = data[module]["types"].get(t, 0) + 1
    
    return data
```

### 周报保存路径

```
E:/obsidian/Obsidian Vault/考公笔记/周报/YYYY-Www_考公周报.md
```

## Phase 4: Suggested Improvement Areas

根据统计数据，自动生成下周建议：

1. **专项突破**：选择错题最多的题型/考点
2. **限时训练建议**：
   - 判断推理 15题限时 20分钟
   - 图形推理 10题限时 10分钟
   - 言语理解 15题限时 16分钟
3. **错题重做**：隔日重做本周错题中的重点题

## Reference

- `references/判断推理复盘流程.md` — 判断推理复盘体系
- `references/言语理解复盘流程.md` — 言语理解复盘体系
- `references/图推复盘流程.md` — 图形推理复盘体系
- `scripts/generate_weekly_report.py` — 周报生成脚本
