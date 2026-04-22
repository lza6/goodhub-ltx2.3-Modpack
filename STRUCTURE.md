# 📁 项目目录结构

```
LTX2.3_v4.0/
│
├── 📖 根目录文件
│   ├── README.md                  # 项目入口（GitHub 主文档）
│   ├── CHANGELOG.md               # 版本更新日志
│   ├── LICENSE                    # MIT 开源协议
│   ├── .gitignore                # Git 忽略规则
│   └── STRUCTURE.md               # 本文件（目录说明）
│
├── 🛠️ tools/                      # 核心工具集
│   ├── activation/               # 激活相关
│   │   ├── bypass_activation.py     # 核心激活脚本
│   │   ├── run_bypass_activation.bat # 一键批处理
│   │   └── README.md                # 激活工具文档
│   │
│   ├── workflow/                 # 工作流工具
│   │   ├── inspect_workflow.py      # 工作流分析器
│   │   ├── convert_workflows.py     # 批量转换（计划中）
│   │   └── README.md                # 工作流工具文档
│   │
│   ├── settings/                 # 设置管理
│   │   ├── fix_settings_persistence.py  # 设置诊断
│   │   ├── auto_save_settings.bat       # 自动保存提醒
│   │   └── README.md                    # 设置工具文档
│   │
│   ├── lora/                     # LoRA 工具
│   │   ├── create_lora_preset_panel.py  # 预设生成器
│   │   ├── lora_preset_inject.js        # 手动注入脚本
│   │   └── README.md                    # LoRA 工具文档
│   │
│   └── README.md                # 工具集总览
│
├── 🎯 scripts/                    # 用户快捷脚本
│   ├── quick_activate.bat       # 一键激活+启动（计划）
│   ├── launch.bat               # 快速启动 ComfyUI
│   └── README.md
│
├── 🎛️ presets/                    # LoRA 预设配置
│   ├── lora_preset.user.js      # Tampermonkey 永久脚本
│   ├── lora_presets.json        # 预设数据（生成）
│   └── README.md
│
├── 📋 workflows/                  # 工作流资源
│   ├── examples/                # 官方示例
│   │   ├── LTX2_3_a2v.json      # 文生视频
│   │   ├── LTX2_3_i2v.json      # 图生视频
│   │   ├── LTX2_3_DZQY.json     # 动作强度
│   │   ├── LTX2_3_SWZ.json      # 手部细节
│   │   └── LTX2_3_t2v.json      # 文本转视频
│   │
│   ├── templates/               # 标准模板（待创建）
│   │   ├── baseline.json        # 纯净基线
│   │   ├── single_lora.json     # 单 LoRA
│   │   ├── dual_lora.json       # 双 LoRA（推荐）
│   │   └── all_loras.json       # 全激活（实验性）
│   │
│   └── README.md                # 工作流文档
│
├── 📚 docs/                       # 完整技术文档
│   ├── README.md                # 文档导航索引
│   ├── ACTIVATION.md            # 激活绕过指南（用户必读）
│   ├── LORA-GUIDE.md            # LoRA 版本管理与使用
│   ├── PRESET-PANEL.md          # 预设面板使用说明
│   ├── SETTINGS.md              # 设置持久化设计方案
│   ├── TROUBLESHOOTING.md       # 常见问题 FAQ
│   ├── ARCHITECTURE.md          # 系统架构概览
│   ├── DEVELOPMENT.md           # 开发者手册
│   │
│   ├── ─── 原始完整版（归档） ───
│   ├── ACTIVATION_BYPASS.md       # 激活技术详解（完整版）
│   ├── SETTINGS_PERSISTENCE.md    # 设置持久化完整设计
│   ├── LORA_MANAGEMENT_GUIDE.md   # LoRA 管理完整版
│   ├── WORKFLOW_CONVERSION_TOOL.md # 工作流转换工具完整手册
│   ├── LORA_PRESET_PANEL_API.md   # 预设面板 API 完整版
│   ├── DEVELOPER_HANDBOOK.md      # 开发者手册完整版
│   ├── PLAN_OVERVIEW.md          # 三层改进计划总览
│   └── CHANGELOG.md              # 版本日志
│
├── ComfyUI/                       # ComfyUI 主程序（保持原位）
│   ├── custom_nodes/
│   │   └── ComfyUI-LTXVideo/     # LTXVideo 节点
│   └── models/
│       ├── loras/                # LoRA 模型存储（用户文件）
│       ├── checkpoints/          # 主模型
│       └── vae/                  # VAE 模型
│
├── 🔧 根目录工具脚本
│   ├── bypass_activation.py          # 原位置（已复制到 tools/）
│   ├── inspect_workflow.py           # 原位置（已复制到 tools/）
│   ├── fix_settings_persistence.py   # 原位置（已复制到 tools/）
│   ├── create_lora_preset_panel.py   # 原位置（已复制到 tools/）
│   ├── lora_preset_inject.js         # 原位置（已复制到 tools/）
│   ├── run_bypass_activation.bat     # 原位置（已复制到 tools/）
│   ├── auto_save_settings.bat        # 原位置（已复制到 tools/）
│   ├── extract_strings.py            # 逆向辅助工具
│   ├── app_decompiled.py             # 反编译代码
│   ├── verify_docs.py               # 文档验证脚本
│   ├── 启动脚本.bat                 # Windows 启动器
│   ├── 清理临时文件.bat             # 清理脚本
│   ├── 使用说明.md                  # 原始中文说明
│   ├── ACTIVATION_BYPASS_INFO.md    # 原始激活分析笔记
│   │
│   ├── LTX2_3_*.json                # 示例工作流（已移到 workflows/examples/）
│   ├── LTX2_3_*.pyd                 # 节点二进制文件
│   ├── app.pyd                      # 主程序（含激活逻辑）
│   ├── core.pyd                     # 核心引擎
│   │
│   └── python_embeded/             # 内嵌 Python 环境
│
└── .github/                        # GitHub 配置（计划）
    └── ISSUE_TEMPLATE/             # Issue 模板（待配置）
```

