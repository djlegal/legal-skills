#!/usr/bin/env python3
"""
合同风险条款分析脚本
分析客户合同中的高风险条款，输出风险报告

支持直接读取 DOCX 文件（通过 docx skill）或 Markdown 文件

使用方法:
    # 直接分析 DOCX 文件（推荐）
    PYTHONPATH=/path/to/docx/skill python analyze_risks.py <contract.docx> [--json] [--output <file>]

    # 分析 Markdown 文件（兼容旧方式）
    python analyze_risks.py <contract.md> [--json] [--output <file>]
"""
import json
import re
import sys
from pathlib import Path

# 高风险条款配置（包含关键词、风险说明和修改建议）
RISK_CONFIG = {
    "高风险": {
        "无限责任": {
            "patterns": [
                r"全部损失",
                r"任何损失",
                r"一切损失",
                r"所有损失",
                r"无上限",
                r"全额退还.*已支付.*全部费用",
                r"赔偿.*遭受的全部损失",
            ],
            "description": "此条款要求承担无限责任",
            "suggestion": "建议修改为：设置责任上限（如合同金额的100%），排除间接损失和预期利润损失。"
        },
        "知识产权风险": {
            "patterns": [
                r"知识产权.*转让",
                r"著作权.*归.*所有",
                r"放弃.*权利",
                r"全部.*归.*方所有",
            ],
            "description": "此条款涉及知识产权归属或转让",
            "suggestion": "建议修改为：明确区分软件产品与定制开发的知识产权，保留核心技术的知识产权。"
        },
        "单方解约": {
            "patterns": [
                r"立即解除本合同",
                r"有权.*解除本合同",
                r"单方.*终止",
            ],
            "description": "此条款允许单方解约",
            "suggestion": "建议修改为：明确解约条件和程序，设置合理的整改期（如15个工作日）。"
        },
    },
    "中风险": {
        "管辖权不利": {
            "patterns": [
                r"仲裁委员会",
                r"甲方所在地",
                r"对方所在地.*法院",
            ],
            "description": "此条款约定仲裁或对方所在地管辖",
            "suggestion": "建议修改为：约定我方所在地人民法院管辖。"
        },
        "整改期过短": {
            "patterns": [
                r"(\d+)个工作日内.*改正",
                r"逾期达到(\d+)个工作日.*解除",
            ],
            "description": "整改期限可能过短",
            "suggestion": "建议修改为：延长至7-15个工作日。"
        },
        "授权范围扩大": {
            "patterns": [
                r"关联公司",
                r"独占.*许可",
                r"排他.*许可",
            ],
            "description": "授权范围可能过大",
            "suggestion": "建议修改为：限定为单一法人实体，关联公司使用需另行授权；使用普通许可而非独占/排他许可。"
        },
        "退款条款": {
            "patterns": [
                r"退还.*未使用.*款项",
                r"未使用款项.*退还",
            ],
            "description": "退款条款可能对我方不利",
            "suggestion": "建议修改为：明确退款条件，区分一次性费用（不退）和服务费（按期退）的退款规则。"
        },
    },
    "低风险": {
        "自动续约": {
            "patterns": [
                r"自动续期",
                r"默认续约",
                r"自动延长",
            ],
            "description": "包含自动续约条款",
            "suggestion": "建议关注：确认续约条件和取消通知期限。"
        },
        "保密期限": {
            "patterns": [
                r"保密.*持续有效",
                r"保密义务.*终止后",
            ],
            "description": "保密期限可能未明确",
            "suggestion": "建议修改为：明确保密期限为合同终止后2-3年。"
        },
    },
}


def extract_text_from_docx(docx_path: str) -> list[dict]:
    """从 DOCX 文件中直接提取段落和条款（通过 docx skill）"""
    import subprocess
    import tempfile

    # 解包 DOCX
    with tempfile.TemporaryDirectory() as tmpdir:
        unpack_script = Path(__file__).parent.parent.parent / "docx" / "ooxml" / "scripts" / "unpack.py"
        subprocess.run(
            ["python3", str(unpack_script), docx_path, tmpdir],
            capture_output=True, check=True
        )

        # 使用 XMLEditor 读取段落
        sys.path.insert(0, str(Path(__file__).parent.parent.parent / "docx"))
        from scripts.utilities import XMLEditor

        editor = XMLEditor(Path(tmpdir) / "word" / "document.xml")

        paragraphs = []
        current_section = ""
        current_clause = ""

        for i, para in enumerate(editor.dom.getElementsByTagName("w:p")):
            text = editor._get_element_text(para).strip()
            if not text:
                continue

            # 检测章节标题（支持多种格式）
            if re.match(r'^第[一二三四五六七八九十\d]+条', text):
                current_section = text
            elif re.match(r'^[一二三四五六七八九十]+[、.]', text):
                current_section = text
            elif re.match(r'^\*{0,2}第[一二三四五六七八九十\d]+条', text):
                current_section = text.replace('**', '')

            # 检测条款编号
            clause_match = re.match(r'^(\d+[\.\d]*)', text)
            if clause_match:
                current_clause = clause_match.group(1)

            paragraphs.append({
                "para_index": i,
                "section": current_section,
                "clause": current_clause,
                "text": text,
            })

        return paragraphs


