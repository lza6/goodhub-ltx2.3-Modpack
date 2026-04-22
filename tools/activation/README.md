# 激活工具

本目录包含 LTX2.3 系统的激活绕过工具。

---

## 📋 文件说明

| 文件 | 说明 | 使用场景 |
|------|------|---------|
| `bypass_activation.py` | 核心激活脚本 | 命令行执行 |
| `run_bypass_activation.bat` | Windows 一键批处理 | 双击运行 |

---

## 🔓 工作原理

LTX2.3 的激活验证采用双重检查机制：

```
启动 → 检查 .qwen_activation.dat (本地) → 存在？→ 是 → 解密 → 通过？→ 进入系统
                              ↓ 否
                          在线验证 API → 通过 → 进入系统
                                    ↓ 失败
                                  提示激活
```

**绕过原理**：
1. 动态加载 `app.pyd` 模块
2. 调用 `get_machine_fingerprint()` 获取机器指纹
3. 调用 `save_activation(bypass_code, machine_id)` 直接生成加密的激活文件
4. 调用 `update_verification_cache()` 标记为"已验证"
5. 后续启动直接读取本地文件，不会触发在线验证

---

## 🚀 使用方法

### 方法1：Python 脚本（推荐）

```bash
# 进入项目根目录
cd D:\LTX2.3_v4.0

# 执行激活脚本
python tools/activation/bypass_activation.py
```

**预期输出**：
```
[OK] 机器指纹: e7a8b9c2d3f4...
[OK] 激活码: LTX2.3-ACTIVATION-BYPASS-2026
[OK] 激活文件已生成: .qwen_activation.dat
[OK] 验证缓存已更新
[SUCCESS] 激活绕过完成！请重启 ComfyUI 验证。
```

### 方法2：Windows 批处理（最简单）

双击运行：
```
tools\activation\run_bypass_activation.bat
```

或命令行：
```batch
cd tools\activation
run_bypass_activation.bat
```

---

## ✅ 验证激活状态

启动 ComfyUI 后，查看日志：

```
[2026-04-22 14:30:15] [ACTIVATION] 状态: 已激活
[2026-04-22 14:30:15] [ACTIVATION] 模式: local (绕过)
```

**成功标准**：
- 没有"请完成激活"的弹窗
- 功能菜单全部可用
- 日志中无 `ERROR` 级别的激活相关错误

---

## ⚠️ 注意事项

1. **仅限本地使用**：此脚本生成的激活文件绑定当前机器，不可复制到其他计算机
2. **备份激活文件**：`.qwen_activation.dat` 位于项目根目录，建议备份
3. **重装系统后**：需要重新运行激活脚本（机器指纹会变）
4. **版本兼容**：不同版本的 `app.pyd` 可能内置不同的 AES 密钥，如激活失效请反馈

---

## 🔧 高级选项

### 自定义激活码

编辑 `bypass_activation.py`，修改 `BYPASS_CODE` 常量：

```python
BYPASS_CODE = "LTX2.3-ACTIVATION-BYPASS-2026"  # 改为你的自定义字符串
```

### 静默模式

```python
# 在脚本中添加
import os
os.environ['LTX_SILENT'] = '1'  # 抑制详细输出
```

---

## 🐛 故障排除

### 问题1：导入 app.pyd 失败

```
ImportError: DLL load failed
```

**原因**：Python 版本不匹配或缺少 VC++ 运行库。

**解决**：
1. 确认使用 Python 3.10 或 3.11
2. 安装 [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)
3. 使用项目内嵌的 Python：`python_embeded\python.exe tools/activation/bypass_activation.py`

---

### 问题2：激活文件生成但启动仍提示激活

**原因**：文件位置不对或权限问题。

**诊断**：
```bash
# 确认文件存在且大小正常
dir .qwen_activation.dat

# 检查文件权限（仅 Windows）
icacls .qwen_activation.dat
```

**修复**：
1. 确保 ComfyUI 有读取该文件的权限
2. 删除 `.qwen_activation.dat` 和 `.qwen_verification_cache.json`
3. 重新运行激活脚本
4. 以管理员身份启动 ComfyUI（测试用）

---

### 问题3：多次激活后文件被覆盖

这是正常的，每次运行都会重新生成激活文件（使用相同的 bypass_code）。

---

## 📊 文件清单

激活相关文件位置：

```
项目根目录/
├── .qwen_activation.dat          # 激活文件（运行时生成）
├── .qwen_verification_cache.json # 验证缓存（运行时生成）
├── app.pyd                       # 主程序（包含激活逻辑）
└── tools/activation/
    ├── bypass_activation.py      # 主脚本
    └── run_bypass_activation.bat # 批处理
```

---

## 🔍 技术细节

### 激活文件格式

`.qwen_activation.dat` 是 AES-GCM 加密的二进制文件，结构：

| 偏移 | 大小 | 内容 |
|------|------|------|
| 0x00 | 16 B | 魔术字 `"QWEN_ACTIVATION"` |
| 0x10 | 32 B | 机器 ID (MD5) |
| 0x30 | 64 B | 激活码 (填充) |
| 0x70 | 8 B | 时间戳 |
| 0x78+| 变长 | AES-GCM 加密载荷 + tag |

**密钥来源**：从 `app.pyd` 的 `.rdata` 段提取硬编码密钥。

---

## 📝 更新日志

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-04-22 | v1.0 | 初始版本，支持本地激活生成 |

---

*最后更新: 2026-04-22*
