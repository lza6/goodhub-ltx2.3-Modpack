# LoRA 预设配置

本目录存放 LoRA 预设相关的配置文件。

---

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `lora_preset.user.js` | Tampermonkey 油猴脚本（自动注入预设面板） |
| `lora_presets.json` | 预设配置数据（由 `create_lora_preset_panel.py` 生成） |

---

## 🎛️ 使用油猴脚本

### 1. 安装 Tampermonkey

- Chrome: https://chrome.google.com/webstore/detail/tampermonkey
- Firefox: https://addons.mozilla.org/firefox/addon/tampermonkey/
- Edge: Microsoft Edge 内置商店搜索

### 2. 创建脚本

1. 点击 Tampermonkey 图标 → "创建新脚本"
2. 删除默认模板内容
3. 复制 `lora_preset.user.js` 全部内容粘贴
4. 按 `Ctrl+S` 保存

### 3. 测试

访问 `http://127.0.0.1:7966`，右下角应自动出现 LoRA 预设面板。

---

## 🔧 自定义预设

### 方法1：直接修改 JS 文件

编辑 `lora_preset.user.js`，找到 `const LORA_PRESETS` 部分进行修改，保存后刷新页面生效。

### 方法2：使用 JSON 配置（待支持）

未来版本将支持从 `lora_presets.json` 加载预设，无需修改 JS 代码。

---

## 📋 当前内置预设

1. 无LoRA
2. 仅蒸馏LoRA（推荐）
3. 仅Crisp增强
4. IC-LoRA Union
5. 蒸馏+增强
6. 全激活（实验性）

详见 [../docs/PRESET-PANEL.md](../docs/PRESET-PANEL.md)

---

*最后更新: 2026-04-22*
