import sys
import os
import importlib.util

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# 明确指定要导入的 app.pyd 路径
app_pyd_path = os.path.join(current_dir, "app.pyd")

if not os.path.exists(app_pyd_path):
    print(f"错误：未找到 app.pyd，路径：{app_pyd_path}")
    sys.exit(1)

# 强制导入指定路径的 app.pyd
spec = importlib.util.spec_from_file_location("app", app_pyd_path)
app = importlib.util.module_from_spec(spec)
sys.modules["app"] = app  # 将导入的模块注册为 "app"
spec.loader.exec_module(app)

# 验证是否导入成功
print(f"成功导入的 app 模块路径：{app.__file__}")

if __name__ == "__main__":
    if hasattr(app, "main"):
        app.main()
    else:
        print("错误：app 模块中仍未找到 main() 函数")
        sys.exit(1)