# ⚙️ 设置持久化设计

当前版本中，用户设置不会在重启后保持。本文档描述未来的设计方案。

---

## 问题定义

用户每次启动 ComfyUI 后，LTXVideo 节点的参数（分辨率、FPS、LoRA 选择等）都会**重置为默认值**，需要重新配置。

---

## 设计方案（规划中）

### 核心思路

1. 引入全局配置文件 `~/.ltx_config/settings.json`
2. 在 Gradio UI 中添加设置面板
3. 工作流加载时自动注入全局默认值（仅当节点值为空时）
4. 保存工作流时持久化实际使用的配置

---

## 实施阶段（TODO）

- [ ] Phase 2-P1: 创建配置管理器 Python 模块
- [ ] Phase 2-P1: 开发 Gradio 设置面板 UI
- [ ] Phase 2-P1: 实现工作流注入钩子
- [ ] Phase 2-P2: 自定义节点打包发布

---

详细技术设计请参见原始文档 [`SETTINGS_PERSISTENCE.md`](../SETTINGS_PERSISTENCE.md)（完整版）。

---

*状态: 设计中*  
*预计完成: Phase 2 (P1)*
