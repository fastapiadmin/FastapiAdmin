@echo off
setlocal EnableDelayedExpansion

set "SCRIPT_DIR=%~dp0"
set "LOG_DIR=%SCRIPT_DIR%logs"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "CYAN=[96m"
set "RESET=[0m"

if "%1"=="" goto :show_help

if "%1"=="start" goto :start_all
if "%1"=="stop" goto :stop_all
if "%1"=="restart" goto :restart_all
if "%1"=="status" goto :check_status
if "%1"=="help" goto :show_help
if "%1"=="--help" goto :show_help
if "%1"=="-h" goto :show_help

echo %RED%❌ 未知参数: %1%RESET%
goto :show_help

:: ==================== 帮助 ====================
:show_help
echo %BLUE%使用说明:%RESET%
echo   %~nx0 start     - 启动所有服务
echo   %~nx0 stop      - 停止所有服务
echo   %~nx0 restart   - 重启所有服务
echo   %~nx0 status    - 检查服务状态
echo.
echo %BLUE%服务说明:%RESET%
echo   🚀 后端服务     - FastAPI 后端 (端口: 8001)
echo   🌐 前端 Web    - Vue 前端 (端口: 5173)
echo   📱 前端 App    - UniApp 应用 (端口: 8080)
echo   📚 文档服务    - VitePress 文档 (端口: 5174)
echo.
echo %BLUE%日志位置:%RESET%
echo   %LOG_DIR%\
goto :end

:: ==================== 启动 ====================
:start_all
echo %CYAN%🚀 开始启动所有服务...%RESET%
echo.

call :start_service "backend"   "%SCRIPT_DIR%backend"             "uv run main.py run --env=dev"    "FastapiAdmin.Backend"  "%BACKEND_PID%"
call :start_service "frontend"  "%SCRIPT_DIR%frontend\web"        "pnpm dev"                         "FastapiAdmin.Web"      "%WEB_PID%"
call :start_service "app"       "%SCRIPT_DIR%frontend\app"        "pnpm dev:h5"                      "FastapiAdmin.App"      "%APP_PID%"
call :start_service "docs"      "%SCRIPT_DIR%frontend\docs"       "pnpm dev"                         "FastapiAdmin.Docs"     "%DOCS_PID%"

echo.
echo %GREEN%🎉 所有服务启动完成！%RESET%
echo.
echo %BLUE%访问地址:%RESET%
echo   🚀 后端 API: http://localhost:8001/api/v1/docs
echo   🌐 前端 Web: http://localhost:5173
echo   📱 前端 App: http://localhost:8080
echo   📚 文档服务: http://localhost:5174
echo.
goto :end

:start_service
set "NAME=%~1"
set "DIR=%~2"
set "CMD=%~3"
set "TITLE=%~4"

echo %BLUE%🔄 启动 %NAME% 服务...%RESET%
set "PID_FILE=%LOG_DIR%\%NAME%.pid"
set "LOG_FILE=%LOG_DIR%\%NAME%.log"

if exist "%PID_FILE%" (
    set /p OLD_PID=<"%PID_FILE%"
    tasklist /FI "PID eq !OLD_PID!" 2>NUL | findstr /I "!OLD_PID!" >NUL
    if !errorlevel!==0 (
        echo %YELLOW%⚠️  %NAME% 已在运行 (PID: !OLD_PID!)%RESET%
        exit /b
    )
)

cd /d "%DIR%"
start "%TITLE%" /B %CMD% > "%LOG_FILE%" 2>&1
:: 通过窗口标题获取准确 PID
for /f "tokens=2 delims= " %%a in ('tasklist /FI "WINDOWTITLE eq %TITLE%" /NH 2^>NUL') do (
    echo %%a > "%PID_FILE%"
)
echo %GREEN%✅ %NAME% 已启动 (日志: %LOG_FILE%)%RESET%
cd /d "%SCRIPT_DIR%"
exit /b

:: ==================== 停止 ====================
:stop_all
echo %CYAN%⏹️ 开始停止所有服务...%RESET%
echo.
call :stop_service "backend"
call :stop_service "frontend"
call :stop_service "app"
call :stop_service "docs"
echo %GREEN%🎉 所有服务已停止！%RESET%
echo.
goto :end

:stop_service
set "NAME=%~1"
set "PID_FILE=%LOG_DIR%\%NAME%.pid"

if exist "%PID_FILE%" (
    set /p PID=<"%PID_FILE%"
    tasklist /FI "PID eq !PID!" 2>NUL | findstr /I "!PID!" >NUL
    if !errorlevel!==0 (
        taskkill /PID !PID! /F >NUL 2>&1
        echo %GREEN%✅ 已停止 %NAME% (PID: !PID!)%RESET%
    )
    del "%PID_FILE%" 2>NUL
) else (
    echo %YELLOW%⚠️  %NAME% 未在运行%RESET%
)
exit /b

:: ==================== 重启 ====================
:restart_all
echo %CYAN%🔄 重启所有服务...%RESET%
call :stop_all
echo.
call :start_all
goto :end

:: ==================== 状态 ====================
:check_status
echo %CYAN%🔍 检查服务状态...%RESET%
echo.
call :check_service "backend"
call :check_service "frontend"
call :check_service "app"
call :check_service "docs"
goto :end

:check_service
set "NAME=%~1"
set "PID_FILE=%LOG_DIR%\%NAME%.pid"

if exist "%PID_FILE%" (
    set /p PID=<"%PID_FILE%"
    tasklist /FI "PID eq !PID!" 2>NUL | findstr /I "!PID!" >NUL
    if !errorlevel!==0 (
        echo %GREEN%✅ %NAME%: 运行中 (PID: !PID!)%RESET%
    ) else (
        echo %RED%❌ %NAME%: 已停止%RESET%
        del "%PID_FILE%" 2>NUL
    )
) else (
    echo %RED%❌ %NAME%: 未启动%RESET%
)
exit /b

:: ==================== 结束 ====================
:end
echo %GREEN%========================================%RESET%
endlocal
