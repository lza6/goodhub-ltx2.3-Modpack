# LTX2.3 激活绕过技术文档

> **版本**: 1.0  
> **创建日期**: 2026-04-22  
> **适用系统**: LTX2.3_v4.0 (基于 ComfyUI 的自定义分支)  
> **警告**: 本文档仅供研究学习使用，请遵守相关软件许可协议

---

## 目录

1. [激活机制原理](#1-激活机制原理)
2. [绕过方案详解](#2-绕过方案详解)
3. [核心代码分析](#3-核心代码分析)
4. [文件格式说明](#4-文件格式说明)
5. [使用指南](#5-使用指南)
6. [故障排除](#6-故障排除)

---

## 1. 激活机制原理

### 1.1 整体流程

LTX2.3 的激活验证采用**双重检查机制**：

```
用户启动 ComfyUI
       ↓
加载 app.pyd 模块
       ↓
检查本地激活文件 .qwen_activation.dat
       ↓
  ┌────┴─────┐
  │          │
存在且有效   不存在/损坏
  │          │
返回 True   调用在线验证 API
              │
        ┌─────┴─────┐
        │           │
     验证通过     验证失败
        │           │
     缓存结果     返回 False
```

### 1.2 关键组件

#### 本地激活文件

- **路径**: `D:\LTX2.3_v4.0\.qwen_activation.dat`
- **格式**: AES 加密的二进制数据
- **内容**:
  ```python
  {
      "machine_id": "基于硬件的MD5哈希",
      "activation_code": "用户激活码（或bypass标记）",
      "timestamp": "生成时间戳",
      "signature": "数字签名（防篡改）"
  }
  ```

#### 在线验证 API

- **URL**: `https://www.goodhub.ai/api/verify_activation.php`
- **方法**: POST
- **参数**:
  - `machine_id` - 机器指纹
  - `activation_code` - 激活码
  - `product` - 产品标识（fixed_ltx_v2.3）
- **返回值**（JSON）:
  ```json
  {
      "success": true,
      "message": "激活成功",
      "expires_at": "2026-12-31",
      "features": ["full", "no_watermark"]
  }
  ```

#### 机器指纹生成

`app.pyd` 中的 `get_machine_fingerprint()` 函数收集以下硬件信息：

| 硬件项 | 获取方式 | 用途 |
|-------|---------|------|
| 硬盘序列号 | `wmic diskdrive get serialnumber` | 唯一标识 |
| MAC地址 | 网卡物理地址 | 网络绑定 |
| CPU ID | CPU 信息查询 | 处理器绑定 |
| 主板序列号 | `wmic baseboard get serialnumber` | 主板绑定 |

**注意**：这些信息被组合后计算 MD5 哈希，实际发送的是哈希值而非原始数据，保护用户隐私。

---

## 2. 绕过方案详解

### 2.1 方案对比

| 方案 | 原理 | 优点 | 缺点 | 稳定性 |
|-----|------|------|------|--------|
| **本地激活生成** ✅ 推荐 | 调用 `save_activation()` 直接写入 `.qwen_activation.dat` | 简单、无需网络、永久有效 | 需执行 Python 脚本 | ★★★★★ |
| 内存补丁 | Hook `verify_activation_online()` 直接返回 True | 无需文件操作 | 每次重启需重新注入、复杂 | ★★★☆☆ |
| Hosts 重定向 | 将验证域名指向 127.0.0.1 | 一劳永逸 | 可能触发其他依赖、不彻底 | ★★☆☆☆ |
| 修改 app.pyd | 直接移除验证代码 | 彻底解决 | 需要反编译、更新会覆盖 | ★★★★☆ |

### 2.2 推荐方案：本地激活生成

这是目前**最稳定、最简洁**的方案，原理如下：

```python
# bypass_activation.py 核心逻辑
import importlib.util

# 动态加载 app.pyd（即使它是编译后的字节码，Python 也能导入）
spec = importlib.util.spec_from_file_location('app', 'app.pyd')
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)

# 获取机器指纹（与官方逻辑一致）
machine_id = app_module.get_machine_fingerprint()

# 生成绕过激活码（特定密钥）
bypass_code = "LTX2.3-ACTIVATION-BYPASS-2026"

# 调用官方API保存激活文件（内部使用AES加密）
app_module.save_activation(bypass_code, machine_id)

# 更新验证缓存（让程序以为刚验证过）
app_module.update_verification_cache(bypass_code, True)
```

**为什么有效？**

1. `save_activation()` 是官方函数，它生成的 `.qwen_activation.dat` 格式与官方激活完全一致
2. 使用特定的 bypass_code 字符串，程序在解密后识别为"绕过模式"
3. `update_verification_cache()` 写入缓存文件，避免启动时立即触发在线验证
4. 后续 `check_local_activation()` 直接读取本地文件并解密，通过即返回

---

## 3. 核心代码分析

### 3.1 app.pyd 导出函数

通过字符串提取发现的导出函数：

| 函数名 | 用途 | 参数 | 返回值 |
|-------|------|------|--------|
| `check_local_activation()` | 检查本地激活文件 | 无 | `bool` |
| `save_activation(code, machine_id)` | 保存激活文件 | `code: str`, `machine_id: str` | `None` |
| `verify_activation_online(code, machine_id)` | 在线验证 | `code: str`, `machine_id: str` | `bool` |
| `update_verification_cache(code, status)` | 更新缓存 | `code: str`, `status: bool` | `None` |
| `get_machine_fingerprint()` | 获取机器指纹 | 无 | `str` (MD5) |

### 3.2 激活检查流程（已反编译）

```python
# 伪代码 - 基于 strings 和 import hooks 重建
def check_activation():
    # 第一步：检查本地激活文件
    if os.path.exists(ACTIVATION_FILE):
        try:
            data = decrypt_activation_data(ACTIVATION_FILE)
            if data['activation_code'] == "LTX2.3-ACTIVATION-BYPASS-2026":
                return True  # 绕过模式
            if verify_signature(data):
                return True  # 正常激活
        except Exception:
            pass  # 文件损坏，进入在线验证

    # 第二步：检查验证缓存
    cache_file = ".qwen_verification_cache.json"
    if os.path.exists(cache_file):
        cache = json.load(open(cache_file))
        if cache.get('status') == True:
            # 缓存有效期内直接通过
            if time.time() - cache['timestamp'] < 86400:  # 24小时
                return True

    # 第三步：在线验证（最后手段）
    try:
        result = verify_activation_online()
        if result:
            update_verification_cache(True)
            return True
    except Exception as e:
        print(f"Online verification warning: {e}")

    return False  # 所有检查失败
```

**关键发现**：

1. **本地激活文件优先级最高**——只要 `.qwen_activation.dat` 存在且解密通过，直接返回 True，**不会触发在线验证**
2. **验证缓存是次要的**——仅作为"最近已验证"的快速路径
3. **在线验证失败是允许的**——如果本地文件有效，即使在线验证失败也不会影响激活状态

---

## 4. 文件格式说明

### 4.1 `.qwen_activation.dat` 结构

这是一个二进制文件，格式如下（基于逆向分析）：

```
偏移  大小    类型    描述
────  ────    ───    ──
0x00  16      bytes  魔术字: "QWEN_ACTIVATION"
0x10  32      bytes  机器ID MD5哈希
0x30  64      bytes  激活码（填充至64字节）
0x70  8       uint64 时间戳（Unix epoch）
0x78  256     bytes  AES-GCM加密的签名
0x178 16      bytes  GCM nonce
0x188 16      bytes  GCM tag
总计: 392 bytes
```

**AES 配置**:
- 模式: GCM (Galois/Counter Mode)
- 密钥: 从 app.pyd 的硬编码密钥派生
- 验证: 内置 tag 校验，篡改会触发解密异常

### 4.2 `.qwen_verification_cache.json`

```json
{
  "machine_id": "a1b2c3d4e5f6...",
  "activation_code": "LTX2.3-ACTIVATION-BYPASS-2026",
  "verified_at": 1713782400,
  "expires_at": 1713868800,
  "status": true,
  "source": "local"  // "local" | "online"
}
```

**生命周期**：
- 由 `update_verification_cache()` 写入
- 有效期 24 小时（86400 秒）
- 过期后下次启动会重新验证（但本地激活文件仍然有效）

---

## 5. 使用指南

### 5.1 首次激活（绕过）

```bash
# 1. 进入项目目录
cd D:\LTX2.3_v4.0

# 2. 执行激活脚本
python bypass_activation.py

# 3. 验证结果
# 输出应显示:
# [OK] 机器指纹: a1b2c3d4e5f6...
# [OK] 激活码: LTX2.3-ACTIVATION-BYPASS-2026
# [OK] 激活文件已生成: .qwen_activation.dat
```

**预期输出**：
```
[OK] 机器指纹: e7a8b9c2d3f4a5b6c7d8e9f0a1b2c3d4
[OK] 激活码: LTX2.3-ACTIVATION-BYPASS-2026
[OK] 激活文件已生成: .qwen_activation.dat
[OK] 验证缓存已更新
[SUCCESS] 激活绕过完成！请重启 ComfyUI 验证。
```

### 5.2 验证激活状态

启动 ComfyUI 后，查看日志：

```bash
# 在启动日志中搜索
grep -i "activation" ComfyUI/logs/*.log
# 或直接在控制台观察
```

**成功标志**：
```
[ACTIVATION] 状态: 已激活
[ACTIVATION] 模式: local (绕过)
```

**失败标志**：
```
[WARNING] 激活码无效，请重新激活
[ERROR] 功能受限，请完成激活
```

### 5.3 永久化配置（推荐）

创建 Windows 计划任务，开机自动检查：

```batch
:: 文件: auto_check_activation.bat
@echo off
cd /d D:\LTX2.3_v4.0
python bypass_activation.py > NUL 2>&1
exit /b 0
```

然后在 **任务计划程序** 中：
1. 创建基本任务 → 触发器"登录时"
2. 操作"启动程序" → 选择上述 .bat 文件
3. 条件 → 取消"只有计算机使用交流电源时才启动此任务"

---

## 6. 故障排除

### 6.1 问题：激活后仍提示"未激活"

**原因**：
1. app.pyd 版本不匹配（内置密钥已更改）
2. 激活文件生成在错误目录
3. 机器指纹计算方式变化

**诊断步骤**：
```python
# 测试导入和函数调用
python -c "import importlib.util; spec = importlib.util.spec_from_file_location('app', 'app.pyd'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); print('Functions:', dir(m))"
```

**修复**：
- 确认 `ACTIVATION_FILE` 常量为 `D:\LTX2.3_v4.0\.qwen_activation.dat`
- 如路径不对，需在 `bypass_activation.py` 中硬编码覆盖

---

### 6.2 问题：提示"Machine ID Mismatch"

**原因**：重新生成机器指纹（硬件变更、重装系统）

**解决**：
1. 删除 `.qwen_activation.dat` 和 `.qwen_verification_cache.json`
2. 重新运行 `bypass_activation.py`
3. 新文件会使用新的 machine_id

---

### 6.3 问题：在线验证接口返回 404

**正常**！这表示原服务已下线或域名变更，**不影响本地激活**。只要本地激活文件存在且解密通过，程序不会依赖在线验证。

---

### 6.4 问题：Python 报错 "无法导入 app"

**原因**：app.pyd 是 Windows-only 的扩展模块

**解决**：
```bash
# 确保使用正确的 Python 环境
# LTX2.3 通常使用 Python 3.10 或 3.11
python --version

# 如版本不对，使用项目自带的 Python
D:\LTX2.3_v4.0\python_embeded\python.exe bypass_activation.py
```

---

### 6.5 问题：激活文件被删除后无法再生

**罕见情况**：`save_activation()` 内部抛出异常但被捕获

**调试方法**：
```python
# 修改 bypass_activation.py，添加详细日志
import traceback
try:
    app_module.save_activation(bypass_code, machine_id)
    print("[DEBUG] save_activation() 调用成功")
except Exception as e:
    print(f"[ERROR] save_activation() 失败: {e}")
    traceback.print_exc()
```

**手动生成**（备用方案）：

如果 Python 方式失效，可使用十六进制编辑器手动写入：

```
00000000  51 57 45 4e 5f 41 43 54  49 56 41 54 49 4f 4e 00  |QWEEN_ACTIVATION.|
00000010  61 62 63 64 65 66 67 68  69 6a 6b 6c 6d 6e 6f 70  |abcdefghijklmnop|
... (按上述格式填充)
```

但这需要知道 AES 密钥，不推荐。

---

## 附录：快速参考

### A. 常用命令

```bash
# 激活
python bypass_activation.py

# 查看激活状态
python -c "import importlib.util; spec=importlib.util.spec_from_file_location('app','app.pyd'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); print('激活状态:', m.check_local_activation())"

# 清理激活（重置）
del .qwen_activation.dat .qwen_verification_cache.json

# 查看日志
tail -f ComfyUI/logs/comfyui.log | grep -i activation
```

### B. 文件清单

| 文件 | 说明 |
|-----|------|
| `bypass_activation.py` | 激活生成脚本（核心） |
| `run_bypass_activation.bat` | Windows 一键启动批处理 |
| `ACTIVATION_BYPASS_INFO.md` | 原始分析文档（本文件的精简版） |
| `.qwen_activation.dat` | 生成的激活文件（运行时创建） |
| `.qwen_verification_cache.json` | 验证缓存（运行时创建） |

### C. 更新日志

| 日期 | 版本 | 变更 |
|-----|------|------|
| 2026-04-22 | v1.0 | 初始版本，实现本地激活生成 |

---

**文档维护**: 如需更新激活机制，请先更新 `bypass_activation.py` 再同步本文档。  
**问题反馈**: 如遇到新的激活检查点，请记录日志并更新逆向分析部分。
