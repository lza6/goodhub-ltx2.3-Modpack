# 📦 LoRA 使用指南

> **版本**: 1.0  
> **最后更新**: 2026-04-22

---

## 概述

LoRA (Low-Rank Adaptation) 是 LTX2.3 中用于调整视频风格、画质和控制的关键技术。本指南帮助你理解 LoRA 版本兼容性、正确选择和配置。

---

## 🔍 LoRA 文件清单

当前 LTX2.3_v4.0 包含的 LoRA 文件：

| 文件名 | 大小 | 类型 | 状态 |
|--------|------|------|------|
| `LTX2.3_Crisp_Enhance.safetensors` | 705 MB | 画质增强 | ✅ 推荐 |
| `ltx-2.3-22b-distilled-lora-384-1.1.safetensors` | 7.6 GB | 蒸馏版 | ✅ 推荐 |
| `ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors` | 654 MB | IC-LoRA联合控制 | ✅ 可用 |
| `Ltx2.3-Licon-VBVR-I2V-96000-R32.safetensors` | 554 MB | I2V转换 | ⚠️ 实验性 |
| `ltx-2.3-22b-distilled-1.1_lora-dynamic_fro09_avg_rank_111_bf16.safetensors` | 2.7 GB | 蒸馏版变体 | ⚠️ 实验性 |

**位置**：`ComfyUI/models/loras/`

---

## ⚠️ 版本兼容性警告

### 关键规则

```
2.3 版本的 LoRA ❌ 不能用于 2.19b 模型
2.19b 版本的 LoRA ❌ 不能用于 2.3 模型
```

### 错误示例

```
Value not in list: lora_03: 'ltx-2-19b-distilled-lora_xxx.safetensors'
not in ['None', 'LTX2.3_Crisp_Enhance.safetensors', ...]
```

**原因**：工作流中引用了旧版 LoRA（2.19b），但磁盘上只有新版（2.3 22b）。

**解决**：
1. 临时方案：将 Lora Loader 设为 `None`
2. 使用 LoRA 预设面板选择正确的 LoRA
3. 使用 `inspect_workflow.py` 诊断并修复

---

## 🎯 LoRA 槽位说明

LTXVideo 节点提供 4 个 LoRA 槽位：

| 槽位 | 用途 | 推荐配置 |
|------|------|---------|
| `lora_01` | 预留槽位 | 保持 `None` |
| `lora_02` | 主 LoRA | 蒸馏版或画质增强 |
| `lora_03` | 辅助 LoRA | 次要增强或控制 |
| `lora_04` | 控制 LoRA | IC-LoRA 或其他 |

---

## 💡 推荐配置方案

### 方案1：快速测试（最低显存）

```
lora_01: None
lora_02: None
lora_03: None
lora_04: None
```
**显存**: ~12 GB | **速度**: 最快 | **画质**: 基线

---

### 方案2：日常使用（推荐⭐）

```
lora_01: None
lora_02: ltx-2.3-22b-distilled-lora-384-1.1.safetensors  (strength: 0.8)
lora_03: None
lora_04: None
```
**显存**: ~20 GB | **速度**: 快 | **画质**: 良好

---

### 方案3：画质优先（双LoRA）

```
lora_01: None
lora_02: ltx-2.3-22b-distilled-lora-384-1.1.safetensors  (strength: 0.8)
lora_03: LTX2.3_Crisp_Enhance.safetensors                (strength: 0.6)
lora_04: None
```
**显存**: ~21 GB | **速度**: 中等 | **画质**: 优秀

---

### 方案4：全激活（实验性）

```
lora_01: None
lora_02: 蒸馏版 (0.9)
lora_03: Crisp增强 (0.7)
lora_04: IC-LoRA (0.5)
```
**显存**: 32 GB+ | **速度**: 慢 | **画质**: 最高（可能不稳定）

---

## 🎚️ Strength 参数建议

| 范围 | 效果 | 适用场景 |
|------|------|---------|
| 0.3 - 0.5 | 轻微风格 | 保留原始模型特征为主 |
| 0.5 - 0.7 | 均衡混合 | 推荐默认范围 |
| 0.7 - 1.0 | 强风格 | LoRA 效果主导 |

**经验法则**：
- 蒸馏版 LoRA：建议 0.7-1.0（它是主要模型）
- Crisp 增强：建议 0.5-0.7（辅助画质）
- IC-LoRA：建议 0.4-0.6（控制即可，不宜过强）

---

## 🔧 使用预设面板

最快捷的 LoRA 切换方式：

1. 在 Web UI 中激活预设面板（见 README.md）
2. 从下拉菜单选择预设
3. 点击"应用预设"
4. 按 `Ctrl+S` 保存工作流

**内置预设**：
- 无LoRA
- 仅蒸馏LoRA
- 仅Crisp增强
- IC-LoRA Union
- 蒸馏+增强
- 全激活

---

## 🐛 故障排查

### 问题：LoRA 文件不存在错误

**诊断**：
```bash
python tools/workflow/inspect_workflow.py <工作流.json>
```

**修复**：
1. 检查文件名拼写（注意大小写）
2. 确认 `ComfyUI/models/loras/` 目录下文件存在
3. 使用预设面板选择正确的 LoRA
4. 手动编辑工作流 JSON 替换文件名

---

### 问题：显存不足 (Out of Memory)

**立即解决**：
1. 减少 LoRA 数量（从 2 个减到 1 个）
2. 降低 Strength 值
3. 降低分辨率（1024x576 → 512x512）
4. 减少采样帧数

**长期解决**：升级 GPU 显存至 24GB 或以上。

---

### 问题：更新 LoRA 后需要重新加载模型？

**不需要**。LoRA 是在推理时动态加载的，切换 LoRA 不会导致基础模型重载（除非你更换了基础模型）。

**注意**：更换基础模型（如从 2.3 换到 2.1）需要重启 ComfyUI。

---

## 📊 显存需求估算

| 配置 | 基础模型 | LoRA 增量 | 总计估算 |
|------|---------|-----------|---------|
| 无 LoRA | 12 GB | 0 | 12 GB |
| + 蒸馏版 | 12 GB | +7.6 GB | ~20 GB |
| + Crisp | 12 GB | +0.7 GB | ~13 GB |
| + IC-LoRA | 12 GB | +0.65 GB | ~13 GB |
| 蒸馏 + Crisp | 12 GB | +8.3 GB | ~21 GB |
| 全部激活 | 12 GB | +9.5 GB | 32 GB+ |

**注意**：实际显存占用受分辨率、帧数、采样步数影响，以上为 1024x576 分辨率下的近似值。

---

## 🔄 工作流迁移

如果你从旧版本（2.19b）升级到 2.3 22b：

1. **备份现有工作流**：复制 `*.json` 文件到 `workflows/backup/`
2. **扫描问题工作流**：使用 `inspect_workflow.py`
3. **批量转换**（待 convert_workflows.py 实现）
4. **手动修复**：打开 Web UI，逐个修正 Lora Loader 节点的 LoRA 选择

---

## 📝 相关文档

- [激活指南](ACTIVATION.md) - 系统激活
- [预设面板说明](PRESET-PANEL.md) - 一键切换LoRA
- [故障排查](TROUBLESHOOTING.md) - 更多LoRA问题

---

*最后更新: 2026-04-22*
