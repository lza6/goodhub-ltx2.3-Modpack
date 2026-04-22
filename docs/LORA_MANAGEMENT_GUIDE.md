# LTX2.3 LoRA 版本管理与兼容性指南

> **版本**: 1.0  
> **创建日期**: 2026-04-22  
> **适用**: LTX2.3_v4.0 用户

---

## 目录

1. [LoRA 基础概念](#1-lora-基础概念)
2. [版本差异详解](#2-版本差异详解)
3. [兼容性矩阵](#3-兼容性矩阵)
4. [用户 LoRA 文件清单](#4-用户-lora-文件清单)
5. [版本不匹配问题排查](#5-版本不匹配问题排查)
6. [使用建议](#6-使用建议)

---

## 1. LoRA 基础概念

### 1.1 什么是 LoRA

**LoRA** (Low-Rank Adaptation) 是一种轻量级的模型微调技术，通过在预训练模型的基础上添加少量可学习的低秩矩阵，实现对模型的快速适配，而无需修改原始模型参数。

在 LTX2.3 中，LoRA 用于：
- **风格迁移**：调整输出视频的视觉风格（如画质增强、电影感）
- **内容控制**：深度图、边缘图等条件控制
- **性能优化**：蒸馏版 LoRA 提供更快的推理速度

### 1.2 LoRA 槽位说明

LTXVideo 节点提供 4 个 LoRA 槽位：

| 槽位 | 用途 | 推荐场景 |
|-----|------|---------|
| `lora_01` | 预留（当前未使用） | - |
| `lora_02` | 主 LoRA | 蒸馏版 / 画质增强 |
| `lora_03` | 第二 LoRA | 组合增强 |
| `lora_04` | 第三 LoRA | IC-LoRA 联合控制 |

**显存注意**：同时启用多个 LoRA 会显著增加显存占用：
- 单 LoRA：+1-2GB 显存
- 双 LoRA：+3-5GB 显存  
- 三 LoRA：+6-10GB 显存（需要 32GB+ 显存）

---

## 2. 版本差异详解

### 2.1 版本命名格式

```
ltx-{模型版本}-{类型}-{规格}.safetensors
```

| 字段 | 示例 | 说明 |
|-----|------|------|
| 模型版本 | `2.3-22b`, `2-19b`, `2.3-22b-distilled` | 对应的基础模型版本 |
| 类型 | `distilled`, `ic-lora`, `crisp` | LoRA 训练方法 |
| 规格 | `384-1.1`, `union-control-ref0.5` | 训练参数/配置 |

### 2.2 可用 LoRA 类型

#### 蒸馏版 LoRA (Distilled)

```
ltx-2.3-22b-distilled-lora-384-1.1.safetensors
```

- **特点**：专为快速推理优化，体积大但加载快
- **推荐场景**：日常测试、批量生成
- **显存需求**：约 7-8GB
- **推荐 strength**：0.6 - 1.0

#### IC-LoRA 联合控制 (Union Control)

```
ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors
```

- **特点**：支持深度图和边缘图双条件控制
- **推荐场景**：需要精确控制运动和轮廓的生成
- **显存需求**：约 600MB - 1GB
- **推荐 strength**：0.3 - 0.7

#### Crisp Enhance (画质增强)

```
LTX2.3_Crisp_Enhance.safetensors
```

- **特点**：提升视频清晰度和细节
- **推荐场景**：最终输出前的质量增强（常与蒸馏版组合）
- **显存需求**：约 700MB
- **推荐 strength**：0.5 - 0.8

#### 其他 LoRA

```
Ltx2.3-Licon-VBVR-I2V-96000-R32.safetensors
ltx-2.3-22b-distilled-1.1_lora-dynamic_fro09_avg_rank_111_bf16.safetensors
```

- 这些是实验性或特定用途的 LoRA
- 需根据实际测试结果使用

---

## 3. 兼容性矩阵

### 3.1 主模型与 LoRA 版本匹配

| 主模型版本 | 兼容的 LoRA 版本 | 不兼容的 LoRA 版本 |
|-----------|-----------------|-------------------|
| `ltx-2.3-22b-*` | `ltx-2.3-22b-*` | `ltx-2-19b-*` |
| `ltx-2.3-22b-distilled-*` | `ltx-2.3-22b-*` (均兼容) | - |
| `ltx-2-19b-*` | `ltx-2-19b-*` | `ltx-2.3-22b-*` |

**关键规则**：
- **2.3 的 LoRA 不能用于 2.19 模型**
- **2.19 的 LoRA 不能用于 2.3 模型**
- 主模型版本必须 ≥ LoRA 版本（或匹配）

### 3.2 组合兼容性

| LoRA 组合 | 兼容性 | 注意事项 |
|----------|--------|---------|
| 蒸馏 + Crisp | ✅ 推荐 | 常用组合，效果好 |
| 蒸馏 + IC-LoRA | ✅ 推荐 | 需控制 strength |
| Crisp + IC-LoRA | ⚠️ 需测试 | 可能冲突 |
| 蒸馏 + Crisp + IC-LoRA | ⚠️ 高显存 | 需要 32GB+ 显存 |

---

## 4. 用户 LoRA 文件清单

基于 `D:\LTX2.3_v4.0\ComfyUI\models\loras\` 目录扫描：

| 文件名 | 大小 | 类型 | 状态 |
|--------|------|------|------|
| `LTX2.3_Crisp_Enhance.safetensors` | 705 MB | 画质增强 | ✅ 可用 |
| `ltx-2.3-22b-distilled-lora-384-1.1.safetensors` | 7.6 GB | 蒸馏版 | ✅ 可用 |
| `ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors` | 654 MB | IC-LoRA | ✅ 可用 |
| `Ltx2.3-Licon-VBVR-I2V-96000-R32.safetensors` | 554 MB | I2V | ⚠️ 实验性 |
| `ltx-2.3-22b-distilled-1.1_lora-dynamic_fro09_avg_rank_111_bf16.safetensors` | 2.7 GB | 蒸馏版(变体) | ⚠️ 实验性 |

---

## 5. 版本不匹配问题排查

### 5.1 常见错误信息

```
Value not in list: lora_03: 'ltx-2-19b-distilled-lora_xxx.safetensors' 
not in ['None', 'LTX2.3_Crisp_Enhance.safetensors', ...]
```

**原因**：工作流中配置了旧版本（2.19b）的 LoRA，但用户只有 2.3 22b 版本的 LoRA 文件。

### 5.2 解决步骤

#### 步骤1：诊断检查

```python
# 运行 inspect_workflow.py 分析工作流
python inspect_workflow.py D:\LTX2.3_v4.0\LTX2_3_a2v.json
```

#### 步骤2：识别问题工作流

找到所有引用 `ltx-2-19b-*` 的工作流文件。

#### 步骤3：修复方案

**方案A：手动重置（推荐新手）**
1. 打开 Web UI 中的工作流
2. 在 Lora Loader 节点中，将所有 LoRA 槽位设为 "None"
3. 保存工作流

**方案B：使用预设面板**
1. 在浏览器 F12 控制台注入 `lora_preset_inject.js`
2. 选择"无LoRA"预设 → 点击应用
3. 选择合适的 LoRA 预设 → 点击应用
4. 保存工作流

**方案C：批量转换（高级）**
使用 `convert_workflows.py` 脚本批量替换。

---

## 6. 使用建议

### 6.1 推荐的 LoRA 组合

| 场景 | 组合 | LoRA 1 | LoRA 2 | LoRA 3 |
|------|------|--------|--------|--------|
| 快速测试 | 单蒸馏 | 蒸馏 0.8 | None | None |
| 标准生成 | 双组合 | 蒸馏 0.8 | Crisp 0.6 | None |
| 高质量 | 全激活 | 蒸馏 0.9 | Crisp 0.7 | IC-LoRA 0.5 |
| 深度控制 | IC单用 | None | None | IC-LoRA 0.6 |

### 6.2 Strength 参数建议

| 场景 | 范围 | 说明 |
|------|------|------|
| 轻微风格 | 0.3 - 0.5 | 保留原模型大部分特征 |
| 均衡 | 0.5 - 0.7 | 平衡风格与原始 |
| 强风格 | 0.7 - 1.0 | LoRA 效果为主 |

### 6.3 性能优化

1. **测试阶段**：使用"无LoRA"或单蒸馏版，减少加载时间
2. **正式生成**：启用需要的完整 LoRA 组合
3. **显存不足时**：减少 LoRA 数量或降低分辨率

---

## 附录：技术细节

### A. LoRA 加载流程

```
1. 初始化 Lora Loader 节点
2. 读取用户选择的 LoRA 文件名
3. 从磁盘加载 .safetensors 文件
4. 解压 LoRA 权重到 GPU 显存
5. 将 LoRA 权重叠加到基础模型
```

### B. 文件路径

- LoRA 存储：`D:\LTX2.3_v4.0\ComfyUI\models\loras\`
- 工作流存储：`D:\LTX2.3_v4.0\*.json`
- LoRA 预设配置：`lora_preset_inject.js` 或 `lora_preset.user.js`

---

*文档版本: v1.0*
*最后更新: 2026-04-22*