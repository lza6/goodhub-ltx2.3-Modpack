# 工作流工具

本目录提供 LTX2.3 工作流的分析、转换和诊断工具。

---

## 📋 工具列表

### inspect_workflow.py

**用途**：分析工作流 JSON 文件的结构，显示 LoRA 配置、节点类型、参数详情。

**用法**：
```bash
python tools/workflow/inspect_workflow.py <工作流文件路径>
```

**示例**：
```bash
python tools/workflow/inspect_workflow.py workflows/examples/LTX2_3_a2v.json
```

**输出**：
```
============================================================
  工作流分析: LTX2_3_a2v.json
============================================================

文件信息:
  路径: D:\LTX2.3_v4.0\workflows\examples\LTX2_3_a2v.json
  大小: 8,593 字节
  修改时间: 2026-03-09 17:08:00

节点总数: 12

LTXVideo 节点 (ID: 3):
  节点类型: LTXVideo
  标题: LTX2.3 图生视频

  LoRA 配置:
    lora_01: None
    lora_02: ltx-2.3-22b-distilled-lora-384-1.1.safetensors  [OK]
    lora_03: None
    lora_04: None

  关键参数:
    分辨率: 1024 x 576
    帧率: 24 FPS
    采样步数: 20
    CFG: 3.5

LoRA 文件检查:
  ✓ ltx-2.3-22b-distilled-lora-384-1.1.safetensors 存在于磁盘
```

---

### convert_workflows.py (开发中)

**用途**：批量将旧版工作流中的 LoRA 文件名更新为新版本。

**待实现功能**：
- 扫描目录下所有 `.json` 工作流文件
- 识别不存在的 LoRA 引用
- 根据映射表自动替换文件名
- 创建备份文件

**计划参数**：
```bash
# 批量转换
python tools/workflow/convert_workflows.py --dir workflows/examples/

#  dry-run 预览
python tools/workflow/convert_workflows.py --dry-run --file example.json

# 使用自定义映射
python tools/workflow/convert_workflows.py --mapping my_mapping.json
```

---

## 🎯 使用场景

### 场景1：工作流加载失败

**错误信息**：
```
Value not in list: lora_03: 'ltx-2-19b-xxx.safetensors'
not in ['None', 'LTX2.3_Crisp_Enhance.safetensors', ...]
```

**诊断步骤**：
1. 运行 `inspect_workflow.py` 查看该工作流
2. 确认 LoRA 文件名与磁盘实际文件是否匹配
3. 参考 [docs/LORA-GUIDE.md](../docs/LORA-GUIDE.md) 选择正确的 LoRA
4. 手动修改或等待批量转换工具

---

### 场景2：批量检查多个工作流

```bash
# 批量分析
for f in workflows/examples/*.json; do
    echo "=== 分析: $f ==="
    python tools/workflow/inspect_workflow.py "$f" | grep -i "lora"
done
```

---

## 📊 输出说明

`inspect_workflow.py` 提供以下信息：

| 部分 | 内容 |
|------|------|
| 文件信息 | 路径、大小、修改时间 |
| 节点统计 | 节点总数、LTXVideo节点数量 |
| 节点详情 | 每个 LTXVideo 节点的参数值 |
| LoRA 配置 | lora_01 到 lora_04 的具体文件名 |
| 文件检查 | 验证 LoRA 文件是否存在于磁盘 |

---

## 🔧 技术细节

### 工作流 JSON 结构

```json
{
  "nodes": [
    {
      "id": 3,
      "type": "LTXVideo",
      "widgets_values": [
        "input.png",       // 0: 输入图像
        "1024",            // 1: 宽度
        "576",             // 2: 高度
        "24",              // 3: FPS
        "...",
        "ltx-2.3-22b-..."  // N: lora_02 (位置需实测)
      ]
    }
  ]
}
```

**注意**：`widgets_values` 数组索引可能因节点版本而异，必须以实际工作流为准。

---

## 🚀 待开发功能

- [ ] 批量转换所有工作流
- [ ] 交互式修复模式（选择替代 LoRA）
- [ ] 工作流版本迁移向导
- [ ] 生成差异报告（旧 vs 新）

---

## 📝 更新日志

| 日期 | 版本 | 工具 | 变更 |
|------|------|------|------|
| 2026-04-22 | v1.0 | inspect_workflow.py | 初始版本，基础分析功能 |
| 2026-04-22 | v1.0 | convert_workflows.py | 计划中 |

---

*最后更新: 2026-04-22*