def extract_text_from_markdown(md_content: str) -> list[dict]:
    """从 markdown 内容中提取段落和条款（兼容旧方式）"""
    paragraphs = []
    lines = md_content.split('\n')
    current_section = ""
    current_clause = ""

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        # 检测章节标题
        if line.startswith('**第') and '条' in line:
            current_section = line.replace('**', '')
        elif re.match(r'^第[一二三四五六七八九十\d]+条', line):
            current_section = line
        elif re.match(r'^\d+\.\d+', line):
            current_clause = line[:10]

        paragraphs.append({
            "line_number": i + 1,
            "section": current_section,
            "clause": current_clause,
            "text": line,
        })

    return paragraphs


def analyze_risks(paragraphs: list[dict]) -> list[dict]:
    """分析段落中的风险条款"""
    risks = []

    for para in paragraphs:
        text = para["text"]

        for risk_level, categories in RISK_CONFIG.items():
            for category, config in categories.items():
                for pattern in config["patterns"]:
                    match = re.search(pattern, text)
                    if match:
                        risk_item = {
                            "risk_level": risk_level,
                            "category": category,
                            "matched_text": match.group(0),
                            "context": text[:200] + "..." if len(text) > 200 else text,
                            "section": para["section"],
                            "clause": para["clause"],
                            "description": config["description"],
                            "suggestion": config["suggestion"],
                        }
                        # 根据来源添加位置信息
                        if "para_index" in para:
                            risk_item["para_index"] = para["para_index"]
                        if "line_number" in para:
                            risk_item["line_number"] = para["line_number"]
                        risks.append(risk_item)
                        break  # 同一段落同一类别只记录一次

    return risks


def generate_report(risks: list[dict], output_format: str = "text") -> str:
    """生成风险报告"""
    if output_format == "json":
        return json.dumps(risks, ensure_ascii=False, indent=2)

    # 文本格式报告
    report = []
    report.append("=" * 60)
    report.append("合同风险条款分析报告")
    report.append("=" * 60)
    report.append("")

    # 统计
    high_count = len([r for r in risks if r["risk_level"] == "高风险"])
    mid_count = len([r for r in risks if r["risk_level"] == "中风险"])
    low_count = len([r for r in risks if r["risk_level"] == "低风险"])

    report.append(f"风险统计：高风险 {high_count} 项 | 中风险 {mid_count} 项 | 低风险 {low_count} 项")
    report.append("")

    # 按风险等级分组输出
    for level in ["高风险", "中风险", "低风险"]:
        level_risks = [r for r in risks if r["risk_level"] == level]
        if level_risks:
            report.append(f"\n{'='*20} {level} {'='*20}")
            for i, risk in enumerate(level_risks, 1):
                report.append(f"\n[{i}] {risk['category']}")
                report.append(f"    位置: {risk['section']} {risk['clause']}")
                report.append(f"    匹配: {risk['matched_text']}")
                report.append(f"    说明: {risk['description']}")
                report.append(f"    建议: {risk['suggestion']}")

    return "\n".join(report)


def main():
    if len(sys.argv) < 2:
        print("用法: python analyze_risks.py <contract_file> [--json] [--output <output_file>]")
        print("")
        print("参数:")
        print("  contract_file  合同文件（支持 .docx 或 .md 格式）")
        print("  --json         输出 JSON 格式（用于批注脚本）")
        print("  --output FILE  保存报告到文件")
        print("")
        print("示例:")
        print("  python analyze_risks.py contract.docx                    # 直接分析 DOCX（推荐）")
        print("  python analyze_risks.py contract.docx --json --output risks.json")
        print("  python analyze_risks.py contract.md                      # 兼容 Markdown")
        sys.exit(1)

    input_file = sys.argv[1]
    output_format = "json" if "--json" in sys.argv else "text"

    # 检查文件
    input_path = Path(input_file)
    if not input_path.is_file():
        print(f"错误: 文件不存在 - {input_file}")
        sys.exit(1)

    # 根据文件类型选择解析方式
    if input_path.suffix.lower() == '.docx':
        print(f"直接读取 DOCX 文件: {input_file}")
        paragraphs = extract_text_from_docx(input_file)
    else:
        # 兼容 Markdown 文件
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        paragraphs = extract_text_from_markdown(content)

    # 分析风险
    risks = analyze_risks(paragraphs)

    # 生成报告
    report = generate_report(risks, output_format)

    # 输出
    if "--output" in sys.argv:
        output_idx = sys.argv.index("--output")
        output_file = sys.argv[output_idx + 1]
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"报告已保存至: {output_file}")
    else:
        print(report)

    # 返回统计信息
    if output_format != "json":
        high_count = len([r for r in risks if r["risk_level"] == "高风险"])
        mid_count = len([r for r in risks if r["risk_level"] == "中风险"])
        low_count = len([r for r in risks if r["risk_level"] == "低风险"])
        print(f"\n共发现 {len(risks)} 个风险条款")


if __name__ == "__main__":
    main()
