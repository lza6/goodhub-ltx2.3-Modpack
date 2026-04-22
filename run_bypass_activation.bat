@echo off
chcp 936 >nul 2>&1
title LTX2.3 激活工具
echo.
echo ============================================
echo   LTX2.3 激活工具
echo ============================================
echo.
echo 正在执行激活绕过...
echo.

python_embeded\python.exe bypass_activation.py --no-menu

echo.
echo ============================================
echo   执行完成
echo ============================================
echo.
echo 按任意键退出...
pause >nul