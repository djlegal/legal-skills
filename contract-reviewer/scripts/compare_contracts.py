#!/usr/bin/env python3
"""
合同对比分析脚本
对比客户合同与公司模板，生成差异报告

使用方法:
    python compare_contracts.py <customer_md> <template_md> [--output <report_file>]
"""
import json
import re
import sys
from pathlib import Path
from difflib import SequenceMatcher


def extract_clauses(md_content: str) -> dict:
    """从 markdown 中提取条款"""
    clauses = {}
    current_section = ""
    current_clause_num = ""
    current_text = []

    lines = md_content.split('\n')

    for line in lines:
        line = line.strip()

        # 检测章节标题 (如 "第一条 定义")
        section_match = re.match(r'\*?\*?第([一二三四五六七八九十]+)条\s*(.+?)\*?\*?$', line)
        if section_match:
            # 保存上一个条款
            if current_clause_num and current_text:
                clauses[current_clause_num] = {
                    "section": current_section,
                    "text": '\n'.join(current_text)
                }

            current_section = f"第{section_match.group(1)}条 {section_match.group(2)}"
            current_clause_num = current_section
            current_text = []
            continue

        # 检测子条款 (如 "1.1", "2.3")
        sub_match = re.match(r'^(\d+\.\d+)\s*(.+)', line)
        if sub_match:
            # 保存上一个子条款
            if current_clause_num and current_text:
                clauses[current_clause_num] = {
                    "section": current_section,
                    "text": '\n'.join(current_text)
                }

            current_clause_num = sub_match.group(1)
            current_text = [sub_match.group(2)]
            continue

        # 普通文本行
        if line and current_clause_num:
            current_text.append(line)

    # 保存最后一个条款
    if current_clause_num and current_text:
        clauses[current_clause_num] = {
            "section": current_section,
            "text": '\n'.join(current_text)
        }

    return clauses


def compare_clauses(customer_clauses: dict, template_clauses: dict) -> dict:
    """对比两份合同的条款"""
    comparison = {
        "only_in_customer": [],    # 仅在客户合同中
        "only_in_template": [],    # 仅在模板中
        "different": [],           # 存在差异
        "similar": [],             # 基本相同
    }

    # 找出仅在客户合同中的条款
    for clause_num in customer_clauses:
        if clause_num not in template_clauses:
            comparison["only_in_customer"].append({
                "clause": clause_num,
                "section": customer_clauses[clause_num]["section"],
                "text": customer_clauses[clause_num]["text"][:200]
            })

    # 找出仅在模板中的条款
    for clause_num in template_clauses:
        if clause_num not in customer_clauses:
            comparison["only_in_template"].append({
                "clause": clause_num,
                "section": template_clauses[clause_num]["section"],
                "text": template_clauses[clause_num]["text"][:200]
            })

    # 对比共同条款
    common_clauses = set(customer_clauses.keys()) & set(template_clauses.keys())
    for clause_num in common_clauses:
        customer_text = customer_clauses[clause_num]["text"]
        template_text = template_clauses[clause_num]["text"]

        similarity = SequenceMatcher(None, customer_text, template_text).ratio()

        if similarity >= 0.9:
            comparison["similar"].append({
                "clause": clause_num,
                "similarity": f"{similarity*100:.1f}%"
            })
        else:
            comparison["different"].append({
                "clause": clause_num,
                "section": customer_clauses[clause_num]["section"],
                "similarity": f"{similarity*100:.1f}%",
                "customer_text": customer_text[:300],
                "template_text": template_text[:300],
            })

    return comparison


def generate_comparison_report(comparison: dict) -> str:
    """生成对比报告"""
    report = []
    report.append("=" * 60)
    report.append("合同对比分析报告")
    report.append("=" * 60)
    report.append("")

    # 统计
    report.append("【对比统计】")
    report.append(f"  仅在客户合同中的条款: {len(comparison['only_in_customer'])} 项")
    report.append(f"  仅在公司模板中的条款: {len(comparison['only_in_template'])} 项")
    report.append(f"  存在差异的条款: {len(comparison['different'])} 项")
    report.append(f"  基本相同的条款: {len(comparison['similar'])} 项")
    report.append("")

    # 仅在客户合同中的条款
    if comparison["only_in_customer"]:
        report.append("\n" + "=" * 20 + " 仅在客户合同中 " + "=" * 20)
        report.append("【注意】这些条款在公司模板中没有，需要仔细审查")
        for item in comparison["only_in_customer"]:
            report.append(f"\n  [{item['clause']}] {item['section']}")
            report.append(f"  内容: {item['text'][:100]}...")

    # 存在差异的条款
    if comparison["different"]:
        report.append("\n" + "=" * 20 + " 条款差异 " + "=" * 20)
        for item in comparison["different"]:
            report.append(f"\n  [{item['clause']}] 相似度: {item['similarity']}")
            report.append(f"  客户版本: {item['customer_text'][:150]}...")
            report.append(f"  模板版本: {item['template_text'][:150]}...")

    # 仅在模板中的条款
    if comparison["only_in_template"]:
        report.append("\n" + "=" * 20 + " 仅在公司模板中 " + "=" * 20)
        report.append("【建议】考虑在客户合同中增加这些条款")
        for item in comparison["only_in_template"]:
            report.append(f"\n  [{item['clause']}] {item['section']}")
            report.append(f"  内容: {item['text'][:100]}...")

    return "\n".join(report)


def main():
    if len(sys.argv) < 3:
        print("用法: python compare_contracts.py <customer_md> <template_md> [--output <report_file>] [--json]")
        print("示例: python compare_contracts.py customer.md template.md --output comparison.txt")
        sys.exit(1)

    customer_file = sys.argv[1]
    template_file = sys.argv[2]
    output_json = "--json" in sys.argv

    # 读取文件
    with open(customer_file, 'r', encoding='utf-8') as f:
        customer_content = f.read()
    with open(template_file, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # 提取条款
    print("提取客户合同条款...")
    customer_clauses = extract_clauses(customer_content)
    print(f"  共提取 {len(customer_clauses)} 个条款")

    print("提取模板合同条款...")
    template_clauses = extract_clauses(template_content)
    print(f"  共提取 {len(template_clauses)} 个条款")

    # 对比
    print("\n对比条款...")
    comparison = compare_clauses(customer_clauses, template_clauses)

    # 生成报告
    if output_json:
        report = json.dumps(comparison, ensure_ascii=False, indent=2)
    else:
        report = generate_comparison_report(comparison)

    # 输出
    if "--output" in sys.argv:
        output_idx = sys.argv.index("--output")
        output_file = sys.argv[output_idx + 1]
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n报告已保存至: {output_file}")
    else:
        print("\n" + report)


if __name__ == "__main__":
    main()
