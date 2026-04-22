# 🎛️ LoRA 预设面板

LoRA 预设面板允许你在 Web UI 中一键切换不同的 LoRA 组合，无需逐个修改节点。

---

## 🚀 快速开始

### 方式一：控制台注入（临时）

每次打开 Web UI 都需要执行一次：

1. 启动 ComfyUI 并访问 http://127.0.0.1:7966
2. 按 `F12` 打开开发者工具
3. 进入 `Console` 标签
4. 复制 `tools/lora/lora_preset_inject.js` 全部内容
5. 粘贴到控制台并按回车

✅ 右下角出现浮动面板即成功。

---

### 方式二：油猴脚本（永久）

只需安装一次，自动永久生效：

1. 安装 [Tampermonkey](https://www.tampermonkey.net/) 浏览器扩展
2. 点击扩展图标 → "创建新脚本"
3. 删除默认内容，复制 `presets/lora_preset.user.js` 全部内容粘贴
4. 按 `Ctrl+S` 保存
5. 访问 `http://127.0.0.1:7966` 时自动注入

---

## 📋 内置预设

| 预设名 | 描述 | LoRA 配置 |
|--------|------|----------|
| **无LoRA** | 清空所有 LoRA，仅使用基础模型 | lora_02-04: None |
| **仅蒸馏LoRA** | 蒸馏版 LoRA，速度较快（推荐） | lora_02: 蒸馏版 |
| **仅Crisp增强** | 画质增强 LoRA | lora_02: Crisp Enhance |
| **IC-LoRA Union** | 支持深度+边缘控制 | lora_02: IC-LoRA |
| **蒸馏+增强** | 双 LoRA 组合 | l02: 蒸馏 + l03: Crisp |
| **全激活** | 所有槽位激活，需 32GB+ 显存 | 3个LoRA全启用 |

---

## 🎯 使用方法

1. **选择预设**：在面板下拉菜单中选择一个预设
2. **查看描述**：下方显示该预设的说明
3. **应用**：点击"🚀 应用预设"按钮
4. **保存**：按 `Ctrl+S` 保存工作流（重要！）
5. **生成**：开始生成视频

> ⚠️ **注意**：应用预设后，必须保存工作流才会持久化。否则刷新页面后设置会丢失。

---

## 🔧 自定义预设

### 修改现有预设

编辑 `tools/lora/lora_preset_inject.js`：

```javascript
const LORA_PRESETS = {
    "我的预设": {
        "description": "自定义描述",
        "loras": {
            "lora_01": "None",
            "lora_02": "ltx-2.3-22b-distilled-lora-384-1.1.safetensors",
            "lora_03": "None",
            "lora_04": "None"
        }
    },
    // ... 其他预设保持不变
};
```

重新注入脚本即可生效。

---

### 创建全新预设

在 `LORA_PRESETS` 对象中添加新条目：

```javascript
const LORA_PRESETS = {
    // ... 原有预设

    "实验性组合": {
        "description": "尝试新的 LoRA 组合",
        "loras": {
            "lora_01": "None",
            "lora_02": "你的loRA文件名.safetensors",
            "lora_03": "另一个文件.safetensors",
            "lora_04": "None"
        }
    }
};
```

---

## 🎨 面板功能

### 当前功能

- ✅ 6 种预设选择
- ✅ 预设描述显示
- ✅ 一键应用到所有 Lora Loader 节点
- ✅ 状态反馈（成功/失败计数）
- ✅ 最小化按钮（折叠面板）

### 计划功能

- ⏳ 自定义预设保存到本地存储
- ⏳ 显存需求实时预估
- ⏳ 工作流快照（撤销）
- ⏳ 快捷键支持（1-6 数字键）

---

## 🐛 常见问题

### Q1: 面板不显示

**检查**：
1. 脚本是否成功注入？查看控制台有无错误
2. 刷新页面重新注入
3. 确认 ComfyUI 已完全加载（等待几秒再注入）

---

### Q2: 应用预设后节点没有变化

**原因**：
- 页面中可能没有 LTXVideo 节点
- 或节点类型不匹配

**解决**：
1. 在 LTXVideo 标签页创建至少一个 Lora Loader 节点
2. 打开浏览器控制台，运行：
   ```javascript
   console.log(window.graph?.nodes || app?.graph?.nodes)
   ```
   检查是否有 LTXVideo 相关节点

---

### Q3: 刷新页面后设置丢了

**原因**：未保存工作流。

**解决**：
- 应用预设后立即按 `Ctrl+S` 保存
- 或点击界面上的"保存工作流"按钮（如果有）

---

### Q4: 油猴脚本不自动运行

**检查**：
1. Tampermonkey 是否已启用？
2. 脚本状态是否为"已启用"？
3. `@match` 规则是否匹配当前 URL？应包含 `http://127.0.0.1:7966/*`

**修复**：编辑油猴脚本，确保：
```javascript
// @match        http://127.0.0.1:7966/*
// @match        http://localhost:7966/*
// @match        http://0.0.0.0:7966/*
```

---

### Q5: LoRA 文件不匹配错误

```
Value not in list: 'ltx-2-19b-xxx.safetensors' not in [...]
```

**原因**：工作流中的 LoRA 文件名与磁盘文件不匹配。

**解决**：
1. 查看 [LORA-GUIDE.md](LORA-GUIDE.md) 了解版本兼容性
2. 使用"无LoRA"预设清空，再选择正确的 LoRA
3. 或手动在节点中选择正确的文件

---

## 🔧 技术细节

### 如何修改面板位置

编辑 `lora_preset_inject.js`，找到 `injectPanel()` 函数中的 CSS：

```javascript
root.style.cssText = `
    position:fixed;
    bottom:20px;   /* 距离底部 */
    right:20px;    /* 距离右侧 */
    /* ... */
`;
```

想要左上角：
```javascript
root.style.cssText = `
    position:fixed;
    bottom:auto;
    top:20px;
    right:auto;
    left:20px;
    /* ... */
`;
```

---

### 如何修改面板样式

样式定义在注入脚本的 `root.style.cssText` 部分，可以修改：

- `width`: 面板宽度（默认 300px）
- `background`: 背景色（默认深色半透明）
- `border`: 边框（默认粉色 #ff6b9d）
- `z-index`: 层级（默认 999999）

---

## 📖 API 参考

如需扩展面板功能，参考 [docs/PRESET-PANEL-API.md](../docs/PRESET-PANEL-API.md)

**核心函数**：

| 函数 | 说明 |
|------|------|
| `LTXPresetPanel.inject()` | 手动注入面板 |
| `LTXPresetPanel.apply(name)` | 应用预设 |
| `LTXPresetPanel.addCustomPreset()` | 添加自定义预设 |
| `LTXPresetPanel.getCurrentPreset()` | 获取当前预设 |

---

## 🎨 预设示例

### 示例1：影视风格

```javascript
"影视风格": {
    "description": "电影感画面，高对比度",
    "loras": {
        "lora_02": "ltx-2.3-22b-distilled-lora-384-1.1.safetensors",
        "lora_03": "LTX2.3_Crisp_Enhance.safetensors",
        "lora_04": "None"
    }
}
```

### 示例2：快速预览

```javascript
"快速预览": {
    "description": "低步数快速测试",
    "loras": {
        "lora_02": "None",
        "lora_03": "None",
        "lora_04": "None"
    }
}
```

---

## 🤝 贡献

如果你有好的 LoRA 组合方案，欢迎提交 PR：

1. Fork 本项目
2. 修改 `lora_preset_inject.js` 添加预设
3. 测试效果
4. 提交 Pull Request

---

## 📝 更新日志

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-04-22 | v1.0 | 初始版本，6个内置预设 |

---

*文档关联: [LORA-GUIDE.md](LORA-GUIDE.md) | [TROUBLESHOOTING.md](../docs/TROUBLESHOOTING.md)*
