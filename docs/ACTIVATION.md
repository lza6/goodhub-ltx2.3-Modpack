# 🔓 LTX2.3 激活绕过指南

> **版本**: 1.0  
> **最后更新**: 2026-04-22  
> **适用**: LTX2.3_v4.0

---

## ⚡ 快速激活（3分钟）

### 步骤1：运行激活脚本

```bash
cd D:\LTX2.3_v4.0
python tools\activation\bypass_activation.py
```

### 步骤2：查看输出

如果看到以下输出，表示成功：
```
[OK] 机器指纹: e7a8b9c2d3f4a5b6...
[OK] 激活码: LTX2.3-ACTIVATION-BYPASS-2026
[OK] 激活文件已生成: .qwen_activation.dat
[SUCCESS] 激活绕过完成！
```

### 步骤3：重启 Web UI

关闭当前运行的 ComfyUI 进程，重新启动：
```bash
python main.py
# 或双击 启动脚本.bat
```

### 步骤4：验证

在启动日志中找到：
```
[ACTIVATION] 状态: 已激活
[ACTIVATION] 模式: local (绕过)
```

看到"已激活"即完成 ✅

---

## 📖 详细说明

### 激活机制

LTX2.3 的激活验证流程：

```
启动 → 读取 .qwen_activation.dat → 解密验证 → 通过？
           ↓ 失败/不存在            ↓ 否
        在线验证 API → 通过？ → 进入系统
                   ↓ 否
           ❌ 提示激活
```

**绕过原理**：
1. 动态加载 `app.pyd`（官方模块）
2. 调用官方 API `save_activation()` 生成加密的激活文件
3. 调用 `update_verification_cache()` 标记为已验证
4. 启动时 `check_local_activation()` 读取本地文件直接通过，不再联网

---

## 🛠️ 高级用法

### Windows 计划任务（开机自动）

```batch
# 1. 创建计划任务
schtasks /create /tn "LTX_Activation" /tr "D:\LTX2.3_v4.0\tools\activation\bypass_activation.py" /sc onlogon /delay 0000:30 /ru System

# 2. 验证
schtasks /query /tn "LTX_2.3_Activation"
```

**作用**：每次登录 Windows 时自动运行激活检查，确保永久激活。

---

### 静默模式

```bash
# 设置环境变量
set LTX_SILENT=1
python tools\activation\bypass_activation.py

# 输出简化
[OK] 激活成功
```

编辑 `bypass_activation.py` 添加：
```python
import os
if os.environ.get('LTX_SILENT'):
    print = lambda *args, **kwargs: None  # 禁用输出
```

---

### 自定义激活码

```python
# 在 bypass_activation.py 中修改
BYPASS_CODE = "YOUR-CUSTOM-CODE-HERE"
```

**注意**：修改后需要删除旧的 `.qwen_activation.dat` 重新生成。

---

## 🔧 故障排除

### 现象：激活后仍有警告 "Online verification failed"

**这是正常现象**，不影响使用。

**原因**：激活检查流程是：
1. 检查本地文件 ✅ → 返回已激活
2. 接着尝试在线验证 ❌ → 记录警告日志
3. 但最终状态是 ✅ 已激活

**验证方法**：
```python
# 在 Python 中验证
python -c "import importlib.util; spec=importlib.util.spec_from_file_location('app','app.pyd'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); print('状态:', '已激活' if m.check_local_activation() else '未激活')"
```

预期输出：`状态: 已激活`

---

### 现象：启动后仍提示"请完成激活"

**原因 1**：`.qwen_activation.dat` 文件位置不对

**解决**：
```bash
# 确认文件位置
dir .qwen_activation.dat
# 应该在项目根目录 D:\LTX2.3_v4.0\ 下
```

如果不在，请手动移动到根目录，或修改 `bypass_activation.py` 中的 `ACTIVATION_FILE` 路径。

---

**原因 2**：app.pyd 版本更新，内置密钥变更

**解决**：
1. 删除 `.qwen_activation.dat` 和 `.qwen_verification_cache.json`
2. 重新运行激活脚本
3. 如果还不行，检查 `app.pyd` 文件大小是否与之前一致（可能已被更新）

---

### 现象：Python 报错 "ImportError: cannot import name 'app'"

**原因**：`app.pyd` 是编译后的扩展模块，只能通过 `importlib` 加载。

**正确做法**：
```bash
# ❌ 错误
import app  # 不要这样

# ✅ 正确
import importlib.util
spec = importlib.util.spec_from_file_location('app', 'app.pyd')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
```

---

## 📊 文件清单

| 文件 | 位置 | 说明 |
|------|------|------|
| `.qwen_activation.dat` | 项目根目录 | 激活文件（AES 加密） |
| `.qwen_verification_cache.json` | 项目根目录 | 验证缓存（JSON） |
| `bypass_activation.py` | `tools/activation/` | 激活脚本 |
| `run_bypass_activation.bat` | `tools/activation/` | 批处理一键激活 |
| `app.pyd` | 项目根目录 | 主程序（含激活逻辑） |

---

## 🔐 安全说明

- 本脚本**仅修改本地文件**，不会上传任何数据
- 机器指纹仅用于生成本地加密文件，不对外传输
- 激活码 `LTX2.3-ACTIVATION-BYPASS-2026` 为固定字符串，无实际网络验证
- 建议**仅用于本地研究和测试**，勿用于商业用途

---

## 📝 相关文档

- [系统架构](ARCHITECTURE.md) - 了解 app.pyd 的角色
- [故障排查](TROUBLESHOOTING.md) - 更多激活问题
- [开发者手册](DEVELOPMENT.md) - 如果你想修改激活逻辑

---

*文档版本: v1.0*  
*脚本版本: v1.0*  
*最后更新: 2026-04-22*
