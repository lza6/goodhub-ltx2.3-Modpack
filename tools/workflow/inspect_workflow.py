#!/usr/bin/env python
"""
检查LTX2.3工作流文件，确认是否包含UI设置
"""

import os
import json

workflows_dir = 'ComfyUI/user/default/workflows'

print("=" * 60)
print("  工作流文件分析")
print("=" * 60)
print()

files = [f for f in os.listdir(workflows_dir) if f.endswith('.json')]

# 检查第一个工作流的内容
if files:
    sample_file = os.path.join(workflows_dir, files[0])
    print(f"分析文件: {files[0]}")
    print()

    with open(sample_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"工作流节点数: {len(data.get('nodes', []))}")
    print(f"工作流大小: {os.path.getsize(sample_file)} bytes")
    print()

    # 检查节点类型
    node_types = {}
    for node in data.get('nodes', []):
        typ = node.get('type', 'Unknown')
        node_types[typ] = node_types.get(typ, 0) + 1

    print("节点类型统计:")
    for typ, count in sorted(node_types.items(), key=lambda x: -x[1])[:15]:
        print(f"  {typ}: {count}")

    print()
    print("提示: LTX2.3的UI设置应该保存在: LTXV*)")
    print("检查节点 'LTXVBaseSampler', 'LTXVExtendSampler', 'LTXVImgToVideoInplace' 等")
    print()
    print("如果要持久化设置，请确保:")
    print("1. 在ComfyUI中打开工作流")
    print("2. 配置好所有参数（显存自动清理等）")
    print("3. 使用 Ctrl+S 保存工作流")
    print("4. 下次启动时加载该工作流")
    print()

print(f"总计 {len(files)} 个工作流文件")
print()
print("需要我帮你批量修复工作流设置吗？")
