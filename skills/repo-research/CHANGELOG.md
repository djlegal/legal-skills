# 变更日志

## [0.4.0] - 2026-02-14

### 新增功能

借鉴 Zread MCP 实现思路，增强本地分析能力：

- **代码语义搜索**: 支持搜索函数、类、导入、文档等多种模式
  - 新增 `scripts/search.py` 模块
  - 支持 Python, JavaScript, TypeScript, Go, Rust, Java
  - 使用 Grep 工具进行模式匹配

- **深度代码分析**: 超越基础分析，提供架构和质量层面的深度洞察
  - 新增 `scripts/analyzer/` 模块
  - **架构分析**: 目录结构、模块划分、入口文件、架构模式检测（MVC、微服务、插件、monorepo）
  - **质量分析**: 代码统计、注释覆盖率、技术债务检测（TODO、FIXME）、问题检测（硬编码密钥、console.log）

- **智能问答**: 利用 Claude Code 的 LLM 能力，回答关于仓库的自然语言问题
  - 新增 `scripts/qa.py` 模块
  - 问题意图分类: overview, architecture, usage, api, dependencies
  - 结构化回答模板

### 改进优化

- 更新 SKILL.md，添加高级功能章节
- 文档完善：详细说明各功能的使用方法和触发条件

### 文件变更

- 新增: `scripts/__init__.py`
- 新增: `scripts/search.py`
- 新增: `scripts/qa.py`
- 新增: `scripts/analyzer/__init__.py`
- 新增: `scripts/analyzer/architecture.py`
- 新增: `scripts/analyzer/quality.py`
- 更新: `SKILL.md`

---

## [0.3.0] - 2026-02-11

### 新增功能

- 主题驱动搜索研究模式：支持用户提供主题关键词，自动使用 find-skills 搜索相关 GitHub 仓库
- 依赖管理章节：说明核心功能无需前置技能，find-skills 仅在主题搜索模式下可选使用
- 新增主题研究报告模板：`assets/topic-research-template.md`

### 改进优化

- 更新模式选择表格，添加主题驱动搜索研究模式（第 4 种模式）
- 完善触发条件说明，包含主题搜索相关触发场景
- 添加主题研究模式的完整工作流程（Step 0-6）：依赖检查、搜索、筛选、克隆、分析、报告

### 文档完善

- 更新 Resources 章节，添加新模板文件引用
- 创建配套文档：DECISIONS.md、TASKS.md、LICENSE.txt
- 记录 3 个重要技术决策：主题搜索模式设计、目录结构设计、报告模板设计原则

---

## [0.2.0] - 2026-02-10

### 新增功能

- 对比启发模式：支持外部仓库与本地项目进行对比分析
- 启发式分析框架：差异分析框架 + 启发式问题清单
- 本地项目识别：自动识别常见本地项目类型（技能目录、测试项目等）

### 改进优化

- 扩展模式选择表格，添加对比启发模式（第 3 种模式）
- 新增多仓库对比报告模板：`assets/comparison-template.md`
- 完善报告结构，添加"对比分析"和"具体启发"章节

### 文档完善

- 添加对比启发模式的完整工作流程（Step 4）
- 定义启发式问题清单：功能、架构、实现、文档 4 个维度

---

## [0.1.0] - 2026-02-09

### 新增功能

- 基础研究框架：支持单个和多个 GitHub 仓库的深度研究
- 两种研究模式：
  - 单仓库深度研究：全面分析单个仓库的架构、功能、代码质量
  - 多仓库对比研究：对比多个仓库的共性、差异、优劣
- 基础分析流程：项目类型识别、核心文件阅读、项目结构分析、技术栈识别
- 单仓库报告模板：`assets/report-template.md`

### 功能特性

- 智能克隆：使用 `--depth 1` 浅克隆，节省时间和空间
- 目录结构设计：`research/YYYYMMDD/{repo-name|comparison}/` 模式化组织
- 项目类型识别：自动识别 Node.js、Python、Go、Rust、Claude Skill 等项目类型

### 文档完善

- 定义技能触发条件和使用场景
- 编写完整工作流程文档（Step 1-5）
- 创建报告模板和会话汇报格式