---

## 📊 文件统计

| 类别 | 数量 | 说明 |
|------|------|------|
| 文档 (.md) | 15 个 | 包括完整版和精简版 |
| Python 脚本 | 6 个 | 激活、工作流、设置、LoRA |
| JavaScript | 2 个 | 注入脚本、油猴脚本 |
| 批处理 (.bat) | 3 个 | Windows 快捷操作 |
| 示例工作流 | 5 个 | 各场景模板 |
| 配置文件 | 4 个 | .gitignore, LICENSE, README, CHANGELOG |

**总计**: 约 35 个核心文件 + ComfyUI 框架 + 模型文件

---

## 🗂️ 设计原则

### 1. 按功能分类

所有工具按用途放入 `tools/` 下的子目录，而非堆在根目录：
- `activation/` - 激活相关
- `workflow/` - 工作流处理
- `settings/` - 设置管理
- `lora/` - LoRA 配置

### 2. 用户文档简化

`docs/` 中提供精简版文档（适合快速阅读），完整版文档以 `_完整版` 或保留原文件名归档：

| 用户文档（推荐先读） | 完整技术版（参考用） |
|--------------------|-------------------|
| `ACTIVATION.md` | `ACTIVATION_BYPASS.md` |
| `LORA-GUIDE.md` | `LORA_MANAGEMENT_GUIDE.md` |
| `PRESET-PANEL.md` | `LORA_PRESET_PANEL_API.md` |
| `SETTINGS.md` | `SETTINGS_PERSISTENCE.md` |

### 3. 向后兼容

- 原始脚本保留在根目录（避免破坏性移动）
- 工具从新位置调用：`tools/activation/bypass_activation.py`
- 旧路径可通过符号链接或文档说明兼容

---

## 🚀 GitHub 推送建议

### 包含的文件

✅ **必须包含**：
- `README.md` - 项目入口
- `LICENSE` - 开源协议
- `.gitignore` - 忽略规则
- `CHANGELOG.md` - 版本日志
- `docs/` - 完整文档集
- `tools/` - 所有工具脚本
- `presets/` - 预设配置
- `workflows/examples/` - 示例工作流

❌ **不要包含**：
- `ComfyUI/models/` - 模型文件过大，用 Git LFS 或单独下载
- `*.pyd` 二进制文件？→ 视情况而定（若为编译产物，可提供源码）
- `__pycache__/`, `*.pyc` - 已忽略
- `.qwen_activation.dat` - 用户本地生成，不提交
- `ComfyUI/logs/`, `ComfyUI/output/` - 运行时文件

---

## 📝 后续优化建议

1. **创建 GitHub 仓库**
   ```bash
   cd D:\LTX2.3_v4.0
   git init
   git add .
   git commit -m "feat: initial commit - LTX2.3 improvement toolkit"
   git remote add origin https://github.com/yourname/LTX2.3-Improvements.git
   git push -u origin main
   ```

2. **配置 GitHub Pages**（可选）
   - 将 `docs/` 目录发布为项目网站
   - 添加 `CNAME` 自定义域名（如需）

3. **添加 Issue 模板**
   - 在 `.github/ISSUE_TEMPLATE/` 创建模板
   - Bug 报告、功能请求、提问模板

4. **设置 GitHub Actions**（可选）
   - 自动运行 `verify_docs.py`
   - 自动检查文档链接有效性

---

*最后更新: 2026-04-22*
