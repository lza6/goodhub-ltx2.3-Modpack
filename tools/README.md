# 工具箱

本目录包含 LTX2.3 改进项目的所有工具脚本，按功能分类组织。

---

## 📁 目录结构

```
tools/
├── activation/    # 激活相关工具
├── workflow/      # 工作流处理工具
├── settings/      # 设置管理工具
├── lora/          # LoRA相关工具
└── README.md      # 本文件
```

---

## 🔧 工具列表

### 激活工具 (`activation/`)

| 脚本 | 说明 |
|------|------|
| `bypass_activation.py` | 核心激活脚本：调用 app.pyd API 生成本地激活文件 |
| `run_bypass_activation.bat` | Windows 一键批处理，双击执行激活 |

**使用**：
```bash
cd tools/activation
python bypass_activation.py
```

---

### 工作流工具 (`workflow/`)

| 脚本 | 说明 | 状态 |
|------|------|------|
| `inspect_workflow.py` | 分析工作流 JSON 结构，显示 LoRA 配置 | ✅ 可用 |
| `convert_workflows.py` | 批量转换旧工作流中的 LoRA 文件名 | ⏳ 开发中 |

**使用示例**：
```bash
# 分析单个工作流
python tools/workflow/inspect_workflow.py ../workflows/examples/LTX2_3_a2v.json

# 批量转换（待实现）
python tools/workflow/convert_workflows.py ../workflows/*.json
```

---

### 设置工具 (`settings/`)

| 脚本 | 说明 |
|------|------|
| `fix_settings_persistence.py` | 设置持久化诊断与修复辅助 |
| `auto_save_settings.bat` | 定时提醒保存工作流（每5分钟） |

---

### LoRA 工具 (`lora/`)

| 脚本 | 说明 |
|------|------|
| `create_lora_preset_panel.py` | 生成 LoRA 预设面板的 Python 脚本 |
| `lora_preset_inject.js` | 浏览器控制台手动注入脚本 |

---

## 🎯 快速使用指南

### 首次激活

**推荐步骤**：
1. 打开命令行，进入项目根目录
2. 执行：`python tools/activation/bypass_activation.py`
3. 看到 `[SUCCESS]` 后重启 ComfyUI
4. 验证激活状态：查看启动日志是否显示"已激活"

**遇到问题？** 参见 [docs/TROUBLESHOOTING.md](../docs/TROUBLESHOOTING.md)

---

### 诊断工作流问题

```bash
# 检查工作流中的 LoRA 配置
python tools/workflow/inspect_workflow.py workflows/examples/LTX2_3_a2v.json

# 输出示例：
# Node 3 (LTXVideo):
#   lora_02: ltx-2.3-22b-distilled-lora-384-1.1.safetensors (OK)
#   lora_03: None
```

---

## 📖 详细文档

每个工具子目录中都包含自己的 `README.md`，提供详细的使用说明和参数文档：

- [`activation/README.md`](activation/README.md) - 激活机制详解
- [`workflow/README.md`](workflow/README.md) - 工作流转换工具手册
- [`settings/README.md`](settings/README.md) - 设置管理方案
- [`lora/README.md`](lora/README.md) - LoRA预设面板开发指南

---

## 🔨 开发指南

### 添加新工具脚本

1. 将脚本放入对应分类的子目录
2. 编写完整的 docstring（英文或中文）
3. 如果需要，为该目录更新 `README.md`
4. 在根目录 `README.md` 的工具列表中添加条目

### 脚本规范

- ✅ 使用 Python 3.10+ 语法
- ✅ 添加类型提示（Type Hints）
- ✅ 包含 `if __name__ == "__main__":` 入口
- ✅ 使用 `argparse` 处理命令行参数
- ✅ 提供 `--help` 文档字符串
- ❌ 避免硬编码路径（使用相对路径或配置）

---

## 🐛 问题反馈

如遇工具脚本执行错误：

1. 检查 Python 版本：`python --version`（应为 3.10 或 3.11）
2. 查看完整错误堆栈
3. 确认当前目录为项目根目录
4. 提交 Issue 时附上：
   - 操作系统版本
   - 错误日志全文
   - 执行的相关命令

---

*最后更新: 2026-04-22*
