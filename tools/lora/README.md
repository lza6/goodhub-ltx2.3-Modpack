# LoRA 预设工具

本目录提供 LoRA 配置管理相关的工具和脚本。

---

## 🎛️ 工具列表

| 文件 | 说明 | 使用方式 |
|------|------|---------|
| `create_lora_preset_panel.py` | Python 脚本：生成预设面板配置 | 命令行执行 |
| `lora_preset_inject.js` | JavaScript：手动注入到浏览器控制台 | F12 → Console |
| `lora_presets.json` | JSON：预设配置数据（生成） | 由 Python 脚本生成 |

---

## 🚀 快速使用

### 1. 浏览器控制台注入（推荐）

这是**最快**的试用方式，无需任何安装：

```javascript
// 步骤1: 启动 ComfyUI 并打开 Web UI
// 步骤2: 按 F12 打开开发者工具
// 步骤3: 切换到 Console 标签
// 步骤4: 复制 tools/lora/lora_preset_inject.js 全部内容
// 步骤5: 粘贴到控制台，按回车

// 看到 "✅ LoRA预设面板已加载！" 即成功
```

**操作**：
1. 在右下角浮动面板中选择预设
2. 点击"应用预设"按钮
3. 按 `Ctrl+S` 保存工作流

---

### 2. 油猴脚本（永久方案）

详细步骤参见 `presets/lora_preset.user.js` 的注释说明。

**优势**：自动注入，无需每次手动操作。

---

## 📦 预设配置

当前内置 6 种预设：

| 预设名 | LoRA 组合 | 说明 | 显存需求 |
|--------|----------|------|---------|
| 无LoRA | 全部 None | 纯净基线，最快速度 | ~12 GB |
| 仅蒸馏LoRA | lora_02: distilled | 推荐日常使用 | ~20 GB |
| 仅Crisp增强 | lora_02: Crisp | 画质增强 | ~13 GB |
| IC-LoRA Union | lora_02: ic-lora | 深度+边缘控制 | ~13 GB |
| 蒸馏+增强 | l02: distilled + l03: Crisp | 平衡画质与速度 | ~21 GB |
| 全激活 | 3个LoRA全启用 | 实验性，最高画质 | 32GB+ |

**显存估算公式**：
```
基础模型: ~12 GB
+ 蒸馏版: +7.6 GB
+ Crisp增强: +0.7 GB
+ IC-LoRA: +0.65 GB
= 总计
```

---

## 🔧 自定义预设

### 方法1：修改注入脚本

编辑 `lora_preset_inject.js`，找到 `const LORA_PRESETS` 部分：

```javascript
const LORA_PRESETS = {
    "我的预设": {
        "description": "自定义描述",
        "loras": {
            "lora_01": "None",
            "lora_02": "ltx-2.3-22b-distilled-lora-384-1.1.safetensors",
            "lora_03": "LTX2.3_Crisp_Enhance.safetensors",
            "lora_04": "None"
        }
    },
    // ... 其他预设
};
```

重新注入即可生效。

---

### 方法2：使用 Python 生成器

```bash
# 交互式创建自定义预设
python tools/lora/create_lora_preset_panel.py
```

该脚本会：
1. 扫描 `ComfyUI/models/loras/` 目录
2. 列出可用 LoRA 文件
3. 交互式选择组合
4. 生成新的 `lora_presets.json` 或更新 JS 文件

---

## 🎯 技术原理

### 节点查找逻辑

```javascript
function findAndSetWidget(node, slotName, value) {
    for (const w of node.widgets || []) {
        if (w.name === slotName || w.name?.includes(slotName)) {
            w.setValue(value);  // 更新 widget 值
            triggerNodeUpdate(node);  // 触发重算
            return true;
        }
    }
    return false;
}
```

### 更新触发

修改 `widget.value` 后需要触发 `change` 事件，Gradio 才会重新渲染：

```javascript
const event = new Event('change', { bubbles: true });
node.widgets[0].element.dispatchEvent(event);
```

---

## 🐛 已知问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 面板不显示 | 脚本注入失败 | 刷新页面，检查控制台错误 |
| 应用后节点未更新 | 节点类型不匹配 | 确认是 LTXVideo 节点的 Lora Loader |
| 刷新后设置丢失 | 未保存工作流 | 应用预设后按 `Ctrl+S` |
| 油猴脚本不自动注入 | 匹配规则不符 | 检查 `@match` 是否包含当前 URL |

---

## 📖 详细文档

- [docs/PRESET-PANEL.md](../docs/PRESET-PANEL.md) - API 与扩展指南
- [docs/LORA-GUIDE.md](../docs/LORA-GUIDE.md) - LoRA 版本兼容性

---

## 🛠️ 开发调试

### 调试模式

在 `lora_preset_inject.js` 开头添加：

```javascript
const DEBUG = true;

function debug(...args) {
    if (DEBUG) console.log('[LTXPreset]', ...args);
}
```

### 检查节点结构

在控制台运行：
```javascript
// 打印所有 LTXVideo 节点的 widget
const graph = window.graph || app?.graph;
graph.nodes.forEach(n => {
    if (n.type?.includes('LTX')) {
        console.log(n.id, n.widgets?.map(w => w.name));
    }
});
```

---

## 🔮 未来计划

- [ ] 预设云端同步
- [ ] 显存实时预估显示
- [ ] 预设导出/导入（JSON 文件）
- [ ] 快捷键支持（数字键 1-6）
- [ ] 工作流快照与撤销

---

*最后更新: 2026-04-22*
