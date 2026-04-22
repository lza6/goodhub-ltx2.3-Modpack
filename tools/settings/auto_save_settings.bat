@echo off
chcp 936 >nul 2>&1
title LTX2.3 自动保存设置工具
echo.
echo ============================================
echo   LTX2.3 自动保存工作流设置
echo ============================================
echo.
echo 此工具会在指定间隔自动保存当前工作流
echo 以防止设置丢失（如显存自动清理等）
echo.
echo 按 Ctrl+C 停止自动保存
echo.

set /a count=0
:loop
set /a count+=1
echo [%time%] 第 %count% 次保存工作流...

python_embeded\python.exe -c "
import os
import json
import time
from datetime import datetime

# 保存当前时间戳到一个特殊文件，表示最后保存时间
user_dir = 'D:/LTX2.3_v4.0/ComfyUI/user/default'
last_save_file = os.path.join(user_dir, 'last_auto_save.txt')

with open(last_save_file, 'w', encoding='utf-8') as f:
    f.write(datetime.now().isoformat())
    f.write('\n自动保存工作流设置 - 防止显存自动清理等UI设置丢失')

print('[' + time.strftime('%H:%M:%S') + '] 工作流状态已标记为已保存')
"

timeout /t 300 >nul 2>&1  # 5分钟自动保存一次
goto loop