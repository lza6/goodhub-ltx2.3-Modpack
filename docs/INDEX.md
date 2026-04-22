# 🚀 快速开始

5 分钟完成激活并开始使用 LoRA 预设面板。

---

## 步骤 1: 激活系统（1分钟）

```bash
# 1. 进入项目目录
cd D:\LTX2.3_v4.0

# 2. 运行激活脚本（Windows 直接双击 bat 文件）
python tools\activation\bypass_activation.py

# 3. 查看输出（应看到 SUCCESS）
```

**预期输出**：
```
[OK] 机器指纹: xxxxxx
[OK] 激活码: LTX2.3-ACTIVATION-BYPASS-2026
[SUCCESS] 激活绕过完成！
```

---

## 步骤 2: 启动 ComfyUI（1分钟）

```bash
# 方式1: 使用启动脚本（推荐）
启动脚本.bat

# 方式2: 命令行
python main.py
```

等待日志显示：
```
To access the interface, click here: http://127.0.0.1:7966
```

---

## 步骤 3: 注入预设面板（1分钟）

### 方法 A: 临时注入（每次启动需重做）

1. 打开浏览器访问 `http://127.0.0.1:7966`
2. 按 `F12` 打开开发者工具
3. 进入 `Console` 标签
4. 复制 `tools/lora/lora_preset_inject.js` 全部内容
5. 粘贴并回车

✅ 右下角出现浮动面板即成功。

---

### 方法 B: 永久注入（推荐⭐）

1. 安装 [Tampermonkey](https://www.tampermonkey.net/) 扩展
2. 点击扩展图标 → "创建新脚本"
3. 复制 `presets/lora_preset.user.js` 全部内容粘贴
4. `Ctrl+S` 保存
5. 刷新 Web UI 页面，面板自动出现

---

## 步骤 4: 使用预设（30秒）

1. 在右下角面板中选择一个预设（如"仅蒸馏LoRA"）
2. 点击"🚀 应用预设"
3. 按 `Ctrl+S` 保存工作流（**关键步骤**）
4. 开始生成视频

---

## ✅ 验证成功

- 没有激活弹窗
- 右下角有 LoRA 预设面板
- 应用预设后节点参数更新
- 保存工作流后刷新页面，设置保留

---

## 🆘 遇到问题？

**激活失败** → 查看 [docs/ACTIVATION.md](docs/ACTIVATION.md)

**LoRA 报错** → 查看 [docs/LORA-GUIDE.md](docs/LORA-GUIDE.md)

**面板不显示** → 查看 [docs/PRESET-PANEL.md](docs/PRESET-PANEL.md)

**其他问题** → 查看 [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

## 📚 详细文档

- [完整使用指南](docs/README.md) - 所有文档导航
- [系统架构](docs/ARCHITECTURE.md) - 了解技术原理
- [开发者手册](docs/DEVELOPMENT.md) - 如果想贡献代码

---

**开始享受 LTX2.3 吧！** 🎉
