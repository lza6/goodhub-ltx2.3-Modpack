# 设置管理工具

本目录提供 LTX2.3 用户设置持久化的辅助工具。

---

## 📋 问题背景

当前 LTX2.3 的**用户设置不会在重启后保持**：

```
今天:
  [✓] 勾选"显存自动清理"
  [✓] 设置 FPS=24
  [✓] 分辨率=1024x576
  → 关闭 ComfyUI

明天:
  [ ] 显存自动清理未勾选
  [ ] FPS=16 (默认)
  [ ] 分辨率=512x512
  → 需要重新配置
```

**根本原因**：LTXVideo 的参数绑定在**工作流文件**（.json）中，而非全局配置文件。未保存工作流则设置丢失。

---

## 🔧 工具说明

### fix_settings_persistence.py

**用途**：诊断当前设置持久化状态，提供修复建议。

**用法**：
```bash
python tools/settings/fix_settings_persistence.py
```

**功能**：
- 检查 `ComfyUI/user/default/comfy.settings.json` 是否包含 LTX 设置
- 扫描工作流文件，统计未保存的修改
- 提供设置建议

---

### auto_save_settings.bat

**用途**：定时提醒用户保存工作流（每5分钟）。

**使用方法**：
```batch
# 方式1: 直接双击运行
tools\settings\auto_save_settings.bat

# 方式2: 命令行启动
cd tools\settings
auto_save_settings.bat
```

**效果**：
- 每5分钟弹窗提醒："请按 Ctrl+S 保存当前工作流"
- 在系统托盘显示倒计时图标

**注意**：这是**提醒工具**，不能自动保存（ComfyUI 无公开 API）。

---

## 💡 推荐工作流

### 日常使用

```
1. 启动 ComfyUI
2. 在后台运行 auto_save_settings.bat（可选）
3. 调整 LoRA、分辨率等参数
4. ⚠️ 生成前务必按 Ctrl+S 保存工作流！ ← 关键步骤
5. 开始生成
```

---

## 🚀 长期方案

设置持久化系统正在设计中，详见：[docs/SETTINGS.md](../docs/SETTINGS.md)

**计划功能**：
- 全局配置文件 `~/.ltx_config/settings.json`
- Gradio 侧边栏设置面板
- 工作流加载时自动注入默认值
- 自定义节点方式集成

---

## ❓ 常见问题

**Q: 为什么不能自动保存？**  
A: ComfyUI 没有暴露工作流保存的 HTTP API，只能前端模拟按键（不稳定）或手动保存。

**Q: auto_save_settings.bat 会影响性能吗？**  
A: 不会，它只在5分钟时弹一次提示框，无后台轮询。

**Q: 设置持久化系统何时发布？**  
A: 开发计划中，预计在第二阶段（P1）实现。

---

## 📖 相关文档

- [docs/SETTINGS.md](../docs/SETTINGS.md) - 完整设计方案
- [docs/TROUBLESHOOTING.md](../docs/TROUBLESHOOTING.md) - 故障排查

---

*最后更新: 2026-04-22*
