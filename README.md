<<<<<<< HEAD
# LTX2.3 改进工具箱

> **版本**: 1.0  
**兼容**: LTX2.3_v4.0 (基于 ComfyUI 自定义分支)  
**维护**: 社区贡献  

---

## 📖 项目简介

LTX2.3 是基于 ComfyUI 的图生视频生成系统。本仓库提供了一系列改进工具、脚本和文档，解决原版中的激活验证、设置持久化、LoRA管理等痛点问题。

### 核心功能

| 功能 | 说明 | 状态 |
|-----|------|------|
| 🔓 激活绕过 | 本地生成激活文件，无需在线验证 | ✅ 可用 |
| 🎛️ LoRA预设面板 | Web UI 中一键切换LoRA组合 | ✅ 可用 |
| ⚙️ 设置持久化 | 记忆用户偏好，自动填充到工作流 | 🚧 设计中 |
| 🔄 工作流转换 | 批量修复旧版工作流的LoRA版本不匹配 | ⏳ 待实现 |

---

## 🚀 快速开始

### 1. 激活系统（首次必须）

```bash
# 进入项目目录
cd D:\LTX2.3_v4.0

# 运行激活脚本（Windows）
tools\activation\bypass_activation.py

# 或使用一键批处理
tools\activation\run_bypass_activation.bat
```

> ✅ 激活后重启 Web UI，不再提示激活验证

详细步骤参见：[docs/ACTIVATION.md](docs/ACTIVATION.md)

---

### 2. 使用 LoRA 预设面板

**方法A：控制台注入（临时）**

1. 启动 ComfyUI：`python main.py` 或 `scripts\launch.bat`
2. 打开浏览器访问 http://127.0.0.1:7966
3. 按 `F12` 打开开发者工具 → Console 标签
4. 粘贴 `tools\lora\lora_preset_inject.js` 全部内容 → 回车
5. 右下角出现 LoRA 预设面板，选择预设并点击"应用"

**方法B：油猴脚本（永久）**

