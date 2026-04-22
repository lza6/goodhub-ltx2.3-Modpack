# ❓ 常见问题排查（FAQ）

---

## 激活相关问题

### Q: 运行 bypass_activation.py 后提示"激活码无效"

**A**: 检查 Python 版本（需 3.10+），删除 `.qwen_activation.dat` 后重试。

---

### Q: 激活后仍看到"Online verification failed"警告

**A**: 这是正常现象，只要最终显示"已激活"即可，可以忽略该警告。

---

## LoRA 相关问题

### Q: 错误 "Value not in list: lora_03: 'xxx.safetensors' not in [...]"

**A**: 工作流中的 LoRA 文件名与磁盘文件不匹配。使用 `inspect_workflow.py` 诊断，或手动设为 `None` 后重新选择。

---

### Q: 显存不足 (OOM)

**A**: 减少 LoRA 数量，降低分辨率（如 1024x576 → 512x512），或升级 GPU。

---

## Web UI 问题

### Q: 启动后页面似乎卡住

**A**: 不是卡住，这是正常现象。等待 10-30 秒后刷新浏览器，或直接访问 `http://127.0.0.1:7966`。

---

### Q: 无法访问 Web UI

**A**: 检查端口是否被占用，确认 ComfyUI 进程正在运行。

```bash
netstat -an | findstr :7966
```

---

## 预设面板问题

### Q: 面板不显示

**A**: 确保脚本正确注入，查看浏览器控制台有无错误，刷新页面重试。

---

### Q: 应用预设后没有效果

**A**: 确认工作流中存在 LTXVideo 节点，且 Lora Loader widget 名称正确（lora_02 等）。

---

更多问题请参考完整版 [`TROUBLESHOOTING.md`](../TROUBLESHOOTING.md)。

---

*最后更新: 2026-04-22*
