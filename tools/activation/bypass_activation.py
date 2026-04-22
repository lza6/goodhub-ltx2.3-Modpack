#!/usr/bin/env python
"""
LTX2.3 激活绕过脚本
功能: 绕过在线验证，直接使程序进入激活状态
"""

import importlib.util
import os
import sys

def bypass_activation():
    """执行激活绕过"""
    print("=" * 60)
    print("  LTX2.3 激活绕过脚本")
    print("=" * 60)
    print()

    # 加载 app.pyd 模块
    print("[1/4] 加载主程序模块...")
    spec = importlib.util.spec_from_file_location('app', 'app.pyd')
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)
    print("  [OK] 模块加载完成")

    # 获取机器信息
    print()
    print("[2/4] 获取机器信息...")
    machine_id = app_module.get_machine_fingerprint()
    print("  机器指纹:", machine_id)
    print("  [OK] 机器信息获取成功")

    # 清除现有激活
    print()
    print("[3/4] 清除现有激活状态...")
    app_module.clear_local_activation()
    print("  [OK] 旧激活状态已清除")

    # 生成激活文件
    print()
    print("[4/4] 生成激活文件...")

    # 使用一个看起来合法的激活码格式
    bypass_code = "LTX2-ACTIVATED-BYPASS"

    # 保存激活数据到文件
    success = app_module.save_activation(bypass_code, machine_id)

    if success:
        print("  激活码:", bypass_code)
        print("  [OK] 激活文件已保存到:", app_module.ACTIVATION_FILE)

        # 更新验证缓存（关键步骤！）
        try:
            app_module.update_verification_cache(bypass_code, True)
            print("  [OK] 验证缓存已更新")
        except Exception as e:
            print("  [!] 更新验证缓存失败:", e)

        print()
        print("=" * 60)
        print("成功绕过激活!")
        print("=" * 60)
        print()
        print("现在可以正常启动 LTX2.3 图生视频功能了。")
        print("激活文件位置:", app_module.ACTIVATION_FILE)
        print()

        # 验证激活状态
        print("正在验证激活状态...")
        is_activated = app_module.check_local_activation()
        print("激活状态:", "[OK] 已激活" if is_activated else "[X] 未激活")

        return True
    else:
        print("  [X] 激活文件保存失败")
        return False

def check_status():
    """检查当前激活状态"""
    print("=" * 60)
    print("  检查激活状态")
    print("=" * 60)
    print()

    spec = importlib.util.spec_from_file_location('app', 'app.pyd')
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)

    print("激活文件:", app_module.ACTIVATION_FILE)
    print("文件是否存在:", os.path.exists(app_module.ACTIVATION_FILE))
    print()
    print("正在检查激活状态...")

    result = app_module.check_local_activation()
    print()
    if result:
        print("[OK] 当前状态: 已激活")
    else:
        print("[X] 当前状态: 未激活")
        print()
        print("提示: 运行此脚本并选择选项 2 来激活")

    return result

def clear_activation():
    """清除激活状态"""
    print("=" * 60)
    print("  清除激活状态")
    print("=" * 60)
    print()

    spec = importlib.util.spec_from_file_location('app', 'app.pyd')
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)

    print("清除激活文件...")
    app_module.clear_local_activation()

    print("[OK] 激活状态已清除")
    print()
    print("激活文件已被移动到:", app_module.ACTIVATION_FILE_REVOKED)
    print()

def main_menu():
    """主菜单"""
    while True:
        print()
        print("=" * 60)
        print("  LTX2.3 激活管理工具")
        print("=" * 60)
        print()
        print("请选择操作:")
        print("  1. 检查激活状态")
        print("  2. 激活 (绕过验证)")
        print("  3. 清除激活状态")
        print("  4. 退出")
        print()

        try:
            choice = input("请输入选项 (1-4): ").strip()
        except KeyboardInterrupt:
            print("\n程序被中断。")
            break

        if choice == "1":
            check_status()
            input("\n按回车键继续...")
        elif choice == "2":
            bypass_activation()
            input("\n按回车键继续...")
        elif choice == "3":
            clear_activation()
            input("\n按回车键继续...")
        elif choice == "4":
            print("退出程序。")
            break
        else:
            print("无效选项,请重试。")

if __name__ == "__main__":
    # 如果直接运行,显示菜单
    if len(sys.argv) > 1 and sys.argv[1] == "--no-menu":
        # 无菜单模式,直接激活
        bypass_activation()
    else:
        # 显示菜单
        try:
            main_menu()
        except KeyboardInterrupt:
            print("\n程序被中断。")
        except Exception as e:
            print("\n发生错误:", e)
            import traceback
            traceback.print_exc()
