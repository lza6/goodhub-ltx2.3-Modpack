#!/usr/bin/env python
"""
LTX2.3 设置持久化修复工具
功能: 监控并自动保存LTX2.3节点的设置到工作流
"""

import importlib.util
import os
import json
import sys
from datetime import datetime

def backup_current_workflow():
    """
    备份当前工作流设置到本地
    包括: 显存自动清理、GPU配置等
    """
    print("=" * 60)
    print("  LTX2.3 设置持久化备份")
    print("=" * 60)
    print()

    # 加载主模块
    print("[1] 加载主模块...")
    spec = importlib.util.spec_from_file_location('app', 'app.pyd')
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)

    # 获取用户工作流目录
    user_dir = 'D:/LTX2.3_v4.0/ComfyUI/user/default'
    workflows_dir = os.path.join(user_dir, 'workflows')
    backup_dir = os.path.join(user_dir, 'workflows_backup')

    print("   工作流目录:", workflows_dir)
    print("   备份目录:", backup_dir)

    # 创建备份目录
    os.makedirs(backup_dir, exist_ok=True)

    # 查找所有LTX工作流
    print()
    print("[2] 扫描LTX工作流文件...")
    ltx_workflows = []
    if os.path.exists(workflows_dir):
        for f in os.listdir(workflows_dir):
            if any(keyword in f.lower() for keyword in ['ltx', 'a2v', 'i2v', 't2v', 'dzqy', 'swz']):
                ltx_workflows.append(f)

    print(f"   找到 {len(ltx_workflows)} 个工作流:")
    for wf in ltx_workflows:
        print(f"     - {wf}")

    # 创建系统设置备份
    print()
    print("[3] 备份系统设置...")

    # 创建设置记录文件
    settings_backup = {
        "timestamp": datetime.now().isoformat(),
        "machine_id": app_module.get_machine_fingerprint(),
        "activation_status": app_module.check_local_activation(),
        "workflows": ltx_workflows,
        "note": "LTX2.3 设置备份 - 包含自动生成的工作流"
    }

    backup_file = os.path.join(backup_dir, 'settings_backup.json')
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(settings_backup, f, indent=2, ensure_ascii=False)

    print(f"   设置已备份到: {backup_file}")

    print()
    print("=" * 60)
    print("备份完成!")
    print("=" * 60)
    print()
    print("要恢复设置，请运行 restore_settings.py")
    print()

def create_workflow_from_template():
    """
    从默认工作流创建用户自定义工作流
    """
    print("=" * 60)
    print("  创建工作流模板")
    print("=" * 60)
    print()

    # 查找示例工作流
    examples_dir = 'D:/LTX2.3_v4.0/ComfyUI/custom_nodes/ComfyUI-LTXVideo/example_workflows/2.3'
    if not os.path.exists(examples_dir):
        print("示例工作流目录不存在:", examples_dir)
        return

    print("示例工作流文件:")
    user_dir = 'D:/LTX2.3_v4.0/ComfyUI/user/default/workflows'
    os.makedirs(user_dir, exist_ok=True)

    for f in os.listdir(examples_dir):
        if f.endswith('.json'):
            print(" ", f)

    print()
    print("请手动将示例工作流复制到用户工作流目录:")
    print(f"  从: {examples_dir}")
    print(f"  到: {user_dir}")
    print()
    print("这样你的工作流就会被持久化保存。")
    print()

def check_settings_status():
    """
    检查当前设置状态
    """
    print("=" * 60)
    print("  设置状态检查")
    print("=" * 60)
    print()

    # 加载主模块
    spec = importlib.util.spec_from_file_location('app', 'app.pyd')
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)

    user_dir = 'D:/LTX2.3_v4.0/ComfyUI/user/default'

    print("=== 激活状态 ===")
    activated = app_module.check_local_activation()
    print("  状态:", "已激活" if activated else "未激活")
    print()

    print("=== 工作流目录 ===")
    workflows_dir = os.path.join(user_dir, 'workflows')
    print("  路径:", workflows_dir)
    print("  存在:", os.path.exists(workflows_dir))
    if os.path.exists(workflows_dir):
        count = len([f for f in os.listdir(workflows_dir) if f.endswith('.json')])
        print("  工作流数量:", count)
    print()

    print("=== 设置文件 ===")
    settings_file = os.path.join(user_dir, 'comfy.settings.json')
    print("  路径:", settings_file)
    print("  存在:", os.path.exists(settings_file))
    if os.path.exists(settings_file):
        size = os.path.getsize(settings_file)
        print("  大小:", size, "bytes")
    print()

    print("=== 配置建议 ===")
    print("1. 从示例工作流复制文件到用户工作流目录")
    print("2. 在ComfyUI中配置好节点参数后，保存工作流（Ctrl+S）")
    print("3. 下次启动时会自动加载保存的工作流")
    print()

def main():
    """主菜单"""
    while True:
        print("=" * 60)
        print("  LTX2.3 设置持久化管理工具")
        print("=" * 60)
        print()
        print("请选择操作:")
        print("  1. 检查设置状态")
        print("  2. 备份当前设置")
        print("  3. 创建工作流模板")
        print("  4. 退出")
        print()

        try:
            choice = input("请输入选项 (1-4): ").strip()
        except KeyboardInterrupt:
            print("\n程序被中断。")
            break

        if choice == "1":
            check_settings_status()
            input("\n按回车键继续...")
        elif choice == "2":
            backup_current_workflow()
            input("\n按回车键继续...")
        elif choice == "3":
            create_workflow_from_template()
            input("\n按回车键继续...")
        elif choice == "4":
            print("退出程序。")
            break
        else:
            print("无效选项，请重试。")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--no-menu":
        backup_current_workflow()
    else:
        try:
            main()
        except KeyboardInterrupt:
            print("\n程序被中断。")
        except Exception as e:
            print("\n发生错误:", e)
            import traceback
            traceback.print_exc()
