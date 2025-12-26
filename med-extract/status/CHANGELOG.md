# 变更日志

## Unreleased
- 建立文档框架（docs/ 与 status/），为病历信息抽取技能开发铺路。
- 编写并打包 `med-extract` 技能（结构化抽取病历关键诊疗信息，含时间轴与过错线索提示），生成 `med-extract.zip`。
- 重构目录：将技能、docs、status 集中到 `med-extract/` 目录，并在 `dist/` 下产出最新打包文件。
- 技能命名精简为 `med-extract`，并重新打包输出 `dist/med-extract.zip`。
- 扁平化技能目录：`SKILL.md`、`references/` 放置在 `med-extract/` 根；打包输出统一至仓库根的 `dist/`，避免自包含导致包体膨胀。
- 更新抽取重点：强调“就诊人信息 + 诊疗时间顺序 + 每个时间点的具体事件”，并改用 Markdown 时间轴模板输出。
- 示例内容已匿名化，移除真实客户病历文件，重新打包 `dist/med-extract.zip`。
- 新增规划：引入诊疗规范、过错评价、人损评定资料模块，待收集官方材料后落地。
- 添加 `references/guideline_checklist.md`，列出诊疗规范/过错评价/人损评定的收集清单与对照策略占位。
- 完善并移至 references：`references/medical-structure.md`（通用结构/时间轴指引，中文内容、英文文件名），并更新打包。
- 时间轴指引补充：沟通记录（医患/家属）按签署时间放入对应节点，避免顺序错位。
- 调整 `references/sample_medical_record_structure.md`：保留中文内容（英文文件名），强调沟通记录按签署时间插入节点，并重新打包。
- 文件名简化：使用 `medical-structure.md`，内容保持中文。
- 输出格式调整：SKILL 支持一次生成多文档（record-summary.md、fault-analysis.md、legal-actions.md），便于案件处理流程。
- 补充处理：强调非时间顺序存放的沟通/同意/检验报告需按签署/报告时间插入时间轴，并在参考文档中说明。
- 输出文件改为中文命名：`病历概要.md`、`过错初步分析.md`、`律师行动清单.md`。
- 完善 `references/medical-structure.md`：补充住院通知/身份确认/授权委托、手术指征评估、抗感染审批、风险评估表、管理性文书等文档类型与缺口清单。
- 下载并归档首批规范 PDF（糖尿病足感染、腹腔感染、VSD 指南、SSI 标准/指南），并更新 `guideline_checklist.md`。
- 清理含真实个人信息的参考文件（`references/蒋成杰_案情摘要.md`）。
