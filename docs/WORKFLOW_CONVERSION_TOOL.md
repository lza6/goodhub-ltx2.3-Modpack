# 工作流转换工具使用手册

> **版本**: 1.0  
> **创建日期**: 2026-04-22  
> **工具脚本**: `convert_workflows.py`

---

## 目录

1. [工具概述](#1-工具概述)
2. [安装要求](#2-安装要求)
3. [快速开始](#3-快速开始)
4. [功能详解](#4-功能详解)
5. [批量转换](#5-批量转换)
6. [故障排除](#6-故障排除)

---

## 1. 工具概述

### 1.1 用途

`convert_workflows.py` 是一个命令行工具，用于批量将旧版 LTX2.3 工作流文件中的 LoRA 引用更新为新版本对应的文件名。

### 1.2 解决的问题

**问题背景**：
- 用户从旧版本（如 2.19b）升级到 2.3 22b
- 旧工作流中保存的 LoRA 文件名与磁盘上的文件不匹配
- 导致加载工作流时报错：`Value not in list`

**转换示例**：
```
转换前:
  lora_02: "ltx-2-19b-distilled-lora_resized.safetensors"

转换后:
  lora_02: "ltx-2.3-22b-distilled-lora-384-1.1.safetensors"
```

---

## 2. 安装要求

- Python 3.10 或更高版本
- 无需额外依赖（仅使用标准库）

---

## 3. 快速开始

### 3.1 单文件转换

```bash
cd D:\LTX2.3_v4.0

# 转换单个工作流文件
python convert_workflows.py LTX2_3_a2v.json

# 输出:
# [CONVERT] LTX2_3_a2v.json
#   - 更新 1 个 LoRA 引用
#   - 备份创建: LTX2_3_a2v.json.bak
# [DONE] 转换完成！
```

### 3.2 批量转换

```bash
# 转换当前目录下所有 .json 文件
python convert_workflows.py *.json

# 转换指定目录
python convert_workflows.py workflows/*.json

# 递归转换（需要脚本支持）
python convert_workflows.py --recursive ./workflows
```

### 3.3 预览模式

在不实际修改文件的情况下查看将要进行的更改：

```bash
python convert_workflows.py --dry-run LTX2_3_a2v.json
```

输出：
```
[DRY-RUN] LTX2_3_a2v.json
  节点 3 (LTXVideo):
    节点 10 (Lora Loader):
      [lora_02] 'ltx-2-19b-xxx' → 'ltx-2.3-22b-xxx' ( distilled-lora )
  
  将修改 1 处，创建 1 个备份
```

---

## 4. 功能详解

### 4.1 转换规则

工具内置以下转换映射：

| 旧模式 | 新模式 | 说明 |
|-------|--------|------|
| `ltx-2-19b-distilled-lora_*` | `ltx-2.3-22b-distilled-lora-384-1.1.safetensors` | 蒸馏版 |
| `ltx-2-19b-crisp-enhance_*` | `LTX2.3_Crisp_Enhance.safetensors` | Crisp 增强 |
| `ltx-2-19b-ic-lora-*` | `ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors` | IC-LoRA |

### 4.2 命令行参数

```
usage: convert_workflows.py [-h] [--dry-run] [--backup-dir DIR]
                            [--mapping-file FILE] [--verbose]
                            files [files ...]

批量转换LTX2.3工作流文件

positional arguments:
  files                要转换的工作流文件（支持通配符）

options:
  -h, --help           显示帮助信息
  --dry-run            预览模式，不实际修改文件
  --backup-dir DIR     备份文件存放目录（默认：同目录下 .bak）
  --mapping-file FILE  自定义映射文件（JSON格式）
  --verbose, -v        显示详细日志
```

### 4.3 自定义映射文件

创建 `lora_mapping.json`：

```json
{
  "ltx-2-19b-distilled-lora_old_v1.safetensors": "ltx-2.3-22b-distilled-lora-384-1.1.safetensors",
  "my-custom-lora.safetensors": "custom-lora-v2.safetensors"
}
```

然后使用：

```bash
python convert_workflows.py --mapping-file lora_mapping.json *.json
```

---

## 5. 批量转换

### 5.1 全量转换脚本

```python
# batch_convert.py
import subprocess
from pathlib import Path

def batch_convert_workflows():
    """批量转换工作流"""
    base_dir = Path("D:/LTX2.3_v4.0")
    workflow_files = list(base_dir.glob("*.json"))

    print(f"发现 {len(workflow_files)} 个工作流文件")

    for wf in workflow_files:
        # 跳过模板文件
        if wf.name.startswith("template_"):
            continue

        print(f"处理: {wf.name}")
        result = subprocess.run(
            ["python", "convert_workflows.py", str(wf)],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            print("  ✓ 转换成功")
        else:
            print(f"  ✗ 转换失败: {result.stderr}")

if __name__ == "__main__":
    batch_convert_workflows()
```

### 5.2 查找需要转换的文件

```python
def find_mismatched_workflows():
    """查找LoRA版本不匹配的工作流"""
    import json

    mismatched = []
    for wf_file in Path(".").glob("*.json"):
        with open(wf_file) as f:
            data = json.load(f)

        for node in data.get("nodes", []):
            if node.get("type") == "LTXVideo":
                widgets = node.get("widgets_values", [])
                # 检查 lora_02, lora_03, lora_04
                for w in widgets:
                    if isinstance(w, str) and ("ltx-2-19b" in w or "2-19b" in w):
                        mismatched.append((wf_file.name, w))
                        break

    return mismatched
```

---

## 6. 故障排除

### 6.1 问题：转换后工作流无法加载

**原因**：映射规则不准确或widget索引错误

**解决**：
1. 使用 `--dry-run` 预览
2. 检查 JSON 结构是否正确
3. 恢复备份文件：`copy file.json.bak file.json`

### 6.2 问题：找不到旧LoRA文件名

**说明**：某些工作流中LoRA名称可能是相对路径或别名。

**解决**：手动编辑工作流，查找 `"widgets_values"` 数组，确认LoRA所在位置。

### 6.3 问题：批量转换中断

**检查**：
- 确保所有文件都是有效的JSON
- 确保有足够的磁盘空间（备份会占用额外空间）
- 检查文件权限（读写权限）

---

## 附录：技术参考

### A. 工作流JSON结构

```json
{
  "nodes": [
    {
      "id": 3,
      "type": "LTXVideo",
      "widgets_values": [
        "input_image.png",     // 0: 输入图像
        "1024",                // 1: 宽度
        "576",                 // 2: 高度
        "24",                  // 3: FPS
        "5.0",                 // 4: 时长
        "20",                  // 5: 步数
        "3.5",                 // 6: CFG
        "None",                // 7: lora_01  (通常不使用)
        "ltx-2.3-22b-....",   // 8: lora_02
        "None",                // 9: lora_03
        "None"                 // 10: lora_04
      ]
    }
  ]
}
```

**注意**：索引位置可能因节点版本而异，请在转换前用 `inspect_workflow.py` 确认结构。

### B. 文件备份策略

工具默认备份策略：
- 每次转换前自动备份原文件
- 备份文件名：`原文件名.json.bak`
- 支持恢复到任意历史版本

---

*文档版本: v1.0*  
*工具位置: `convert_workflows.py`*
