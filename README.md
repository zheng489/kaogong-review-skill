# 考公复盘 Skill — Hermes Agent Skill Set

公务员考试（行测）结构化复盘体系 — 基于薛睿判断推理、郭熙言语理解、刘义恒图形推理课程体系。

包含四个独立 skill，每个负责一个复盘流程，可单独加载或组合使用。

## Skills included

| Skill | Directory | Description |
|-------|-----------|-------------|
| 判断推理复盘 | `skills/panduan-tuili-review/` | 论证推理/形式逻辑/分析推理/类比推理错题复盘 |
| 言语理解复盘 | `skills/yanyu-lijie-review/` | 片段阅读/语句表达/逻辑填空错题复盘 |
| 图形推理复盘 | `skills/tutu-review/` | 位置/样式/属性/数量/空间重构错题复盘，含特征信号速查表 |
| 周报自动生成 | `skills/weekly-report/` | 自动汇总周错题数据，生成结构化周报 |

## Prerequisites

- Hermes Agent
- Obsidian vault containing 考公笔记 at `E:/obsidian/Obsidian Vault/考公笔记/`
- The three review process templates pre-loaded (see `references/`)

## Installation

Clone this repo and symlink the skills you need:

```bash
cd ~/.hermes/profiles/default/skills/
git clone https://github.com/郑zzzzzlh/kaogong-review-skill.git kaogong-review
```

## Obsidian Vault Structure

```
考公笔记/
├── 行测/
│   ├── 复盘/
│   │   ├── 判断推理复盘流程.md
│   │   ├── 言语理解复盘流程.md
│   │   ├── 图推复盘流程.md
│   │   └── YYYYMMDD_*错题复盘.md      ← 每日/组复盘汇总
│   ├── 错题汇总/
│   │   ├── 判断推理/
│   │   ├── 言语理解/
│   │   └── 图形推理/
│   │       ├── 位置规律/
│   │       ├── 属性规律/
│   │       ├── 数量规律/
│   │       └── imgs/YYYY-MM-DD/       ← 图推截图
│   └── …
├── 周报/
│   └── YYYY-Www_考公周报.md
└── …
```

## License

MIT
