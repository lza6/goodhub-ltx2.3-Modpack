# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-04-22

### Added
- 激活绕过工具 (`scripts/bypass_activation.py`)
- LoRA 预设面板 (`tools/lora/lora_preset_inject.js`)
- 油猴永久脚本 (`presets/lora_preset.user.js`)
- 完整技术文档集 (`docs/`)
- 工作流分析工具 (`tools/workflow/inspect_workflow.py`)

### Documents
- README.md (项目入口)
- ACTIVATION.md (激活指南)
- LORA-GUIDE.md (LoRA使用指南)
- PRESET-PANEL.md (预设面板说明)
- SETTINGS.md (设置持久化设计)
- TROUBLESHOOTING.md (故障排查)
- ARCHITECTURE.md (系统架构)
- DEVELOPMENT.md (开发者手册)

### Directory Structure
```
tools/
├── activation/   # 激活工具
├── workflow/      # 工作流工具
├── settings/      # 设置工具
└── lora/         # LoRA工具
presets/          # 预设配置
workflows/
├── examples/      # 示例工作流
└── templates/    # 模板（待创建）
docs/             # 完整文档集
```

---

*For older releases, see the git history.*