# LTX2.3 改进计划版本更新日志

> 本日志记录所有与改进计划相关的变更。

---

## [未发布] - 计划中

### 新增功能

- **LoRA 预设面板**：Web UI 右下角浮动面板，一键切换 6 种 LoRA 配置
- **激活绕过脚本**：`bypass_activation.py` 本地生成激活文件
- **文档体系**：包含 8 个技术文档，覆盖激活、设置、LoRA 管理等主题
- **工作流诊断工具**：`inspect_workflow.py` 分析 LoRA 版本兼容性

### 待实现（计划阶段）

- 设置持久化系统（全局配置）
- 工作流批量转换工具
- LoRA 智能管理系统
- 性能监控面板

---

## [v1.0] - 2026-04-22

### 初始版本

**首次发布的改进计划文档集**，包含：

| 文档 | 状态 | 说明 |
|-----|------|------|
| `ACTIVATION_BYPASS.md` | ✅ 完成 | 激活机制详解与绕过方案 |
| `SETTINGS_PERSISTENCE.md` | ✅ 完成 | 设置持久化设计方案 |
| `LORA_MANAGEMENT_GUIDE.md` | ✅ 完成 | LoRA 版本管理与兼容性说明 |
| `WORKFLOW_CONVERSION_TOOL.md` | ✅ 完成 | 工作流转换工具使用手册 |
| `LORA_PRESET_PANEL_API.md` | ✅ 完成 | 预设面板 API 与扩展指南 |
| `TROUBLESHOOTING.md` | ✅ 完成 | 常见问题排查（FAQ） |
| `CHANGELOG.md` | ✅ 完成 | 版本更新日志（本文件） |
| `DEVELOPER_HANDBOOK.md` | ⏳ 待创建 | 开发者手册 |

### 已交付脚本

| 脚本 | 用途 | 状态 |
|-----|------|------|
| `bypass_activation.py` | 本地生成激活文件 | ✅ 可用 |
| `inspect_workflow.py` | 工作流结构分析 | ✅ 可用 |
| `fix_settings_persistence.py` | 设置持久化辅助 | ✅ 可用 |
| `create_lora_preset_panel.py` | 预设面板生成器 | ✅ 可用 |
| `lora_preset_inject.js` | 前端注入脚本 | ✅ 可用 |
| `lora_preset.user.js` | 油猴永久脚本 | ✅ 可用 |

---

*文档维护：请按实际开发进度更新本文件。*
