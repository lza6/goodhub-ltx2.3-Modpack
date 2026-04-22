@echo off
setlocal EnableExtensions
chcp 936 >nul 2>&1  :: 改用GBK（ANSI）避免中文乱码
title WebUI 启动器
cd /d "%~dp0"

cls
echo.
echo  WebUI 启动器
echo =============================================
echo.

:: 设置环境变量
set "PYTHONPATH=%~dp0ComfyUI;%PYTHONPATH%"
set "HF_HOME=%~dp0ComfyUI\models\huggingface"
set "HUGGINGFACE_HUB_CACHE=%~dp0ComfyUI\models\huggingface\hub"
set "TRANSFORMERS_CACHE=%~dp0ComfyUI\models\transformers"
set "HF_DATASETS_CACHE=%~dp0ComfyUI\models\datasets"
set "DIFFUSERS_CACHE=%~dp0ComfyUI\models\diffusers"
set "GIT_PYTHON_GIT_EXECUTABLE=%~dp0git\bin\git.exe"
:: 添加FFmpeg环境变量
set "PATH=%~dp0ffmpeg\bin;%PATH%"
set "FFMPEG_BIN=%~dp0ffmpeg\bin\ffmpeg.exe"

:: 检查Python
echo [1/4] 检查Python环境...
set PYTHON_EXE=%~dp0python_embeded\python.exe
if not exist "%PYTHON_EXE%" (
    echo [错误] 未找到Python: %PYTHON_EXE%
    pause
    exit /b 1
)
echo [OK] Python环境正常

:: =========================
:: Portable temp directories
:: =========================
set "PORTABLE_TEMP_DIR=%~dp0ComfyUI\temp"
set "TEMP=%PORTABLE_TEMP_DIR%"
set "TMP=%PORTABLE_TEMP_DIR%"
set "TMPDIR=%PORTABLE_TEMP_DIR%"
set "GRADIO_TEMP_DIR=%PORTABLE_TEMP_DIR%"
set "PYTHONPYCACHEPREFIX=%PORTABLE_TEMP_DIR%\__pycache__"
if not exist "%PORTABLE_TEMP_DIR%" mkdir "%PORTABLE_TEMP_DIR%" >nul 2>nul

:: 启动ComfyUI
echo [3/4] 启动ComfyUI服务...
:: 使用更简单的端口检查方法
curl -s -o nul -w "%%{http_code}" http://127.0.0.1:9360 | findstr "200" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] ComfyUI已在运行
) else (
    echo [信息] 启动ComfyUI...
    start /B "" "%PYTHON_EXE%" "%~dp0ComfyUI\main.py" --listen 0.0.0.0 --port 9360 --enable-manager --preview-method latent2rgb --preview-size 512
    
    :wait_comfy
    timeout /t 3 >nul
    curl -s -o nul -w "%%{http_code}" http://127.0.0.1:9360 | findstr "200" >nul 2>&1
    if %errorlevel% neq 0 goto wait_comfy
    echo [OK] ComfyUI启动完成
)

:: 启动WebUI
echo [4/4] 启动WebUI...
echo.
echo =============================================
echo WebUI 启动器 正在运行
echo =============================================
echo.
echo 提示: 按 Ctrl+C 停止所有服务
echo =============================================
echo.

:: 启动WebUI并延迟打开浏览器
echo 启动WebUI服务...
start /B "" "%PYTHON_EXE%" "%~dp0run_app.py"  :: 补全app.py的绝对路径，避免路径找不到

:: 等待WebUI启动
echo 等待WebUI启动...
:wait_webui
timeout /t 2 >nul
curl -s -o nul -w "%%{http_code}" http://127.0.0.1:7966 | findstr "200" >nul 2>&1
if %errorlevel% neq 0 goto wait_webui

:: 延迟打开浏览器（只打开一次）
echo 打开浏览器...
timeout /t 2 >nul
start "" http://127.0.0.1:7966/?__theme=dark  :: 修复start命令的引号格式

:: 等待程序结束
:wait_main
timeout /t 5 >nul
curl -s -o nul -w "%%{http_code}" http://127.0.0.1:7966 | findstr "200" >nul 2>&1
if %errorlevel% equ 0 goto wait_main

echo.
echo WebUI服务已停止
pause