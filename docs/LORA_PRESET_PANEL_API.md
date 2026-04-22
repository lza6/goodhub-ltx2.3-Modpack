# LoRA 预设面板 API 与扩展指南

> **版本**: 1.0  
> **创建日期**: 2026-04-22  
> **相关文件**: `lora_preset_inject.js`, `lora_preset.user.js`

---

## 目录

1. [面板架构](#1-面板架构)
2. [JavaScript API](#2-javascript-api)
3. [自定义预设](#3-自定义预设)
4. [扩展开发](#4-扩展开发)
5. [集成到 ComfyUI](#5-集成到-comfyui)

---

## 1. 面板架构

### 1.1 文件结构

```
ltx-preset-panel/
├── lora_preset_inject.js    # 基础注入脚本（控制台用）
├── lora_preset.user.js      # Tampermonkey 版本（自动注入）
├── presets.js               # 预设配置（可独立加载）
└── styles.css               # 样式文件（可选）
```

### 1.2 运行时状态

```javascript
// 面板挂载到 window 对象，便于调试
window.LTX_PRESET_PANEL = {
  status: 'ready',        // ready | injecting | error
  presets: {...},         // 当前预设配置
  currentPreset: null,    // 当前选中的预设名
  appliedCount: 0,        // 本次会话已应用的次数
  version: '1.0'
}
```

---

## 2. JavaScript API

### 2.1 核心函数

#### `LTXPresetPanel.inject()`

手动注入面板到页面。

```javascript
// 调用方式
LTXPresetPanel.inject();

// 参数
// 无

// 返回值
// Promise<void> - 注入完成时 resolve
```

**示例**：
```javascript
// 在浏览器控制台中
LTXPresetPanel.inject()
  .then(() => console.log('面板已注入'))
  .catch(err => console.error('注入失败:', err));
```

---

#### `LTXPresetPanel.apply(presetName)`

应用指定预设到当前工作流。

```javascript
LTXPresetPanel.apply('仅蒸馏LoRA');
```

**内部流程**：
1. 获取当前工作流图数据
2. 查找所有 Lora Loader 节点
3. 遍历节点 widgets，匹配 `lora_01` - `lora_04`
4. 调用 `setWidgetValue()` 更新值
5. 触发节点更新事件
6. 返回更新计数

---

#### `LTXPresetPanel.getCurrentPreset()`

获取当前选中的预设配置。

```javascript
const preset = LTXPresetPanel.getCurrentPreset();
console.log(preset.loras);
// { lora_01: "None", lora_02: "xxx.safetensors", ... }
```

---

#### `LTXPresetPanel.addCustomPreset(name, config)`

添加自定义预设（需要用户权限）。

```javascript
LTXPresetPanel.addCustomPreset('我的组合', {
  description: '自定义 LoRA 组合',
  loras: {
    lora_01: 'None',
    lora_02: 'ltx-2.3-22b-distilled-lora-384-1.1.safetensors',
    lora_03: 'LTX2.3_Crisp_Enhance.safetensors',
    lora_04: 'None'
  }
});
```

---

### 2.2 事件系统

面板通过 CustomEvent 广播状态变化：

```javascript
// 监听预设切换
document.addEventListener('lora-preset-change', (e) => {
  console.log('新预设:', e.detail.presetName);
});

// 监听应用完成
document.addEventListener('lora-preset-applied', (e) => {
  console.log(`已更新 ${e.detail.updatedNodes} 个节点`);
});

// 监听错误
document.addEventListener('lora-preset-error', (e) => {
  console.error('错误:', e.detail.message);
});
```

---

### 2.3 配置对象结构

```typescript
interface LoraPreset {
  description: string;
  loras: {
    lora_01: string;  // 通常为 "None"
    lora_02: string;  // 主 LoRA 槽位
    lora_03: string;  // 第二 LoRA
    lora_04: string;  // 第三 LoRA
  };
}

interface PanelConfig {
  container?: HTMLElement;  // 自定义挂载点
  position?: 'bottom-right' | 'bottom-left' | 'top-right' | 'top-left';
  theme?: 'dark' | 'light';
  onApplied?: (count: number) => void;
  onError?: (error: Error) => void;
}
```

---

## 3. 自定义预设

### 3.1 预设配置文件格式

创建 `my_presets.json`：

```json
{
  "version": "1.0",
  "presets": [
    {
      "name": "我的预设1",
      "description": "蒸馏版 + 增强，推荐配置",
      "loras": {
        "lora_01": "None",
        "lora_02": "ltx-2.3-22b-distilled-lora-384-1.1.safetensors",
        "lora_03": "LTX2.3_Crisp_Enhance.safetensors",
        "lora_04": "None"
      },
      "generation": {
        "steps": 20,
        "cfg": 3.5
      }
    }
  ]
}
```

### 3.2 加载自定义预设

```javascript
// 方法1：通过脚本加载
fetch('/custom_presets.json')
  .then(r => r.json())
  .then(config => {
    Object.entries(config.presets).forEach(([name, preset]) => {
      LTXPresetPanel.addCustomPreset(name, preset);
    });
  });

// 方法2：修改 lora_preset_inject.js 的 LORA_PRESETS 常量
// 然后重新注入脚本
```

---

## 4. 扩展开发

### 4.1 添加新功能按钮

在面板 HTML 中添加：

```javascript
// 扩展 injectPanel 函数
function injectPanel() {
  // ... 原有代码 ...

  root.innerHTML += `
    <button id="lora-reset-btn" style="...">
      🔄 重置为默认
    </button>
  `;

  document.getElementById('lora-reset-btn').onclick = () => {
    if (confirm('确定重置所有 LoRA 为 None 吗？')) {
      LTXPresetPanel.apply('无LoRA');
    }
  };
}
```

---

### 4.2 集成显存估算器

```javascript
class VramEstimator {
  static estimate(loras, resolution, frames) {
    // 基础显存 (2.3 22b 模型)
    let vram = 12; // GB

    // 每个 LoRA 的增量
    const loraSizes = {
      'distilled': 7.6,
      'crisp': 0.7,
      'ic-lora': 0.65
    };

    for (const [slot, file] of Object.entries(loras)) {
      if (file === 'None') continue;

      if (file.includes('distilled')) vram += loraSizes.distilled;
      else if (file.includes('Crisp')) vram += loraSizes.crisp;
      else if (file.includes('ic-lora')) vram += loraSizes.ic;
    }

    // 分辨率调整
    const pixelCount = (resolution.width * resolution.height * frames) / 1e6;
    vram += pixelCount * 0.015;

    return Math.round(vram * 100) / 100;
  }
}

// 在预设选择时显示
select.onchange = function() {
  const preset = LORA_PRESETS[this.value];
  const est = VramEstimator.estimate(preset.loras, {width:1024, height:576}, 129);
  desc.textContent = `${preset.description} (预估显存: ${est} GB)`;
};
```

---

### 4.3 工作流快照功能

```javascript
class WorkflowSnapshot {
  constructor() {
    this.history = [];
    this.maxSize = 5;
  }

  save() {
    const graph = getGraphData();
    this.history.push(JSON.stringify(graph));
    if (this.history.length > this.maxSize) {
      this.history.shift();
    }
  }

  restore(index) {
    if (this.history[index]) {
      const data = JSON.parse(this.history[index]);
      applyGraphData(data);
    }
  }
}

// 应用预设前自动保存
applyBtn.onclick = async () => {
  snapshot.save();
  // ... 应用逻辑 ...
};
```

---

## 5. 集成到 ComfyUI

### 5.1 作为自定义节点发布

创建 `ComfyUI-LTXPreset` 自定义节点：

```
ComfyUI/custom_nodes/ComfyUI-LTXPreset/
├── __init__.py           # 节点注册
├── ltx_preset_server.py  # 后端 API
├── lora_presets.json     # 预设配置
└── web/
    └── ltx_preset.js     # 前端脚本（自动注入）
```

**`__init__.py`**：
```python
from .ltx_preset_server import register_ltx_preset_api

# 注册 REST API 路由
register_ltx_preset_api()

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
WEB_DIRECTORY = "./web"
```

**`ltx_preset_server.py`**：
```python
from aiohttp import web

 routes = web.RouteTableDef()

 @routes.get("/ltx/presets")
 async def get_presets(request):
     """获取可用预设列表"""
     return web.json_response(LORA_PRESETS)

 @routes.post("/ltx/apply")
 async def apply_preset(request):
     """应用预设到当前图"""
     data = await request.json()
     preset_name = data.get('preset')
     # ... 应用逻辑 ...
     return web.json_response({"success": True, "count": updated})

 def register_ltx_preset_api():
     from server import server
     server.routes.append(routes)
```

---

### 5.2 前端自动注入

在 `web/ltx_preset.js` 中：

```javascript
// 检查是否 LTXVideo 标签页存在
function waitForLTXTab() {
  const tabs = document.querySelectorAll('.tab-nav button');
  for (let tab of tabs) {
    if (tab.textContent.includes('LTX') || tab.textContent.includes('视频')) {
      // 找到 LTX 标签页，注入面板
      injectPanel(tab);
      return;
    }
  }
  setTimeout(waitForLTXTab, 500);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', waitForLTXTab);
} else {
  waitForLTXTab();
}
```

---

### 5.3 通过 ComfyUI API 通信

```javascript
// 获取当前图数据
async function getGraphData() {
  const response = await fetch('/prompt', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({get_graph: true})
  });
  return await response.json();
}

// 更新节点参数
async function setNodeParam(nodeId, widgetName, value) {
  const response = await fetch('/prompt', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      set_node: nodeId,
      widget: widgetName,
      value: value
    })
  });
  return await response.json();
}
```

---

## 6. 调试与开发

### 6.1 调试模式

在脚本开头添加：

```javascript
const DEBUG = true;

function debug(...args) {
  if (DEBUG) {
    console.log('[LTXPreset]', ...args);
  }
}
```

### 6.2 检查节点结构

```javascript
// 打印所有 LTXVideo 节点
function dumpLTXNodes() {
  const graph = window.graph || app?.graph;
  if (!graph) {
    console.warn('无法获取图对象');
    return;
  }

  graph.nodes?.forEach(node => {
    if (node.type?.includes('LTX')) {
      console.log('Node:', node.id, node.type);
      console.log('Widgets:', node.widgets?.map(w => ({name: w.name, value: w.value})));
    }
  });
}

// 在控制台调用
dumpLTXNodes();
```

---

### 6.3 热重载

开发时修改代码后无需刷新页面：

```javascript
// 移除旧面板
const oldRoot = document.getElementById('lora-preset-root');
if (oldRoot) oldRoot.remove();

// 重新注入
injectPanel();
```

---

## 7. 兼容性说明

### 7.1 支持的 ComfyUI 版本

| ComfyUI 版本 | 支持状态 | 备注 |
|------------|---------|------|
| 自定义分支 (LTX2.3) | ✅ 完全支持 | 测试版本 |
| 官方 ComfyUI 1.x | ⚠️ 部分支持 | 需调整节点选择器 |
| ComfyUI-LTXVideo | ❌ 不支持 | 节点类型不同 |

### 7.2 浏览器支持

| 浏览器 | 支持版本 |
|-------|---------|
| Chrome | 90+ |
| Firefox | 88+ |
| Edge | 90+ |
| Safari | 14+ (需手动开启 WebGL) |

---

## 8. 发布清单

发布新版本前检查：

- [ ] 更新版本号（`version` 字段）
- [ ] 测试所有预设能否正确应用
- [ ] 验证在不同分辨率下的显示效果
- [ ] 检查控制台有无错误
- [ ] 更新本 API 文档
- [ ] 创建 GitHub Release（如开源）

---

*文档版本: v1.0*  
*API 版本: 1.0.0*  
*最后更新: 2026-04-22*
