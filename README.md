# Legal Skills

> 面向律师办案的 Claude Skills 集合，将 Claude 从通用 AI 助手转变为专业的法律工作协作者。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/GitHub-cat--xierluo-blue)](https://github.com/cat-xierluo/legal-skills)

## 📋 项目概述

本项目旨在沉淀并分发面向律师办案的 Claude Skills，支持诉讼与非诉场景的 AI 协作。所有技能遵循统一的结构规范，确保可复用、可追溯、可扩展。

### 核心特点

- 🎯 **场景导向**：聚焦法律实务场景（证据整理、文档转换、案件分析等）
- 📦 **独立自包含**：每个技能都是完整的模块，可单独使用或组合使用
- 📝 **文档完善**：每个技能配备决策记录、任务跟踪、变更日志
- 🔒 **安全合规**：遵循数据保护原则，避免泄露客户信息

## 🛠️ 技能列表

### 已发布技能

| 技能 | 说明 | 状态 |
| :--- | :--- | :--- |
| **[mineru-ocr](mineru-ocr/)** | PDF/图片转 Markdown，支持 OCR、表格和公式识别 | ✅ v1.0.1 |
| **[pdf](pdf/)** | PDF 处理工具包：文本提取、表单填写、合并拆分 | ✅ 稳定版 |
| **[skill-creator](skill-creator/)** | 技能创建指南和工具集 | ✅ 工具类 |

### 技能目录说明

| 目录 | 说明 |
| :--- | :--- |
| `test/` | 调试中的技能，测试完成后移至根目录 |
| `dist/` | 技能打包产物，用于分发 |
| `references/` | 共享参考资料 |

## 📁 技能结构规范

每个技能遵循统一的扁平化结构：

```
skill-name/
├── SKILL.md           # 技能定义文件（必填，含 frontmatter）
├── CHANGELOG.md       # 变更日志（必填）
├── DECISIONS.md       # 设计决策记录
├── TASKS.md           # 任务跟踪
├── config/            # 配置文件（按需，如 .env）
│   ├── .env.example   # 配置模板
│   └── .env           # 实际配置（不提交到 git）
├── references/        # 参考资料（按需）
├── scripts/           # 可执行脚本（按需）
├── assets/            # 模板和静态资源（按需）
└── archive/           # 处理结果归档（按需）
```

### SKILL.md 格式

每个技能必须包含 YAML frontmatter：

```yaml
---
name: skill-name
description: 技能描述，说明何时使用此技能
allowed-tools: Read, Write, Bash, Grep
---
```

## 📖 协作规范

本项目遵循 [AGENTS.md](AGENTS.md) 定义的协作规范（v1.1.2）：

- **技能导向**：每个技能独立成树，根目录包含 SKILL.md 和配套文档
- **文档即上下文**：关键决策、任务、变更记录在文档中
- **透明变更**：所有修改写入 CHANGELOG.md，遵循版本号规范
- **保留证据**：输出引用可回溯，缺失信息明确标注

### CHANGELOG 版本号规则

- 测试版本（`test/` 目录）：`0.x.x`
- 正式版本（根目录）：`1.x.x`

## 🚀 快速开始

### 安装技能

1. 将技能目录复制到 Claude Code 的 skills 目录
2. 对于需要配置的技能（如 mineru-ocr），按说明配置 `config/.env`
3. 在对话中直接使用技能功能

### 创建新技能

参考 [skill-creator](skill-creator/) 的指南，或直接使用 Skill Creator 工具。

## 🔗 相关链接

- **仓库地址**：[https://github.com/cat-xierluo/legal-skills](https://github.com/cat-xierluo/legal-skills)
- **协作规范**：[AGENTS.md](AGENTS.md)
- **Claude Code 文档**：[https://code.claude.com](https://code.claude.com)

## 📄 许可证

MIT License

本项目各技能可能采用不同许可证，请参阅各技能目录下的 LICENSE 文件。

---

**最后更新**：2026-01-07
