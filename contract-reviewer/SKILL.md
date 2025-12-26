---
name: contract-reviewer
description: 合同审核与对比分析技能。当用户需要对比客户合同与公司模板、识别高风险条款、添加批注建议、自动填充公司信息并生成最终 DOCX 文件时，应使用此技能。适用于合同审核、条款风险分析、合同信息填充等场景。 (project)
---

# 合同审核与对比分析

## 概述

自动化合同审核流程：对比合同差异、识别风险条款、添加批注建议、填充公司信息。

## 使用前准备

启动时询问用户提供以下文件：

```
请提供以下文件：

1. 【必填】您公司的合同模板：___
2. 【必填】需要审核的客户合同：___
3. 【可选】公司信息文件（用于自动填充）：___
```

## 执行流程

### 1. 风险识别（直接读取 DOCX）

```bash
# 直接分析 DOCX 文件（推荐，无需 pandoc）
python3 "{baseDir}/scripts/analyze_risks.py" "<客户合同.docx>"

# 生成 JSON（用于批注）
python3 "{baseDir}/scripts/analyze_risks.py" "<客户合同.docx>" --json --output /tmp/risks.json
```

### 2. 对比分析（可选，需要 pandoc）

如需对比两份合同的条款差异：

```bash
pandoc "<客户合同.docx>" -o /tmp/customer.md
pandoc "<公司模板.docx>" -o /tmp/template.md
python3 "{baseDir}/scripts/compare_contracts.py" /tmp/customer.md /tmp/template.md
```

### 3. 用户确认

展示风险分析结果，**等待用户确认后**再添加批注。

### 4. 添加批注

```bash
python3 "{docxSkillDir}/ooxml/scripts/unpack.py" "<客户合同.docx>" /tmp/unpacked
PYTHONPATH="{docxSkillDir}" python3 "{baseDir}/scripts/add_comments.py" /tmp/unpacked /tmp/risks.json
python3 "{docxSkillDir}/ooxml/scripts/pack.py" /tmp/unpacked "<输出文件.docx>"
```

### 5. 信息填充（可选）

通过 docx skill 的 Document API 直接修改段落文本：

```python
from scripts.document import Document

doc = Document("/tmp/unpacked", author="合同填充")
doc_xml = doc["word/document.xml"]

# 遍历段落并修改
for para in doc_xml.dom.getElementsByTagName("w:p"):
    text = doc_xml._get_element_text(para)
    if text == "乙方：":
        # 修改段落中的 w:t 元素
        for t in para.getElementsByTagName("w:t"):
            if t.firstChild:
                t.firstChild.data = "乙方：上海千彗科技有限公司"

doc.save()
```

## 风险等级说明

| 等级 | 类型 | 说明 |
|-----|------|-----|
| 高 | 无限责任 | "全部损失"、"任何损失" |
| 高 | 知识产权 | "知识产权转让"、"著作权归...所有" |
| 高 | 单方解约 | "立即解除"、"有权解除" |
| 中 | 管辖权 | "仲裁委员会"、"甲方所在地" |
| 中 | 整改期 | "X个工作日内改正" |
| 中 | 授权范围 | "关联公司"、"独占许可" |
| 低 | 自动续约 | "自动续期"、"默认续约" |

## 脚本说明

| 脚本 | 功能 | 依赖 |
|-----|------|-----|
| `analyze_risks.py` | 风险条款分析（支持 DOCX/MD） | docx skill（DOCX 模式） |
| `compare_contracts.py` | 合同对比 | pandoc |
| `add_comments.py` | 添加批注 | docx skill |

## 参考文档

- `{baseDir}/references/risk_clauses.md` - 风险条款详细说明
- `{baseDir}/references/common_info_template.md` - 公司信息模板