1. 安装 [Tampermonkey](https://www.tampermonkey.net/) 浏览器扩展
2. 打开扩展 → 创建新脚本
3. 复制 `presets\lora_preset.user.js` 全部内容粘贴
4. 保存（Ctrl+S），访问 http://127.0.0.1:7966 时自动注入

详细说明：[docs/PRESET-PANEL.md](docs/PRESET-PANEL.md)

---

### 3. 修复 LoRA 版本不匹配

如果工作流报错 `Value not in list: lora_03: 'xxx' not in [...]`：

```bash
# 分析工作流结构
python tools\workflow\inspect_workflow.py workflows\examples\LTX2_3_a2v.json

# 等待 convert_workflows.py 实现后批量转换
python tools\workflow\convert_workflows.py workflows\*.json
```

临时方案：在 Web UI 的 Lora Loader 节点中手动将 LoRA 设为 `None`。

---

## 📂 目录结构

```
LTX2.3_v4.0/
├── README.md                # 项目入口（本文件）
├── CHANGELOG.md             # 版本更新日志
├── LICENSE                  # 开源协议
├── .gitignore              # Git忽略规则
│
├── docs/                   # 📚 完整文档
│   ├── README.md           # 文档导航
│   ├── ACTIVATION.md       # 激活绕过指南
│   ├── LORA-GUIDE.md       # LoRA版本管理与使用
│   ├── PRESET-PANEL.md     # 预设面板使用与开发
│   ├── SETTINGS.md         # 设置持久化方案
│   ├── TROUBLESHOOTING.md  # 常见问题与诊断
│   ├── DEVELOPMENT.md      # 开发者手册
│   └── ARCHITECTURE.md     # 系统架构说明
│
├── tools/                  # 🔧 核心工具脚本
│   ├── activation/         # 激活相关工具
│   │   ├── bypass_activation.py
│   │   ├── run_bypass_activation.bat
│   │   └── README.md
│   ├── workflow/           # 工作流处理工具
│   │   ├── inspect_workflow.py
│   │   ├── convert_workflows.py
│   │   └── README.md
│   ├── settings/           # 设置管理工具
│   │   ├── fix_settings_persistence.py
│   │   └── auto_save_settings.bat
│   ├── lora/               # LoRA相关工具
│   │   ├── create_lora_preset_panel.py
│   │   └── lora_preset_inject.js
│   └── README.md           # 工具集合说明
│
├── scripts/                # 🎯 用户快捷脚本
│   ├── quick_activate.bat  # 一键激活+启动
│   ├── launch.bat          # 启动WebUI
│   └── README.md
│
├── presets/                # 🎛️ LoRA预设配置
│   ├── lora_presets.json   # 预设定义（待生成）
│   ├── lora_preset.user.js # 油猴永久脚本
│   └── README.md
│
├── workflows/              # 📋 工作流资源
│   ├── examples/           # 官方示例工作流
│   │   ├── a2v.json        # 文生视频
│   │   ├── i2v.json        # 图生视频
│   │   └── ...
│   ├── templates/          # 标准模板（待创建）
│   │   ├── baseline.json
│   │   └── ...
│   └── README.md
│
├── ComfyUI/                # ComfyUI 主程序（保持原位）
│   ├── custom_nodes/
│   │   └── ComfyUI-LTXVideo/
│   └── models/
│       ├── loras/         # LoRA模型存储
│       ├── checkpoints/   # 主模型
│       └── vae/
│
└── verify_docs.py          # 文档完整性验证脚本
```

---

## 🔑 核心工具列表

| 工具 | 路径 | 功能 |
|------|------|------|
| **bypass_activation.py** | `tools/activation/` | 本地生成激活文件，绕过在线验证 |
| **lora_preset_inject.js** | `tools/lora/` | 浏览器控制台注入LoRA预设面板 |
| **lora_preset.user.js** | `presets/` | Tampermonkey油猴脚本（自动注入） |
| **inspect_workflow.py** | `tools/workflow/` | 分析工作流结构，诊断LoRA版本 |
| **create_lora_preset_panel.py** | `tools/lora/` | 生成自定义预设面板脚本 |

---

## 📖 文档导航

### 新用户必读

1. 📘 **[激活指南](docs/ACTIVATION.md)** - 3分钟完成系统激活
2. 📗 **[LoRA使用指南](docs/LORA-GUIDE.md)** - 了解LoRA版本与兼容性
3. 📙 **[故障排查](docs/TROUBLESHOOTING.md)** - 常见问题快速解决

### 开发者参考

1. 📕 **[预设面板API](docs/PRESET-PANEL.md)** - 扩展面板功能
2. 📔 **[系统架构](docs/ARCHITECTURE.md)** - 理解代码结构
3. 📓 **[开发者手册](docs/DEVELOPMENT.md)** - 环境搭建与贡献流程

---

## ⚡ 一键操作

### Windows 用户

```batch
:: 激活并启动
tools\activation\run_bypass_activation.bat
scripts\launch.bat

:: 浏览器访问
http://127.0.0.1:7966
```

### 高级用户

```bash
# Python环境激活
cd D:\LTX2.3_v4.0
python tools/activation/bypass_activation.py

# 启动ComfyUI
python main.py
```

---

## ❓ 常见问题

**Q: 激活后仍看到"在线验证失败"警告？**  
A: 这是正常现象，只要最终显示"已激活"即可，警告可忽略。

**Q: LoRA预设面板不显示？**  
A: 确保脚本注入成功，检查浏览器控制台有无错误。刷新页面重试。

**Q: 工作流提示LoRA文件不存在？**  
A: 使用 `inspect_workflow.py` 分析，或手动在Lora Loader中设为None。

更多问题参见 **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)**

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

请阅读 **[DEVELOPMENT.md](docs/DEVELOPMENT.md)** 了解：
- 代码规范
- 分支策略
- 提交信息格式
- 开发环境搭建

---

## ⚠️ 免责声明

本项目工具仅供**研究学习**使用，请遵守相关软件许可协议。使用本工具产生的一切后果由使用者自行承担。

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🔗 相关链接

- **ComfyUI 官方文档**: https://comfy.github.io/docs/
- **LTXVideo 节点**: https://github.com/comfyanonymous/ComfyUI_LTXVideo
- **LoRA 论文**: https://arxiv.org/abs/2106.09685

---

**提示**: 建议先阅读 `docs/README.md` 了解完整文档结构，或从 [ACTIVATION.md](docs/ACTIVATION.md) 开始使用。
=======
# goodhub-ltx2.3-Modpack
goodhub.ai版本的绕过LTX整合包（绕过了激活图生视频），利用本地先检查缓存/激活文件，然后进行在线验证。docs文件夹下内置了4.0整合包升级迭代文档
>>>>>>> 3b1b7529a99c24d316c2f2977492862fcac85160
