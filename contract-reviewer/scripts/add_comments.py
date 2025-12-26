#!/usr/bin/env python3
"""
合同批注脚本
为客户合同中的风险条款添加 Word 批注

依赖 docx skill 的 Document 类
使用方法:
    PYTHONPATH=/path/to/docx/skill python add_comments.py <unpacked_dir> <risks_json> [author]
"""
import json
import sys
from pathlib import Path

from scripts.document import Document


def load_risks(risks_file: str) -> list[dict]:
    """加载风险分析结果"""
    with open(risks_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_comment(risk: dict) -> str:
    """格式化批注内容"""
    level = risk.get("risk_level", "风险")
    description = risk.get("description", "")
    suggestion = risk.get("suggestion", "")

    return f"【{level}】{description}\n{suggestion}"


def add_comments_to_document(unpacked_dir: str, risks: list[dict], author: str = "合同审核") -> Document:
    """为文档添加批注"""
    doc = Document(unpacked_dir, author=author, initials="审")

    # 按行号排序，从后往前处理（避免行号变化影响）
    sorted_risks = sorted(risks, key=lambda r: r.get("line_number", 0), reverse=True)

    success_count = 0
    failed_risks = []

    for risk in sorted_risks:
        # 优先使用 context（更完整的上下文），其次使用 matched_text
        search_text = risk.get("context", "").replace("...", "")[:50]  # 取前50字符
        if not search_text:
            search_text = risk.get("matched_text", "")

        if not search_text:
            continue

        try:
            # 尝试在段落级别查找
            node = doc["word/document.xml"].get_node(tag="w:p", contains=search_text)

            if node:
                comment_text = format_comment(risk)
                doc.add_comment(start=node, end=node, text=comment_text)
                success_count += 1
                category = risk.get("category", "未知")
                level = risk.get("risk_level", "")
                print(f"✓ [{level}] {category}")
            else:
                failed_risks.append(risk)

        except Exception as e:
            failed_risks.append(risk)
            if "--verbose" in sys.argv:
                print(f"✗ 添加批注失败: {search_text[:30]}... - {str(e)}")

    print(f"\n批注添加完成: 成功 {success_count} 项, 失败 {len(failed_risks)} 项")

    if failed_risks and "--verbose" in sys.argv:
        print("\n未能添加批注的条款:")
        for risk in failed_risks:
            print(f"  - {risk.get('category')}: {risk.get('matched_text', '')[:30]}...")

    return doc


def main():
    if len(sys.argv) < 3:
        print("用法: PYTHONPATH=/path/to/docx/skill python add_comments.py <unpacked_dir> <risks_json> [author]")
        print("")
        print("参数:")
        print("  unpacked_dir  解包后的文档目录")
        print("  risks_json    风险分析 JSON 文件（由 analyze_risks.py 生成）")
        print("  author        批注作者名称（可选，默认：合同审核）")
        print("  --verbose     显示详细信息")
        print("")
        print("示例:")
        print("  PYTHONPATH=../.claude/skills/docx python add_comments.py ./unpacked risks.json")
        print("  PYTHONPATH=../.claude/skills/docx python add_comments.py ./unpacked risks.json 法务部")
        sys.exit(1)

    unpacked_dir = sys.argv[1]
    risks_file = sys.argv[2]

    # 解析作者参数（跳过 --verbose）
    author = "合同审核"
    for arg in sys.argv[3:]:
        if not arg.startswith("--"):
            author = arg
            break

    # 检查目录和文件
    if not Path(unpacked_dir).is_dir():
        print(f"错误: 目录不存在 - {unpacked_dir}")
        sys.exit(1)

    if not Path(risks_file).is_file():
        print(f"错误: 文件不存在 - {risks_file}")
        sys.exit(1)

    # 加载风险数据
    print(f"加载风险分析结果: {risks_file}")
    risks = load_risks(risks_file)

    high = len([r for r in risks if r.get("risk_level") == "高风险"])
    mid = len([r for r in risks if r.get("risk_level") == "中风险"])
    low = len([r for r in risks if r.get("risk_level") == "低风险"])
    print(f"风险统计: 高风险 {high} | 中风险 {mid} | 低风险 {low}")

    # 添加批注
    print(f"\n开始添加批注（作者: {author}）...")
    doc = add_comments_to_document(unpacked_dir, risks, author)

    # 保存文档
    doc.save()
    print(f"\n文档已保存")


if __name__ == "__main__":
    main()
