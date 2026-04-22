@echo off
chcp 65001 >nul
title 清理WAN2.2临时文件

echo ========================================
echo     清理WAN2.2便携包临时文件
echo ========================================
echo.

set "ROOT_DIR=%~dp0"
set "TEMP_DIR=%ROOT_DIR%ComfyUI\temp"

echo 正在检查临时文件目录...
echo 目标目录: %TEMP_DIR%
echo.

if exist "%TEMP_DIR%" (
    echo 找到临时文件目录，正在分析...
    
    :: 检查目录是否为空
    dir "%TEMP_DIR%" /a /b >nul 2>&1
    if errorlevel 1 (
        echo 临时目录为空，无需清理。
        goto :end
    )
    
    :: 显示目录内容概览
    echo 临时目录内容概览:
    echo ----------------------------------------
    for /f "delims=" %%i in ('dir "%TEMP_DIR%" /s /-c 2^>nul ^| find "个文件"') do echo %%i
    for /f "delims=" %%i in ('dir "%TEMP_DIR%" /s /-c 2^>nul ^| find "个目录"') do echo %%i
    echo ----------------------------------------
    echo.
    
    :: 显示主要子目录
    echo 检测到的缓存目录类型:
    if exist "%TEMP_DIR%\gradio" echo   [√] Gradio缓存目录
    if exist "%TEMP_DIR%\__pycache__" echo   [√] Python缓存目录
    
    :: 检测哈希序列号目录
    set "HASH_COUNT=0"
    for /d %%d in ("%TEMP_DIR%\*") do (
        set "DIR_NAME=%%~nxd"
        call :check_hash_dir "!DIR_NAME!"
    )
    if !HASH_COUNT! gtr 0 (
        echo   [√] 发现 !HASH_COUNT! 个哈希序列号目录（如: 3e3388f67607...）
    )
    
    for %%f in ("%TEMP_DIR%\tmp*") do (
        if exist "%%f" echo   [√] 临时文件: %%~nxf
    )
    echo.
    
    :: 安全检查 - 确认是否有程序正在运行
    echo 安全检查: 请确保已关闭所有WAN2.2相关程序！
    echo ⚠️  警告: 清理前必须关闭以下程序:
    echo    - 所有Gradio界面 (端口7860-7863)
    echo    - ComfyUI (端口8300)
    echo    - 相关Python进程
    echo.
    
    set /p "CONFIRM=确认已关闭所有程序，继续彻底清理临时文件？ (Y/N): "
    if /i not "%CONFIRM%"=="Y" (
        echo 取消清理操作。
        goto :end
    )
    
    echo.
    echo 开始彻底清理临时文件...
    echo ----------------------------------------
    
    :: 方法1: 尝试删除整个temp目录（最彻底的方法）
    echo 尝试完全删除临时目录...
    rmdir /s /q "%TEMP_DIR%" >nul 2>&1
    
    if not exist "%TEMP_DIR%" (
        echo ✓ 临时目录已完全删除！
        echo ✓ 所有缓存文件和哈希目录都已清理完成
        goto :success
    )
    
    :: 方法2: 如果无法完全删除，则逐项清理
    echo × 无法完全删除目录，尝试逐项清理...
    echo.
    
    set "CLEANED_COUNT=0"
    
    :: 清理Gradio缓存
    if exist "%TEMP_DIR%\gradio" (
        echo 正在清理Gradio缓存...
        rmdir /s /q "%TEMP_DIR%\gradio" >nul 2>&1
        if not exist "%TEMP_DIR%\gradio" (
            echo   [√] Gradio缓存清理完成
            set /a CLEANED_COUNT+=1
        ) else (
            echo   [×] Gradio缓存清理失败 ^(文件可能正在使用^)
        )
    )
    
    :: 清理Python缓存
    if exist "%TEMP_DIR%\__pycache__" (
        echo 正在清理Python缓存...
        rmdir /s /q "%TEMP_DIR%\__pycache__" >nul 2>&1
        if not exist "%TEMP_DIR%\__pycache__" (
            echo   [√] Python缓存清理完成
            set /a CLEANED_COUNT+=1
        ) else (
            echo   [×] Python缓存清理失败 ^(文件可能正在使用^)
        )
    )
    
    :: 清理所有哈希序列号目录
    echo 正在清理哈希序列号目录...
    set "HASH_CLEANED=0"
    for /d %%d in ("%TEMP_DIR%\*") do (
        set "DIR_NAME=%%~nxd"
        set "FULL_PATH=%%d"
        call :clean_hash_dir "!FULL_PATH!" "!DIR_NAME!"
    )
    
    :: 清理其他临时文件
    echo 正在清理其他临时文件...
    for %%f in ("%TEMP_DIR%\*.*") do (
        if exist "%%f" (
            del /f /q "%%f" >nul 2>&1
            if not exist "%%f" (
                echo   [√] 删除文件: %%~nxf
                set /a CLEANED_COUNT+=1
            )
        )
    )
    
    :: 清理空的子目录
    for /f "delims=" %%d in ('dir "%TEMP_DIR%" /ad /b 2^>nul') do (
        rmdir "%TEMP_DIR%\%%d" >nul 2>&1
        if not exist "%TEMP_DIR%\%%d" (
            echo   [√] 删除空目录: %%d
            set /a CLEANED_COUNT+=1
        )
    )
    
    echo ----------------------------------------
    
    :: 最终检查
    dir "%TEMP_DIR%" /a /b >nul 2>&1
    if errorlevel 1 (
        echo.
        echo ✓ 临时文件清理完成！目录已完全清空。
        :: 如果目录完全为空，删除整个temp目录
        rmdir "%TEMP_DIR%" >nul 2>&1
        if not exist "%TEMP_DIR%" (
            echo ✓ 临时目录已删除，下次运行时将自动重新创建。
        )
        goto :success
    ) else (
        echo.
        echo ⚠ 清理完成，但仍有部分文件无法删除。
        echo   这通常是因为某些文件正在被程序使用。
        echo   建议：请确保所有相关程序已完全关闭后重试。
        echo.
        echo 剩余文件和目录:
        echo ----------------------------------------
        dir "%TEMP_DIR%" /s /b | findstr /v "^$"
        echo ----------------------------------------
    )
    
    goto :end
    
) else (
    echo 未找到临时文件目录，可能已经被清理或尚未创建。
    echo 目录路径: %TEMP_DIR%
    goto :end
)

