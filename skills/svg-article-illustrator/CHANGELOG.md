# 更新日志

## [1.0.1] - 2026-02-07

### 改进

- 📝 依赖说明优化：PNG 转换依赖移至 png-export.md 模式文档
- 📝 技能协作：新增与 piclist-upload skill 的配合说明
- 📝 修正调用方式：piclist-upload 改为 skill 调用格式（/piclist-upload @article.md）

---

## [1.0.0] - 2026-02-07

### 新增

- ✨ 整合三个版本的 illustrate 命令（v1.8、v2.0.1、v3.0）为统一 skill
- ✨ 支持三种输出模式：dynamic-svg（默认）、static-svg、png-export
- ✨ 使用 Progressive Disclosure 设计，SKILL.md 保持精简
- ✨ 共享核心设计原则文档（core-principles.md）
- ✨ SMIL 动画代码片段模板（assets/animations.smil）
- ✨ 常用布局模板（assets/layouts.svg）
- ✨ SVG 转 PNG 转换脚本（scripts/svg2png.js）

### 改进

- 📝 模式选择指南：根据用户场景自动选择合适的输出模式
- 📝 默认使用动态 SVG 模式，提供最佳视觉效果
- 📝 PNG 模式支持跨平台兼容性
- 📝 静态 SVG 模式简化工作流程

### 技术细节

- 基于 illustrate3.0 的动态效果和配图密度策略
- 支持公众号原生 SMIL 动画
- 画布尺寸 800x450（16:9 比例）
- 高保真 PNG 转换（600 DPI）
- 文件命名规范（≤15 字符）
