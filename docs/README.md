# 📚 文档集

本文件夹包含 LTX2.3 改进项目的完整技术文档。

---

## 📖 文档索引

### 用户指南

| 文档 | 简介 | 阅读时间 |
|------|------|---------|
| [激活指南](ACTIVATION.md) | 如何绕过激活验证，永久使用 LTX2.3 | 5 分钟 |
| [LoRA 使用指南](LORA-GUIDE.md) | LoRA 版本管理、兼容性、推荐配置 | 10 分钟 |
| [预设面板说明](PRESET-PANEL.md) | LoRA 一键切换面板的使用与安装 | 8 分钟 |
| [故障排查](TROUBLESHOOTING.md) | 常见问题与快速诊断命令 | 15 分钟 |

### 开发文档

| 文档 | 简介 | 适合读者 |
|------|------|---------|
| [系统架构](ARCHITECTURE.md) | LTX2.3 整体架构与模块说明 | 架构师、开发者 |
| [开发者手册](DEVELOPMENT.md) | 环境搭建、代码规范、贡献流程 | 贡献者 |
| [设置持久化方案](SETTINGS.md) | 全局配置存储设计方案 | 后端开发者 |
| [预设面板 API](PRESET-PANEL.md) | 前端扩展 API 与自定义 | 前端开发者 |

---

## 🎯 阅读路径建议

### 我是普通用户（想快速使用）

```
1. 执行 tools/activation/bypass_activation.py 完成激活
2. 阅读 ACTIVATION.md 了解激活原理
3. 阅读 LORA-GUIDE.md 了解 LoRA 版本
4. 按 README.md 中的步骤使用预设面板
5. 遇到问题查 TROUBLESHOOTING.md
```

---

### 我是开发者（想深入理解或贡献）

```
1. 阅读 ARCHITECTURE.md - 了解系统架构（10分钟）
2. 阅读 DEVELOPMENT.md - 环境搭建与规范（15分钟）
3. 阅读 PRESET-PANEL.md - 了解当前实现（10分钟）
4. 选择感兴趣的问题，从 GitHub Issues 认领
5. 阅读相关源码，提交 Pull Request
```

---

### 我是系统管理员（需要批量部署）

```
1. 阅读 ACTIVATION.md - 理解激活机制
2. 阅读 LORA-GUIDE.md - 梳理版本兼容性
3. 参考 TROUBLESHOOTING.md 的批量处理章节
4. 使用 tools/workflow/inspect_workflow.py 扫描工作流
5. 待 convert_workflows.py 完成后批量修复
```

---

## 📂 文档结构

```
docs/
├── README.md              # 本文档（导航）
├── ACTIVATION.md          # 激活指南 - 用户必读
├── LORA-GUIDE.md          # LoRA指南 - 版本匹配关键
├── PRESET-PANEL.md        # 预设面板 - 功能说明
├── SETTINGS.md            # 设置持久化 - 设计方案
├── TROUBLESHOOTING.md     # 故障排查 - 遇到问题先看这里
├── ARCHITECTURE.md        # 系统架构 - 技术概览
└── DEVELOPMENT.md         # 开发者手册 - 贡献者指南
```

---

## 🔍 快速查找

**问题：无法激活？**  
→ [ACTIVATION.md](ACTIVATION.md#故障排除) 或 [TROUBLESHOOTING.md#激活相关问题](TROUBLESHOOTING.md#1-激活相关问题)

**问题：LoRA 加载失败？**  
→ [LORA-GUIDE.md#版本不匹配问题排查](LORA-GUIDE.md#5-%E7%89%88%E6%9C%AC%E4%B8%8D%E5%8C%B9%E9%85%8D%E9%97%AE%E9%A2%98%E6%8E%92%E6%9F%A5) 或 [TROUBLESHOOTING.md#lora-相关问题](TROUBLESHOOTING.md#2-lora-相关问题)

**问题：预设面板不显示？**  
→ [PRESET-PANEL.md#常见问题](PRESET-PANEL.md#6-常见问题) 或 [TROUBLESHOOTING.md#web-ui-运行问题](TROUBLESHOOTING.md#4-web-ui-运行问题)

**想了解系统架构？**  
→ [ARCHITECTURE.md](ARCHITECTURE.md)

**想为项目做贡献？**  
→ [DEVELOPMENT.md](DEVELOPMENT.md)

---

## 📝 文档贡献

发现文档错误？欢迎提交 Pull Request！

1. Fork 本仓库
2. 创建 feature/doc-* 分支
3. 修改对应 `.md` 文件
4. 提交并推送
5. 创建 PR 到 `main` 分支

**文档规范**：
- 使用 Markdown 标准语法
- 中文文档使用简体中文
- 代码块标注语言类型（如 ```python）
- 截图保存为 `.png` 并放在 `docs/assets/`（如需要）

---

## 🔄 文档版本

本仓库版本号与项目版本号同步：

| 版本 | 更新日期 | 变更 |
|------|---------|------|
| v1.0 | 2026-04-22 | 初始版本，完整文档集 |

---

*维护者: LTX2.3 改进项目团队*  
*最后更新: 2026-04-22*
