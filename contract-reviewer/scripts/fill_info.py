#!/usr/bin/env python3
"""
合同信息填充脚本
根据用户提供的公司信息自动填充合同中的空白字段

依赖 docx skill 的 Document 类
使用方法:
    PYTHONPATH=/path/to/docx/skill python fill_info.py <unpacked_dir> <info_json>
"""
import json
import sys
from pathlib import Path

from scripts.document import Document


def load_info(info_file: str) -> dict:
    """加载公司信息（必须提供文件）"""
    if not info_file:
        raise ValueError("必须提供公司信息文件")

    path = Path(info_file)
    if not path.is_file():
        raise FileNotFoundError(f"公司信息文件不存在: {info_file}")

    with open(info_file, 'r', encoding='utf-8') as f:
        info = json.load(f)

    if not info:
        raise ValueError("公司信息文件为空")

    return info


def set_paragraph_text(para, new_text: str) -> bool:
    """
    设置段落的完整文本
    保留第一个 w:r 的格式，删除其他 w:r 元素

    注意：XML 解析器可能将 w:t 中的文本拆分为多个文本节点，
    所以需要清除所有子节点后重新设置文本。
    """
    runs = list(para.getElementsByTagName("w:r"))
    if not runs:
        return False

    # 找到第一个包含 w:t 的 run
    first_run = None
    first_t = None
    for run in runs:
        t_elems = run.getElementsByTagName("w:t")
        if t_elems:
            first_run = run
            first_t = t_elems[0]
            break

    if not first_run or not first_t:
        return False

    # 清除 w:t 中的所有子节点（可能有多个文本节点）
    while first_t.firstChild:
        first_t.removeChild(first_t.firstChild)

    # 添加新的文本节点
    owner_doc = para.ownerDocument
    text_node = owner_doc.createTextNode(new_text)
    first_t.appendChild(text_node)

    # 删除第一个 run 中其他的 w:t 元素
    t_elems = list(first_run.getElementsByTagName("w:t"))
    for t in t_elems[1:]:
        t.parentNode.removeChild(t)

    # 删除其他所有包含 w:t 的 run（保留不含文本的 run，如书签等）
    for run in runs:
        if run == first_run:
            continue
        t_elems = run.getElementsByTagName("w:t")
        if t_elems:
            run.parentNode.removeChild(run)

    return True


def get_paragraph_text(para, editor) -> str:
    """获取段落的完整文本（去除空白字符）"""
    text = editor._get_element_text(para)
    # 去除所有空白字符，只保留实际文本
    return ''.join(text.split())


