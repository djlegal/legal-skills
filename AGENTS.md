# AGENTS.md - 法律技能项目协作指南

本项目旨在沉淀并分发面向律师办案的 Claude Skills，支持诉讼与非诉场景的 AI 协作。请所有 AI 代理遵循以下约定，确保技能可复用、可追溯、可扩展。

## 核心原则
- **技能导向**：每个技能独立成树（例：`med-extract/`），根目录直接包含 `SKILL.md`、`references/` 等资源，配套 `docs/`、`status/`，打包产物存放在技能目录之外的 `dist/`（避免自包含）。
- **文档即上下文**：关键决策、路线、任务、变更、日志必须记录在各技能目录下的 `docs/` 与 `status/`。
- **透明变更**：任何对用户或协作者有影响的修改都要写入 `status/CHANGELOG.md`，重要决策写入 `docs/DECISIONS.md`。
- **保留证据**：输出引用需可回溯到来源文件；缺失信息明确标注“未提及/待补充”，避免臆测。
- **中文沟通**：默认以中文回复。

## 目录约定（每个技能项目）
- 根目录：`SKILL.md`（必填，含 frontmatter），`references/`、`scripts/`、`assets/`（按需），原始材料（如示例病历）。
- `docs/`：路线图、决策（`ROADMAP.md`、`DECISIONS.md`）。
- `status/`：任务、变更、日志（`TASKS.md`、`CHANGELOG.md`、`JOURNAL.md`）。
- 打包产物：放在技能目录之外的 `dist/`（同级目录），避免将 zip 自身打进包。

## 文件夹存放规范（主项目）
- 每个技能一个顶层目录（如 `med-extract/`），目录名与技能 name 保持一致。
- 技能目录内仅放该技能相关文件；共享脚本放在主项目 `skills/` 下（如 `skills/skill-creator/`）。
- 打包输出统一放在主项目根的 `dist/`，不得放在技能目录内。
- 示例/原始材料与技能同级放置，命名清晰，避免混入其他技能资料。

## 标准作业流程（每个技能）
1) **选择目标**：阅读 `status/TASKS.md`，选择首个未完成目标作为当前任务。若无目标，补充并认领。
2) **分析与计划**：理解目标输出与验收标准；必要时内部规划步骤。
3) **执行与决策记录**：
   - 代码/文档修改同步在对应技能目录下完成。
   - 涉及重要取舍或涌现任务，写入 `docs/DECISIONS.md`（说明背景、方案、理由）。
4) **更新文档**：
   - 变更：`status/CHANGELOG.md` 按类别记录。
   - 任务：完成项在 `status/TASKS.md` 勾选，新增子任务时及时登记。
   - 路线：若里程碑完成，更新 `docs/ROADMAP.md`。
5) **工作日志**：在 `status/JOURNAL.md` 顶部追加日志，格式：
   ```
   **YYYY-MM-DD HH:MM (AI Agent Name - 如 CodeX)**
   - **目标:** ...
   - **操作:** ...
   - **结果:** ...
   - **下一步:** ...
   ```
6) **打包与校验**：使用 `python3 skills/skill-creator/scripts/package_skill.py <技能目录> dist`；确保输出目录不在技能目录内，避免自包含。zip 文件名与 skill name 一致。

## 写作与输出要求
- SKILL.md 使用祈使/不定式语气，明确何时触发、如何操作。
- 引用具体文件请使用相对路径（示例：`med-extract/SKILL.md`），避免粘贴大段内容。
- 发现矛盾或缺失要显式提示（如“缺少出院时间，需补充”）。

## 多技能协作
- 新增技能：使用 `skills/skill-creator/scripts/init_skill.py <name> --path <目标目录>` 初始化后，按上述目录约定重构并补齐 docs/status。
- 避免跨技能污染：只修改当前技能树内文件，除非明确需要共享资源。
- 分发：总是以 `dist/<skill-name>.zip` 为交付物，并在 changelog 中记录版本。

## 安全与合规
- 避免编造事实；无法确认的信息标记“未提及/待补充”。
- 如处理未脱敏材料，提醒用户审查隐私与合规。
- 不执行破坏性命令（如 `git reset --hard`），保持用户未提交的更改。

遵循以上约定，确保法律技能在不同 IDE/CLI（含 Claude Code）中可被可靠触发与复用。***
