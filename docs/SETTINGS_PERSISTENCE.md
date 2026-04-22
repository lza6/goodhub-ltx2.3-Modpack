# LTX2.3 设置持久化设计方案

> **版本**: 1.0  
> **创建日期**: 2026-04-22  
> **状态**: 方案设计阶段

---

## 目录

1. [问题定义](#1-问题定义)
2. [现有机制分析](#2-现有机制分析)
3. [设计方案](#3-设计方案)
4. [技术实现](#4-技术实现)
5. [集成方案](#5-集成方案)
6. [迁移策略](#6-迁移策略)

---

## 1. 问题定义

### 1.1 用户痛点

当前 LTX2.3 Web UI 中，用户在标签页中设置的选项（如"显存自动清理"、"默认帧率"等）**不会在重启后保持**。每次启动Web UI都需要重新配置，严重影响使用效率。

**典型场景**：
```
第1天：
  ✓ 勾选"显存自动清理"
  ✓ 设置"默认FPS: 24"
  ✓ 选择"分辨率: 1024x576"
  → 生成视频成功
  → 关闭ComfyUI

第2天：
  □ 显存自动清理未勾选
  □ FPS恢复为默认值16
  □ 分辨率恢复为默认值512x512
  → 需要重新配置
```

### 1.2 根本原因

通过分析 `ComfyUI/user/default/comfy.settings.json` 发现：

```json
{
  "default_ui": { ... },
  "tts_settings": { ... }
  // 仅包含ComfyUI原生设置
  // 不包含LTXVideo节点的自定义参数
}
```

**关键发现**：
- LTXVideo 的参数**不是全局设置**，而是**绑定在工作流文件（.json）中**
- 每次创建新工作流时，使用的都是**节点默认值**，而非用户偏好
- Gradio 的 `gr.State()` 仅在会话期间有效，重启后丢失

---

## 2. 现有机制分析

### 2.1 ComfyUI 设置存储

ComfyUI 的设置分为三级：

| 级别 | 存储位置 | 生命周期 | 可配置项 |
|-----|---------|---------|---------|
| **全局设置** | `ComfyUI/user/default/comfy.settings.json` | 永久 | 主题、语言、自定义路径 |
| **工作流参数** | `*.json` 工作流文件 | 永久 | 所有节点参数值 |
| **会话状态** | 内存 `gr.State()` | 临时 | 当前图状态、历史记录 |

**LTXVideo 参数当前属于第2级**（工作流参数），这意味着：
- 保存工作流 = 参数持久化 ✅
- 不保存工作流 = 参数丢失 ❌

**用户行为模式**：
```
普通用户: 生成视频 → 关闭窗口（忘记保存工作流）→ 设置丢失
高级用户: 每次修改后 Ctrl+S → 设置保留 ✅
```

问题在于**高级用户也需要记得保存**，而大多数用户不知道。

---

### 2.2 LTXVideo 节点参数结构

通过检查 `LTX2_3_a2v.json` 等示例工作流，发现 LTXVideo 节点参数格式：

```json
{
  "nodes": [
    {
      "id": 3,
      "type": "LTXVideo",
      "inputs": [
        {"name": "positive", "value": "..."},
        {"name": "negative", "value": "..."},
        {"name": "seed", "value": -1},
        // ...
      ],
      "widgets_values": [
        "image_path",      // 0: 输入图像
        "1024",            // 1: 宽度
        "576",             // 2: 高度
        "24",              // 3: FPS
        "5.0",             // 4: 时长（秒）
        "20",              // 5: 采样步数
        "3.5",             // 6: CFG
        "0.95",            // 7: VE 调度器 sigma
        // ...
      ]
    }
  ]
}
```

**关键参数**（用户希望持久化的）：
- `width`, `height` (分辨率)
- `fps` (帧率)
- `steps` (采样步数)
- `cfg` (CFG scale)
- `seed` (随机种子，通常为 -1 表示随机)
- 显存清理相关选项（可能在 `extra_options` 中）

---

## 3. 设计方案

### 3.1 架构目标

```
┌─────────────────────────────────────────────────────────────┐
│                    LTX2.3 设置持久化系统                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────────┐          ┌─────────────────────┐   │
│   │  Gradio 设置面板 │  ←用户→  │  全局配置文件        │   │
│   │  (UI 侧边栏)    │          │  ~/.ltx_config/     │   │
│   └────────┬────────┘          │  settings.json      │   │
│            │                    └─────────┬───────────┘   │
│            │ 实时保存                   │ 读取           │
│            ▼                            ▼                │
│   ┌─────────────────┐          ┌─────────────────────┐   │
│   │  内存缓存        │          │  工作流注入器        │   │
│   │  (运行时)       │          │  (运行时)           │   │
│   └─────────────────┘          └─────────┬───────────┘   │
│                                          │               │
│                                          ▼               │
│   ┌─────────────────────────────────────────────┐       │
│   │        LTXVideo 节点实例                     │       │
│   │        (接收注入的参数)                       │       │
│   └─────────────────────────────────────────────┘       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 配置文件结构

**位置**: `~/.ltx_config/settings.json`  
**格式**: JSON

```json
{
  "version": "1.0",
  "created_at": "2026-04-22T14:30:00Z",
  "last_updated": "2026-04-22T15:45:00Z",
  "global_defaults": {
    "generation": {
      "width": 1024,
      "height": 576,
      "fps": 24,
      "frames": 129,
      "steps": 20,
      "cfg": 3.5,
      "sampler_name": "euler_cfgpp",
      "scheduler": "normal"
    },
    "lora": {
      "lora_01": "None",
      "lora_02": "ltx-2.3-22b-distilled-lora-384-1.1.safetensors",
      "lora_03": "None",
      "lora_04": "None",
      "strength_default": 0.8
    },
    "vram": {
      "auto_clear": true,
      "clear_after_gen": true,
      "clear_between_steps": false,
      "aggressive_mode": false
    },
    "output": {
      "save_metadata": true,
      "include_workflow": true,
      "output_dir": "ComfyUI/output/ltx2.3"
    }
  },
  "ui_preferences": {
    "show_advanced": false,
    "theme": "dark",
    "language": "zh-CN",
    "auto_save_workflow": true
  },
  "custom_presets": {
    "quick_test": {
      "generation": {
        "steps": 15,
        "cfg": 3.0
      },
      "description": "快速测试预设（低步数）"
    },
    "high_quality": {
      "generation": {
        "steps": 30,
        "cfg": 4.0
      },
      "description": "高质量预设"
    }
  },
  "statistics": {
    "total_generations": 42,
    "avg_generation_time": 156.3,
    "last_workflow": "LTX2_3_base.json"
  }
}
```

---

### 3.3 注入策略

当用户**加载一个工作流**时，系统执行：

```python
def inject_global_defaults(workflow_data, config):
    """
    如果工作流中某个参数为默认值（通常是None或空），
    则用全局配置中的值来填充。
    """
    for node in workflow_data.get("nodes", []):
        if node.get("type") == "LTXVideo":
            widgets = node.get("widgets_values", [])

            # 映射配置项到widget索引（需实测确认）
            mapping = {
                "width": 1,
                "height": 2,
                "fps": 3,
                "steps": 5,
                "cfg": 6,
                # ...
            }

            for key, idx in mapping.items():
                current = widgets[idx]
                default = get_nested(config, f"global_defaults.generation.{key}")

                # 仅在当前值为"空"时注入（避免覆盖用户有意设置的旧值）
                if is_empty_value(current):
                    widgets[idx] = default

    return workflow_data
```

**注入时机**：
1. 用户在 LTXVideo 标签页点击"加载工作流"
2. 在解析 JSON 后、渲染 UI 前调用 `inject_global_defaults()`
3. UI 显示注入后的参数，用户在"保存工作流"时会持久化

---

## 4. 技术实现

### 4.1 Python 配置管理器

**文件**: `ltx_config_manager.py`

```python
import json
import os
from pathlib import Path
from typing import Any, Dict

class LTXConfigManager:
    """LTX2.3 全局配置管理器"""

    CONFIG_DIR = Path.home() / ".ltx_config"
    CONFIG_FILE = CONFIG_DIR / "settings.json"

    def __init__(self):
        self.config: Dict[str, Any] = {}
        self._ensure_config_exists()
        self.load()

    def _ensure_config_exists(self):
        """确保配置目录和文件存在"""
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        if not self.CONFIG_FILE.exists():
            self._create_default_config()

    def _create_default_config(self):
        """创建默认配置"""
        default = {
            "version": "1.0",
            "created_at": datetime.utcnow().isoformat() + "Z",
            "global_defaults": {
                "generation": {
                    "width": 1024,
                    "height": 576,
                    "fps": 24,
                    "steps": 20,
                    "cfg": 3.5,
                },
                "lora": {
                    "lora_01": "None",
                    "lora_02": "ltx-2.3-22b-distilled-lora-384-1.1.safetensors",
                    "lora_03": "None",
                    "lora_04": "None",
                },
                "vram": {
                    "auto_clear": True,
                    "clear_after_gen": True,
                }
            }
        }
        self.save(default)

    def load(self) -> Dict[str, Any]:
        """加载配置"""
        try:
            with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"[ERROR] 加载配置失败: {e}")
            self.config = self._create_default_config()
        return self.config

    def save(self, config: Dict[str, Any] = None):
        """保存配置"""
        if config:
            self.config.update(config)
        with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项（支持点号分隔的嵌套键）"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def set(self, key: str, value: Any):
        """设置配置项"""
        keys = key.split('.')
        target = self.config
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        target[keys[-1]] = value
        self.save()
```

---

### 4.2 Gradio 集成代码

在 `LTXVideo` 标签页初始化时，添加一个设置面板：

```python
import gradio as gr
from ltx_config_manager import LTXConfigManager

config_mgr = LTXConfigManager()

def create_settings_panel():
    """创建设置侧边栏"""
    with gr.Accordion("⚙️ 全局设置", open=False):
        gr.Markdown("这些设置会自动应用到新工作流")

        # 显存管理
        auto_clear = gr.Checkbox(
            label="显存自动清理",
            value=config_mgr.get("global_defaults.vram.auto_clear"),
            info="每次生成后自动清理显存"
        )
        clear_after_gen = gr.Checkbox(
            label="生成后清理",
            value=config_mgr.get("global_defaults.vram.clear_after_gen")
        )

        # 默认分辨率
        with gr.Row():
            width = gr.Number(
                label="宽度",
                value=config_mgr.get("global_defaults.generation.width"),
                precision=0
            )
            height = gr.Number(
                label="高度",
                value=config_mgr.get("global_defaults.generation.height"),
                precision=0
            )

        # 默认FPS和帧数
        fps = gr.Number(
            label="FPS",
            value=config_mgr.get("global_defaults.generation.fps"),
            precision=0
        )
        steps = gr.Slider(
            label="采样步数",
            minimum=1,
            maximum=100,
            value=config_mgr.get("global_defaults.generation.steps"),
        )

        # 保存按钮
        save_btn = gr.Button("💾 保存为默认设置", variant="primary")
        status = gr.Textbox(label="状态", interactive=False)

        # 绑定事件
        save_btn.click(
            fn=lambda: config_mgr.save(),
            inputs=[],
            outputs=[status]
        ).then(
            fn=lambda: "✅ 设置已保存！",
            inputs=[],
            outputs=[status]
        )

    return auto_clear, width, height, fps, steps
```

**注意**：实际位置需根据 `app.py` 或自定义节点入口调整。

---

### 4.3 工作流注入钩子

在 LTXVideo 节点的 `load_workflow()` 方法中添加：

```python
def load_workflow_with_defaults(workflow_file):
    """加载工作流并注入全局默认值"""
    # 1. 读取工作流JSON
    with open(workflow_file, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    # 2. 加载全局配置
    config_mgr = LTXConfigManager()

    # 3. 注入默认值
    modified = False
    for node in workflow.get("nodes", []):
        if node.get("type") == "LTXVideo":
            widgets = node.get("widgets_values", [])

            # 定义映射：配置键 → widgets索引
            mapping = {
                "width": (1, lambda v: str(v)),
                "height": (2, lambda v: str(v)),
                "fps": (3, lambda v: str(v)),
                "steps": (5, lambda v: str(v)),
                # LoRA 槽位
                "lora_01": (8, lambda v: v),  # 需要实测确定索引
                "lora_02": (9, lambda v: v),
            }

            for key, (idx, transform) in mapping.items():
                current_val = widgets[idx] if idx < len(widgets) else None
                default_val = config_mgr.get(f"global_defaults.generation.{key}") \
                    or config_mgr.get(f"global_defaults.lora.{key}")

                if default_val and is_empty(current_val):
                    # 确保类型一致
                    widgets[idx] = transform(default_val)
                    modified = True
                    print(f"[INFO] 注入默认值 {key}={default_val}")

    # 4. 如果有修改，标记为"需要保存"
    if modified:
        # 更新 Gradio 前端状态
        gr.Info("⚠️ 检测到全局默认设置已应用，请保存工作流")
        # 可选：自动触发保存
        # workflow_state = gr.State(value=workflow)

    return workflow
```

**注入条件**：仅当节点当前值为"空"时才注入，避免覆盖用户有意设置的值。

---

## 5. 集成方案

### 5.1 方案A：独立自定义节点（推荐）

创建一个新的 ComfyUI 自定义节点 `ComfyUI-LTXConfig`，包含：
- 配置存储逻辑（Python 后端）
- 设置面板 UI（Gradio 组件）
- 工作流注入钩子

**优点**：
- 不修改 LTXVideo 源码
- 易于卸载/更新
- 可独立发布到 ComfyUI Manager

**实施**：
```
ComfyUI/custom_nodes/ComfyUI-LTXConfig/
├── __init__.py          # 节点注册
├── ltx_config_manager.py # 配置管理器
├── settings_panel.py     # Gradio UI
└── workflow_injector.py  # 注入逻辑
```

---

### 5.2 方案B：修改 LTXVideo 源码

直接修改 `LTXVideo` 节点的 Python 文件，硬编码集成。

**缺点**：
- 需要修改二进制 `.pyd` 文件或源文件（如果存在）
- 官方更新时会覆盖
- 不推荐

---

### 5.3 方案C：前端 JavaScript 注入

通过浏览器控制台或油猴脚本，在 Gradio 前端注入配置管理逻辑。

**缺点**：
- 依赖用户浏览器操作
- 无法在服务端自动生效
- 不符合 LTX2.3 当前架构

**不推荐**。

---

## 6. 迁移策略

### 6.1 数据迁移

如果用户已有保存的工作流文件，进行批量处理：

```python
def migrate_old_workflows(old_dir, new_dir):
    """
    扫描旧工作流，将"空参数"替换为全局默认值
    """
    config_mgr = LTXConfigManager()

    for wf_file in Path(old_dir).glob("*.json"):
        with open(wf_file, 'r', encoding='utf-8') as f:
            workflow = json.load(f)

        # 统计修改数量
        changes = inject_global_defaults(workflow, config_mgr.config)

        if changes > 0:
            # 备份原文件
            backup = wf_file.with_suffix('.json.bak')
            shutil.copy(wf_file, backup)

            # 保存新文件
            with open(wf_file, 'w', encoding='utf-8') as f:
                json.dump(workflow, f, indent=2)

            print(f"[MIGRATED] {wf_file.name} ({changes} 处修改)")
```

**迁移前必须**：
1. 创建完整备份目录 `workflows_backup_20260422/`
2. 使用 `inspect_workflow.py` 生成报告
3. 在少量文件上测试迁移逻辑

---

### 6.2 回滚方案

如果新系统出现问题，用户可以：

1. **恢复单个工作流**：
   - 删除 `.json` 文件
   - 从 `.json.bak` 恢复

2. **禁用配置注入**：
   - 删除/重命名 `~/.ltx_config/` 目录
   - 重启 ComfyUI

3. **完全卸载**：
   - 移除 `ComfyUI-LTXConfig` 节点目录
   - 删除配置文件

---

## 7. 测试计划

### 7.1 单元测试

```python
def test_config_manager():
    """测试配置管理器"""
    mgr = LTXConfigManager()

    # 测试获取默认值
    width = mgr.get("global_defaults.generation.width")
    assert width == 1024

    # 测试设置和读取
    mgr.set("global_defaults.generation.fps", 30)
    assert mgr.get("global_defaults.generation.fps") == 30

    # 测试嵌套路径
    mgr.set("ui_preferences.theme", "light")
    assert mgr.get("ui_preferences.theme") == "light"

def test_workflow_injector():
    """测试工作流注入"""
    workflow = {
        "nodes": [
            {
                "type": "LTXVideo",
                "widgets_values": [None, None, None, "", "5.0", 20, 3.5]
            }
        ]
    }

    config = {
        "global_defaults": {
            "generation": {"width": 1024, "height": 576, "fps": 24}
        }
    }

    modified = inject_global_defaults(workflow, config)
    assert modified == True
    assert workflow["nodes"][0]["widgets_values"][1] == "1024"
    assert workflow["nodes"][0]["widgets_values"][3] == "24"
```

---

### 7.2 集成测试

**场景1：新用户首次使用**
1. 安装 LTX2.3，没有配置文件
2. 启动 Web UI → 创建设置面板 → 修改参数 → 保存
3. 验证 `~/.ltx_config/settings.json` 已创建且包含正确值

**场景2：加载旧工作流**
1. 有一个旧工作流，其中 `fps=""`（空）
2. 打开该工作流 → 检查 UI 中的 FPS 输入框
3. 应为配置文件中的 `global_defaults.generation.fps`

**场景3：用户故意重置**
1. 用户在 LTXVideo 节点中明确设置 `fps=10`
2. 加载时不应注入全局默认值（24）

---

## 8. 边界情况处理

| 场景 | 情况 | 处理逻辑 |
|-----|------|---------|
| 配置文件损坏 | JSON 解析失败 | 删除旧文件，创建新的默认配置，提示用户 |
| 升级后配置版本不匹配 | `config["version"]` 不同 | 提示用户重新配置，或提供迁移脚本 |
| 工作流文件格式异常 | widgets_values 长度不足 | 跳过注入，记录警告日志 |
| 多用户环境 | `~` 指向不同用户 | 每个用户有独立的 `~/.ltx_config/` |
| 显存不足错误 | 用户设置了过高的分辨率 | 在 UI 中添加验证，显示警告 |

---

## 9. 文档与用户指南

### 9.1 用户文档要点

需要向用户说明：

1. ✅ **新增功能**：现在有一个"全局设置"面板
2. ✅ **如何配置**：在设置面板中调整，点击"保存"
3. ✅ **如何生效**：新工作流自动应用；旧工作流需重新加载
4. ⚠️ **注意**：如果工作流中已有非空参数，不会被覆盖

### 9.2 开发者文档要点

需要为后续维护者提供：

- 配置文件schema说明
- 注入逻辑的widget索引映射表（需根据实际节点代码确认）
- 如何扩展新的配置项
- 调试方法（如何查看注入日志）

---

## 10. 后续迭代

### Phase 2 - 智能默认值

根据用户历史行为，自动优化默认值：
```python
# 分析最近10次生成
if user_avg_fps > 25:
    config["global_defaults"]["generation"]["fps"] = 30
```

### Phase 3 - 云同步

可选：将配置上传到用户账号，跨设备同步。

### Phase 4 - 预设市场

允许用户导出/导入配置预设文件（`.ltxpreset.json`），社区共享。

---

*文档版本: v1.0*  
*最后更新: 2026-04-22*