def find_and_fill(doc, info: dict, fill_party: str = None) -> int:
    """
    查找并填充信息

    参数:
        doc: Document 对象
        info: 公司信息字典
        fill_party: 填充哪一方的信息，"甲方" 或 "乙方"，None 则自动检测
    """
    filled_count = 0
    editor = doc["word/document.xml"]
    all_paras = list(editor.dom.getElementsByTagName("w:p"))

    # 记录已填充的段落索引
    filled_indices = set()

    # 首先确定我们是甲方还是乙方
    # 通过查找合同中哪一方的信息是空的来判断
    if fill_party is None:
        for i, para in enumerate(all_paras):
            text = get_paragraph_text(para, editor)
            # 如果乙方后面紧跟着住所（说明乙方信息为空），则我方是乙方
            if text == "乙方：":
                next_text = get_paragraph_text(all_paras[i + 1], editor) if i + 1 < len(all_paras) else ""
                if next_text == "住所：":
                    fill_party = "乙方"
                    break
            elif text == "甲方：":
                next_text = get_paragraph_text(all_paras[i + 1], editor) if i + 1 < len(all_paras) else ""
                if next_text == "住所：":
                    fill_party = "甲方"
                    break

    if fill_party:
        print(f"检测到需要填充: {fill_party}")
    else:
        print("无法自动检测填充方，将填充所有空白字段")

    # 状态机：跟踪当前在填充哪一方的信息
    current_party = None  # "甲方" 或 "乙方" 或 None
    in_bank_section = False  # 是否在银行账户信息区域

    for i, para in enumerate(all_paras):
        if i in filled_indices:
            continue

        text = get_paragraph_text(para, editor)

        # 检测当前段落属于哪一方
        if text == "甲方：" or text.startswith("甲方："):
            current_party = "甲方"
        elif text == "乙方：" or text.startswith("乙方："):
            current_party = "乙方"

        # 检测银行账户信息区域（通常在 6.3 节）
        if "收款账户信息" in text or "6.3" in text:
            in_bank_section = True

        # 根据 fill_party 决定是否填充
        should_fill = (fill_party is None) or (current_party == fill_party) or in_bank_section

        if not should_fill and current_party and current_party != fill_party:
            continue

        # 填充规则
        if text == "甲方：" or text == "乙方：":
            if "company_name" in info and info["company_name"]:
                party_label = text  # "甲方：" 或 "乙方："
                new_text = f"{party_label}{info['company_name']}"
                if set_paragraph_text(para, new_text):
                    print(f"✓ 填充: {party_label} -> {info['company_name']}")
                    filled_count += 1
                    filled_indices.add(i)

        elif text == "住所：":
            if "registered_address" in info and info["registered_address"]:
                if set_paragraph_text(para, f"住所：{info['registered_address']}"):
                    print(f"✓ 填充: 住所")
                    filled_count += 1
                    filled_indices.add(i)

        elif "联系人" in text and "电话" in text and len(text) < 20:
            contact = info.get("contact_person", "")
            phone = info.get("contact_phone", "")
            if contact or phone:
                if set_paragraph_text(para, f"联系人：{contact} 电话：{phone}"):
                    print(f"✓ 填充: 联系人和电话")
                    filled_count += 1
                    filled_indices.add(i)

        elif text == "邮箱：":
            if "contact_email" in info and info["contact_email"]:
                if set_paragraph_text(para, f"邮箱：{info['contact_email']}"):
                    print(f"✓ 填充: 邮箱")
                    filled_count += 1
                    filled_indices.add(i)

        elif text == "开户行：":
            if "bank_name" in info and info["bank_name"]:
                if set_paragraph_text(para, f"开户行：{info['bank_name']}"):
                    print(f"✓ 填充: 开户行")
                    filled_count += 1
                    filled_indices.add(i)

        elif text == "开户名：":
            if "account_name" in info and info["account_name"]:
                if set_paragraph_text(para, f"开户名：{info['account_name']}"):
                    print(f"✓ 填充: 开户名")
                    filled_count += 1
                    filled_indices.add(i)

        elif text == "账号：":
            if "bank_account" in info and info["bank_account"]:
                if set_paragraph_text(para, f"账号：{info['bank_account']}"):
                    print(f"✓ 填充: 账号")
                    filled_count += 1
                    filled_indices.add(i)

    return filled_count


def main():
    if len(sys.argv) < 3:
        print("用法: PYTHONPATH=/path/to/docx/skill python fill_info.py <unpacked_dir> <info_json> [party]")
        print("")
        print("参数:")
        print("  unpacked_dir  解包后的文档目录")
        print("  info_json     公司信息 JSON 文件（必填）")
        print("  party         填充哪一方：甲方 或 乙方（可选，自动检测）")
        print("")
        print("JSON 文件格式示例:")
        print('''{
  "company_name": "XX科技有限公司",
  "legal_representative": "张三",
  "registered_address": "XX市XX区XX路XX号",
  "contact_person": "李四",
  "contact_phone": "138XXXXXXXX",
  "contact_email": "contact@example.com",
  "bank_name": "XX银行XX支行",
  "bank_account": "XXXXXXXXXX",
  "account_name": "XX科技有限公司"
}''')
        sys.exit(1)

    unpacked_dir = sys.argv[1]
    info_file = sys.argv[2]
    fill_party = sys.argv[3] if len(sys.argv) > 3 else None

    # 验证 party 参数
    if fill_party and fill_party not in ["甲方", "乙方"]:
        print(f"错误: party 参数必须是 '甲方' 或 '乙方'，而不是 '{fill_party}'")
        sys.exit(1)

    # 检查目录
    if not Path(unpacked_dir).is_dir():
        print(f"错误: 目录不存在 - {unpacked_dir}")
        sys.exit(1)

    # 加载公司信息
    try:
        print(f"加载公司信息: {info_file}")
        info = load_info(info_file)
        print(f"已加载 {len(info)} 个字段")
    except (ValueError, FileNotFoundError) as e:
        print(f"错误: {e}")
        sys.exit(1)

    # 初始化文档
    print(f"\n初始化文档: {unpacked_dir}")
    doc = Document(unpacked_dir)

    # 填充信息
    print("\n开始填充信息...")
    filled_count = find_and_fill(doc, info, fill_party)

    if filled_count == 0:
        print("\n警告: 未找到可填充的字段")
        print("提示: 确保合同中有空白的 '字段名：' 格式的占位符")
    else:
        print(f"\n共填充 {filled_count} 个字段")

    # 保存文档
    doc.save()
    print("文档已保存")


if __name__ == "__main__":
    main()
