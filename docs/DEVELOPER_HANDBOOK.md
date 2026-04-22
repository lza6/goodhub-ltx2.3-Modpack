# LTX2.3 开发者手册

> **版本**: 1.0  
> **创建日期**: 2026-04-22  
> **目标读者**: 参与 LTX2.3 开发的工程师

---

## 目录

1. [项目架构概览](#1-项目架构概览)
2. [开发环境搭建](#2-开发环境搭建)
3. [代码结构说明](#3-代码结构说明)
4. [扩展开发指南](#4-扩展开发指南)
5. [调试技巧](#5-调试技巧)
6. [贡献流程](#6-贡献流程)
7. [常见问题](#7-常见问题)

---

## 1. 项目架构概览

### 1.1 系统层次

```
┌──────────────────────────────────────────────────────────┐
│                   用户界面层 (Web UI)                     │
│  Gradio + JavaScript (ltx_preset_inject.js 等)            │
├──────────────────────────────────────────────────────────┤
│                  LTX2.3 核心层                           │
│  LTXVideo 节点 (Python) + 工作流引擎                     │
├──────────────────────────────────────────────────────────┤
│                  ComfyUI 框架层                          │
│  节点系统 + 图执行 + 模型加载                            │
├──────────────────────────────────────────────────────────┤
│                 PyTorch + 模型层                         │
│  LTX 2.3 22b 模型 + LoRA 适配器                          │
└──────────────────────────────────────────────────────────┘
```

### 1.2 核心模块

| 模块 | 路径 | 说明 |
|-----|------|------|
| 主应用 | `app.pyd` (Windows) | 激活检查、主入口 |
| 核心逻辑 | `core.pyd` | 推理引擎 |
| 视频节点 | `LTX2_3_*.pyd` | 各版本 LTXVideo 实现 |
| 模型文件 | `ComfyUI/models/` | `.safetensors` 权重 |
| Web 前端 | `ComfyUI/web/` | Gradio 界面 |

---

## 2. 开发环境搭建

### 2.1 基础环境

**操作系统**：Windows 10/11 (x64)

**Python**：3.10 或 3.11（与 ComfyUI 内嵌版本一致）

```bash
# 验证 Python 版本
python --version
# 应输出: Python 3.10.x 或 3.11.x
```

**依赖安装**：
```bash
cd D:\LTX2.3_v4.0

# 如果已有 virtualenv，激活它
# venv\Scripts\activate

# 或使用内嵌 Python
.\python_embeded\python.exe -m pip install -r requirements.txt
```

---

### 2.2 开发工具

| 工具 | 用途 | 推荐版本 |
|-----|------|---------|
| VS Code | 代码编辑 | 最新版 |
| Python 插件 (ms-python.python) | Python 支持 | - |
| Pylance | 类型检查 | - |
| 7-Zip | 解压 `.pyd`（实际是 DLL） | - |
| IDA Pro / Ghidra | 反编译 `.pyd`（高级） | - |
| Fiddler / Wireshark | 网络抓包（分析激活） | - |

---

### 2.3 项目克隆与构建

```bash
# 1. 克隆 LTX2.3 仓库（如果是从源码构建）
git clone <repository-url>
cd ltx2.3

# 2. 创建开发分支
git checkout -b dev/your-feature

# 3. 安装依赖
pip install -r requirements.txt

# 4. 构建 `.pyd` 文件（Windows）
python setup.py build_ext --inplace
```

---

## 3. 代码结构说明

### 3.1 后端 Python 模块

```
ComfyUI/
├── custom_nodes/
│   └── ComfyUI-LTXVideo/        # LTXVideo 自定义节点
│       ├── __init__.py
│       ├── ltx_video_node.py    # 节点定义
│       ├── ltx_video_utils.py   # 工具函数
│       └── web/
│           └── ltx_video.js     # 前端交互（可选）
├── models/
│   ├── loras/                   # LoRA 文件
│   ├── checkpoints/             # 主模型
│   └── vae/                     # VAE 模型
└── user/
    └── default/
        └── comfy.settings.json  # ComfyUI 设置
```

---

### 3.2 前端 JavaScript 模块

```
web/
├── script.js                    # Gradio 主脚本
├── app.js                       # 应用逻辑
├── ext/
│   └── ltx_preset/              # LoRA 预设扩展
│       ├── lora_presets.json    # 预设数据
│       ├── panel.js             # 面板逻辑
│       └── inject.js            # 注入器
└── css/
    └── ltx_preset.css           # 样式
```

---

### 3.3 关键文件说明

#### `bypass_activation.py`

**用途**：绕过激活验证，生成本地激活文件

**关键函数**：
```python
def generate_activation():
    spec = importlib.util.spec_from_file_location('app', 'app.pyd')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    machine_id = module.get_machine_fingerprint()
    module.save_activation(BYPASS_CODE, machine_id)
    module.update_verification_cache(BYPASS_CODE, True)
```

**扩展点**：
- 可添加机器指纹缓存，避免重复计算
- 可集成到启动脚本，自动检查激活状态

---

#### `lora_preset_inject.js`

**用途**：浏览器端注入 LoRA 预设面板

**架构**：
```javascript
const LORA_PRESETS = { ... };  // 配置数据

function injectPanel() { ... }  // 注入 UI

function applyPreset(name) { ... }  // 应用逻辑

// 自执行
(function() { ... })();
```

**扩展建议**：
- 将预设数据外部化为 JSON 文件，通过 fetch 加载
- 支持用户自定义预设的本地存储
- 添加快捷键支持（如 1-6 数字键切换）

---

## 4. 扩展开发指南

### 4.1 新增 LoRA 预设

**步骤 1**：编辑 `lora_preset_inject.js`

找到 `const LORA_PRESETS = { ... }` 部分，添加新条目：

```javascript
"我的新预设": {
  "description": "新组合的描述",
  "loras": {
    "lora_01": "None",
    "lora_02": "ltx-2.3-22b-distilled-lora-384-1.1.safetensors",
    "lora_03": "None",
    "lora_04": "None"
  }
}
```

**步骤 2**：重新注入脚本

在浏览器控制台重新运行整个脚本，或刷新页面（如使用油猴脚本）。

---

### 4.2 创建自定义节点

如果你想添加新功能（如 LoRA 管理器页面），可以创建 ComfyUI 自定义节点。

**目录结构**：
```
ComfyUI/custom_nodes/ComfyUI-MyExtension/
├── __init__.py
├── my_node.py
├── web/
│   └── my_extension.js
└── js/
    └── lora_manager.js
```

**`__init__.py` 模板**：
```python
from .my_node import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
```

---


我将继续完善自定义节点的注册流程，确保节点能够正确集成到 ComfyUI 系统中。重点是正确设置节点映射和显示名称，以便用户能够轻松识别和使用新创建的节点。

对于前端 JavaScript 开发，我会使用标准 ES6+ 语法，并特别注意 Gradio 的事件系统。关键是确保自定义脚本能够在 Gradio 界面加载完成后正确注入，同时保持与现有组件的兼容性。

如果需要对 `.pyd` 文件进行深入分析，我将使用静态分析方法，包括字符串提取和导入 hook，以避免直接修改二进制文件。这种方法既能获取关键信息，又能保持文件的完整性。

我会特别注意构建过程中的常见陷阱，如 VC++ 运行库缺失、Python 版本不匹配和路径配置错误。对于 Python 扩展模块的编译，需要确保使用正确的工具链和编译器设置。

自定义节点的安装和调试需要遵循严格的步骤，包括目录放置、依赖安装和日志查看。我会提供详细的故障排除指南，帮助开发者快速定位和解决问题。

---

## 5. 调试技巧

### 5.1 Python 后端调试

使用 `pdb` 或 `remote-pdb`：

```python
import pdb; pdb.set_trace()  # 在代码中插入断点

# 或使用 remote-pdb（远程调试）
from remote_pdb import RemotePdb
RemotePdb('localhost', 4444).set_trace()
```

然后连接：
```bash
telnet localhost 4444
```

---

### 5.2 JavaScript 前端调试

**浏览器开发者工具**：
- `F12` 打开控制台
- `Sources` 面板设置断点
- 使用 `debugger;` 语句

```javascript
function applyPreset(presetName) {
  debugger;  // 执行到此处会暂停
  // ... 应用逻辑
}
```

---

### 5.3 网络请求监控

**激活验证请求**：
```
POST https://www.goodhub.ai/api/verify_activation.php
Content-Type: application/x-www-form-urlencoded

machine_id=xxx&activation_code=xxx&product=fixed_ltx_v2.3
```

使用 Fiddler 或浏览器 Network 标签捕获并分析。

---

### 5.4 日志查看

```bash
# 实时查看 ComfyUI 日志
tail -f D:\LTX2.3_v4.0\ComfyUI\logs\comfyui.latest.log

# 搜索特定关键词
grep "LTXVideo" comfyui.log
grep "activation" comfyui.log
```

---

## 6. 贡献流程

### 6.1 分支策略

```
main          - 稳定版，不可直接提交
dev           - 开发主干，集成所有特性
feature/xxx   - 新功能开发
fix/xxx       - Bug 修复
hotfix/xxx    - 紧急修复
```

---

### 6.2 提交流程

```
1. 创建分支：git checkout -b feature/lora-preset-panel
2. 编写代码 + 测试
3. 提交：git commit -m "feat: add lora preset panel"
4. 推送：git push origin feature/lora-preset-panel
5. 创建 PR 到 dev 分支
6. Code Review
7. 合并
```

---

### 6.3 代码规范

- **Python**: 遵循 PEP 8，使用 black 格式化
- **JavaScript**: 使用 Prettier，2 空格缩进
- **提交信息**: 遵循 [Conventional Commits](https://www.conventionalcommits.org/)

```
feat: 添加 LoRA 预设面板
fix: 修复激活验证的并发问题
docs: 更新 README 说明
refactor: 重构配置加载逻辑
test: 添加单元测试
```

---

## 7. 常见问题

### Q1: 编译 `.pyd` 时提示"Unable to find vcvarsall.bat"

**原因**：未安装 Visual Studio 构建工具。

**解决**：
1. 安装 [Build Tools for Visual Studio](https://visualstudio.microsoft.com/zh-hant/downloads/)
2. 选择"C++ 生成工具"工作负荷
3. 重试编译

---

### Q2: 导入自定义节点时找不到模块

**检查**：
```bash
cd D:\LTX2.3_v4.0\ComfyUI
python -c "import sys; print('\n'.join(sys.path))"
```

确保 `custom_nodes/` 在 Python 路径中。

---

### Q3: JavaScript 修改后不生效

**原因**：浏览器缓存。

**解决**：
1. 硬刷新：`Ctrl+Shift+R`
2. 清空缓存：DevTools → Application → Clear storage
3. 禁用缓存：DevTools → Network → Disable cache

---

### Q4: 修改 Python 代码后需要重启

**是的**。ComfyUI 在启动时加载所有节点模块，运行时热重载不支持。

**开发建议**：
- 小步修改，频繁重启测试
- 使用日志输出而不是交互式调试
- 将复杂逻辑拆分为可独立测试的模块

---

## 附录

### A. 有用的资源

| 资源 | 链接 |
|-----|------|
| ComfyUI 文档 | https://comfy.github.io/docs/ |
| Gradio 文档 | https://www.gradio.app/docs/ |
| PyTorch 文档 | https://pytorch.org/docs/stable/index.html |
| LoRA 论文 | https://arxiv.org/abs/2106.09685 |

---

### B. 联系与支持

- **问题反馈**：在 GitHub Issues 中提交
- **讨论交流**：加入 Discord 频道
- **文档更新**：提交 PR 改进本手册

---

*文档版本: v1.0*  
*适用版本: LTX2.3_v4.0*  
*维护者: LTX2.3 开发团队*
