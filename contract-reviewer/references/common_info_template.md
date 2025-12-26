# 公司信息模板

使用合同审核 Skill 时，可以提供公司常用信息用于自动填充合同。

## 信息格式

可以通过以下方式提供公司信息：

### 方式一：提供 .docx 文件

创建一个 Word 文档，包含以下信息（格式不限，只要包含关键信息即可）：

```
公司名称：[您的公司名称]
法定代表人：[姓名]
注册地址：[详细地址]
办公地址：[详细地址]（如与注册地址相同可省略）

联系人信息：
  姓名：[联系人姓名]
  电话：[联系电话]
  邮箱：[电子邮箱]

银行账户信息：
  开户行：[银行名称]
  账号：[银行账号]
  户名：[账户名称]
```

### 方式二：直接告诉 Claude

在对话中直接提供信息，例如：

```
公司信息：
- 公司名称：XX科技有限公司
- 法定代表人：张三
- 地址：上海市XX区XX路XX号
- 联系人：李四，电话 138XXXXXXXX
- 开户行：XX银行XX支行，账号：XXXXXXXXX
```

### 方式三：提供 JSON 文件

创建 `company_info.json` 文件：

```json
{
  "company_name": "XX科技有限公司",
  "legal_representative": "张三",
  "registered_address": "上海市XX区XX路XX号",
  "office_address": "上海市XX区XX路XX号",
  "contact_person": "李四",
  "contact_phone": "138XXXXXXXX",
  "contact_email": "contact@example.com",
  "bank_name": "XX银行XX支行",
  "bank_account": "XXXXXXXXXXXXXXXXX",
  "account_name": "XX科技有限公司"
}
```

## 支持填充的字段

| 字段类型 | 字段名称 | 说明 |
|---------|---------|------|
| 公司基本信息 | company_name | 公司全称 |
| | legal_representative | 法定代表人姓名 |
| | registered_address | 注册地址 |
| | office_address | 办公地址 |
| 联系人信息 | contact_person | 联系人姓名 |
| | contact_phone | 联系电话 |
| | contact_email | 电子邮箱 |
| 银行信息 | bank_name | 开户银行 |
| | bank_account | 银行账号 |
| | account_name | 账户名称 |

## 合同中的占位符识别

系统会自动识别合同中的以下占位符并尝试填充：

- `[乙方公司名称]`、`[公司名称]` → 公司名称
- `[法定代表人]` → 法定代表人
- `[地址]`、`[注册地址]` → 地址
- `[联系人]` → 联系人
- `[电话]`、`[联系电话]` → 电话
- `[邮箱]` → 邮箱
- `[开户行]` → 开户行
- `[账号]` → 银行账号
- 以 `：` 或 `:` 结尾的空白行也会尝试匹配填充