:success
echo.
echo ✅ 清理任务成功完成！
echo   - 所有Gradio缓存已清理
echo   - 所有哈希序列号目录已清理
echo   - 所有Python缓存已清理
echo   - 所有临时文件已清理
goto :end

:check_hash_dir
set "dirname=%~1"
set "dirname_len=0"
for /l %%i in (0,1,100) do (
    if not "!dirname:~%%i,1!"=="" set /a dirname_len=%%i+1
)
:: 检查是否为64位16进制字符串（哈希值通常是这个长度）
if !dirname_len! geq 32 (
    echo !dirname! | findstr /r "^[0-9a-fA-F][0-9a-fA-F]*$" >nul
    if !errorlevel! equ 0 (
        set /a HASH_COUNT+=1
    )
)
goto :eof

:clean_hash_dir
set "full_path=%~1"
set "dir_name=%~2"
set "dirname_len=0"

:: 计算目录名长度
for /l %%i in (0,1,100) do (
    if not "!dir_name:~%%i,1!"=="" set /a dirname_len=%%i+1
)

:: 检查是否为哈希值格式的目录（至少32位16进制字符）
if !dirname_len! geq 32 (
    echo !dir_name! | findstr /r "^[0-9a-fA-F][0-9a-fA-F]*$" >nul
    if !errorlevel! equ 0 (
        echo   正在删除哈希目录: !dir_name!
        rmdir /s /q "!full_path!" >nul 2>&1
        if not exist "!full_path!" (
            echo   [√] 哈希目录已删除: !dir_name!
            set /a HASH_CLEANED+=1
            set /a CLEANED_COUNT+=1
        ) else (
            echo   [×] 哈希目录删除失败: !dir_name!
        )
    )
)
goto :eof

:end
echo.
echo ========================================
echo           清理任务完成
echo ========================================
echo 提示: 下次启动WAN2.2时会自动重新创建必要的临时目录
echo.
pause

:: 启用变量延迟扩展
setlocal EnableDelayedExpansion
goto :main

:main
:: 主程序内容（将上面的代码放在这里）
goto :eof