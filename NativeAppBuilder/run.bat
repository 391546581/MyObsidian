@echo off
CHCP 65001 > nul
set SCRIPT_DIR=%~dp0
echo ========================================
echo   NativeAppBuilder Launcher
echo ========================================
echo.

:: 检查 Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] 未找到 Node.js，请先安装: https://nodejs.org/
    pause
    exit /b
)

:: 检查 Nativefier
where nativefier >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] 正在尝试安装 nativefier...
    call npm install -g nativefier
)

:: 运行 PowerShell 脚本
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%build.ps1"

pause
