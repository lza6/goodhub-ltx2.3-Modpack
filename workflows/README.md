# 工作流资源

本目录包含 LTX2.3 的示例工作流和标准模板。

---

## 📂 子目录

```
workflows/
├── examples/    # 官方示例工作流（已提供）
├── templates/   # 标准模板（待创建）
└── README.md    # 本文件
```

---

## 📥 示例工作流 (`examples/`)

官方提供的参考工作流：

| 文件 | 说明 | 场景 |
|------|------|------|
| `LTX2_3_a2v.json` | 文生视频 | 文本生成视频 |
| `LTX2_3_i2v.json` | 图生视频 | 图像生成视频 |
| `LTX2_3_DZQY.json` | 动作强度控制 | 幅度调节 |
| `LTX2_3_SWZ.json` | 手部细节优化 | 手部生成 |
| `LTX2_3_t2v.json` | 文本转视频 | 另一种配置 |

**使用方法**：
1. 在 Web UI 中点击"Load"
2. 选择对应的 `.json` 文件
3. 检查 LoRA 配置是否正确（必要时使用预设面板调整）
4. 按 `Ctrl+S` 保存修改后的工作流

---

## 📋 标准模板 (`templates/`)

**规划中**：将创建以下标准模板供用户快速开始：

| 模板 | 用途 |
|------|------|
| `baseline.json` | 纯净基线（无LoRA） |
| `single_lora.json` | 单蒸馏LoRA配置 |
| `dual_lora.json` | 推荐双LoRA组合 |
| `all_loras.json` | 全激活实验性配置 |

---

## 🔧 工作流工具

### 分析工作流

```bash
python tools/workflow/inspect_workflow.py workflows/examples/LTX2_3_a2v.json
```

### 批量转换（待实现）

```bash
python tools/workflow/convert_workflows.py --dir workflows/examples/
```

---

## ⚠️ 注意事项

1. **版本兼容**：示例工作流可能使用旧版 LoRA 文件名，使用前请用 `inspect_workflow.py` 检查
2. **备份原始**：修改前建议复制一份到 `workflows/backup/`
3. **路径依赖**：工作流中引用的图像路径为相对路径，请确保文件存在

---

*最后更新: 2026-04-22*
