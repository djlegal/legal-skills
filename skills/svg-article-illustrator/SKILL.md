---
name: svg-article-illustrator
description: AI驱动的SVG文章配图生成工具，支持动态SVG、静态SVG和PNG导出三种输出模式。专为公众号文章等需要丰富视觉内容的平台设计，使用SMIL动画实现动态效果，支持SVG直接嵌入Markdown或高保真PNG导出。当用户需要为文章生成配图、创建SVG插图、将SVG转换为PNG，或提到"为文章配图"、"生成插图"、"illustrate"时使用此技能。
---

# SVG Article Illustrator

AI 驱动的文章配图生成工具，使用 SVG 技术为公众号文章生成高质量配图。

## 快速开始

```
/svg-article-illustrator @path/to/article.md
```

## 依赖说明

- **dynamic-svg / static-svg 模式**：无需安装任何依赖
- **png-export 模式**：需要安装 Node.js 和 puppeteer，详见 [references/png-export.md](references/png-export.md#依赖)

---

## 选择输出模式

根据用户需求和发布平台选择合适的输出模式：

| 用户场景 | 使用模式 | 加载参考文件 |
|---------|---------|-------------|
| 默认/未指定 | **dynamic-svg** | references/dynamic-svg.md |
| 需要动画效果 | **dynamic-svg** | references/dynamic-svg.md |
| 需要 PNG 兼容性 | **png-export** | references/png-export.md |
| 不知道如何使用 SVG | **png-export** | references/png-export.md |
| 明确要求静态效果 | **static-svg** | references/static-svg.md |
| 需要静态 SVG 代码 | **static-svg** | references/static-svg.md |

**默认模式**：当用户未明确指定时，使用 **dynamic-svg** 模式。

---

## 核心工作流程

### 第一阶段：内容分析

1. 读取源文章 Markdown 文件
2. 识别核心概念和关键信息点
3. 确定配图位置（目标 10-15 张配图）
   - 每个二级标题（##）后至少 1 张图
   - 每 2-3 个重要段落 1 张图
   - 重要概念转折点额外配图

### 第二阶段：设计 SVG

1. 根据选择的输出模式应用相应规范
   - **dynamic-svg**：添加 SMIL 动画效果
   - **static-svg**：生成静态 SVG 代码
   - **png-export**：生成 SVG 文件
2. 遵循共享设计原则：[references/core-principles.md](references/core-principles.md)

### 第三阶段：输出

- **dynamic-svg**：将 SVG 代码直接嵌入 Markdown 文件
- **static-svg**：将 SVG 代码直接嵌入 Markdown 文件
- **png-export**：
  1. 保存 SVG 文件到源文章目录
  2. 使用 `scripts/svg2png.js` 转换为 PNG
  3. 在 Markdown 中插入图片引用

---

## 共享设计原则

所有输出模式都遵循相同的核心设计原则，详见：[references/core-principles.md](references/core-principles.md)

核心要点：
- 概念聚焦：每张图只表达 1-2 个核心概念
- 极简设计：浅色主题，大图形，少文字
- 画布尺寸：800x450（16:9 比例）
- 边界控制：所有元素在有效区域内（60px 安全边距）

---

## 模式特定规范

### Dynamic SVG 模式

**默认模式**，支持 SMIL 动画效果。

详见：[references/dynamic-svg.md](references/dynamic-svg.md)

核心特性：
- SMIL 动画：浮动、虚线流动、箭头绘制
- Emoji 动画：浮动、脉冲效果
- 逻辑性动画优先：箭头和虚线框必须有动画
- SVG 代码直接嵌入 Markdown

### Static SVG 模式

静态 SVG 代码直接嵌入 Markdown。

详见：[references/static-svg.md](references/static-svg.md)

核心特性：
- 无动画效果
- SVG 代码直接嵌入 Markdown
- 公众号完美支持

### PNG Export 模式

生成独立的 SVG 和 PNG 文件。

详见：[references/png-export.md](references/png-export.md)

核心特性：
- 文件命名：短名-序号.svg（≤15 字符）
- 保存位置：与源文章同目录
- PNG 转换：使用 `scripts/svg2png.js`
- 跨平台兼容性最佳

---

## PNG 转换脚本

使用 `scripts/svg2png.js` 进行高保真转换：

```bash
node scripts/svg2png.js input.svg [output.png] [dpi]
```

- **默认 DPI**：600
- **支持**：emoji、中文、CSS
- **输出位置**：总是生成到 SVG 源文件所在目录

---

## 成功标准

- 配图密度 10-15 张，有效增强视觉吸引力
- 每张配图概念聚焦准确
- 极简风格贯穿始终
- 公众号显示正常
- 跨平台兼容性良好
