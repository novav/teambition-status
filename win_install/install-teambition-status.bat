@echo off
chcp 65001 >nul
title Teambition Status Skill 安装程序
echo.
echo ============================================
echo    Teambition Status Skill 安装程序
echo ============================================
echo.

:: 获取当前脚本所在目录
set "SCRIPT_DIR=%~dp0"
set "SKILL_FILE=%SCRIPT_DIR%teambition-status.skill"
set "OPENCLAW_SKILLS_DIR=%USERPROFILE%\.openclaw\workspace\skills"
set "TARGET_DIR=%OPENCLAW_SKILLS_DIR%\teambition-status"

echo [INFO] 检查安装文件...

:: 检查 .skill 文件是否存在
if not exist "%SKILL_FILE%" (
    echo [ERROR] 未找到 teambition-status.skill 文件！
    echo [ERROR] 请确保 .skill 文件与本脚本在同一目录下。
    echo.
    pause
    exit /b 1
)

echo [OK] 找到安装文件: teambition-status.skill
echo.

:: 检查 OpenClaw 目录是否存在
if not exist "%OPENCLAW_SKILLS_DIR%" (
    echo [INFO] 创建 OpenClaw skills 目录...
    mkdir "%OPENCLAW_SKILLS_DIR%" 2>nul
    if errorlevel 1 (
        echo [ERROR] 无法创建目录: %OPENCLAW_SKILLS_DIR%
        echo [ERROR] 请确保 OpenClaw 已安装。
        echo.
        pause
        exit /b 1
    )
)

:: 检查目标目录是否已存在
if exist "%TARGET_DIR%" (
    echo [WARNING] 检测到已存在的安装！
    echo [INFO] 目标目录: %TARGET_DIR%
    echo.
    choice /C YN /M "是否覆盖现有安装"
    if errorlevel 2 (
        echo [INFO] 安装已取消。
        echo.
        pause
        exit /b 0
    )
    echo [INFO] 删除旧版本...
    rmdir /S /Q "%TARGET_DIR%" 2>nul
)

echo.
echo [INFO] 开始安装...
echo [INFO] 解压到: %TARGET_DIR%
echo.

:: 创建临时解压目录
set "TEMP_DIR=%TEMP%\teambition-status-temp"
if exist "%TEMP_DIR%" rmdir /S /Q "%TEMP_DIR%"
mkdir "%TEMP_DIR%"

:: 使用 PowerShell 解压（Windows 10+ 自带）
echo [INFO] 正在解压文件...
powershell -Command "Expand-Archive -Path '%SKILL_FILE%' -DestinationPath '%TEMP_DIR%' -Force" 2>nul

if errorlevel 1 (
    echo [ERROR] 解压失败！请确保使用的是 Windows 10 或更高版本。
    echo.
    pause
    exit /b 1
)

:: 移动文件到目标目录
echo [INFO] 复制文件到目标位置...
mkdir "%TARGET_DIR%" 2>nul
xcopy /E /Y /Q "%TEMP_DIR%\*" "%TARGET_DIR%\" >nul

:: 清理临时文件
rmdir /S /Q "%TEMP_DIR%" 2>nul

:: 验证安装
if not exist "%TARGET_DIR%\SKILL.md" (
    echo [ERROR] 安装验证失败！SKILL.md 文件未找到。
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo    安装成功！
echo ============================================
echo.
echo 安装路径: %TARGET_DIR%
echo.
echo 已安装的文件:
echo   - SKILL.md
echo   - scripts\analyze_teambition.py
echo   - references\teambition-best-practices.md
echo   - assets\example-config.json
echo.
echo ============================================
echo    使用方法
echo ============================================
echo.
echo 现在您可以直接对 OpenClaw 说以下指令：
echo.
echo   1. 查看TB任务
echo   2. Teambition 状态
echo   3. 看看项目进度
echo   4. 检查团队工作负载
echo   5. 我的待办
echo.
echo ============================================
echo    注意事项
echo ============================================
echo.
echo 使用前请确保：
echo   1. OpenClaw 正在运行
echo   2. Chrome 浏览器已安装 OpenClaw 扩展
echo   3. 已登录 Teambition 网页版
echo   4. 已进入具体项目页面
echo.
echo ============================================
echo.
echo 按任意键退出...
pause >nul
exit /b 0
