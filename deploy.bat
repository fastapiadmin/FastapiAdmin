@echo off
setlocal EnableDelayedExpansion

set "SCRIPT_DIR=%~dp0"
set "BACKEND_DIR=%SCRIPT_DIR%backend"
set "FRONTEND_DIR=%SCRIPT_DIR%frontend"
set "WEB_DIR=%FRONTEND_DIR%\web"
set "APP_DIR=%FRONTEND_DIR%\app"
set "DOCS_DIR=%FRONTEND_DIR%\docs"

set "LOG_DIR=%SCRIPT_DIR%logs"
mkdir "%LOG_DIR%" 2>nul

set "BACKEND_LOG=%LOG_DIR%\backend.log"
set "WEB_LOG=%LOG_DIR%\web.log"
set "APP_LOG=%LOG_DIR%\app.log"
set "DOCS_LOG=%LOG_DIR%\docs.log"

set "BACKEND_PID_FILE=%LOG_DIR%\backend.pid"
set "WEB_PID_FILE=%LOG_DIR%\web.pid"
set "APP_PID_FILE=%LOG_DIR%\app.pid"
set "DOCS_PID_FILE=%LOG_DIR%\docs.pid"

:: 颜色定义
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "CYAN=[96m"
set "RESET=[0m"

echo %GREEN%========================================%RESET%
echo %GREEN%📦 FastapiAdmin 全局启动脚本%RESET%
echo %GREEN%========================================%RESET%
echo.

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

:show_help
echo %BLUE%使用说明:%RESET%
echo %GREEN%  %~nx0 start     %RESET% - 启动所有服务
set "YELLOW=[93m"
echo %GREEN%  %~nx0 stop      %RESET% - 停止所有服务
set "YELLOW=[93m"
echo %GREEN%  %~nx0 restart   %RESET% - 重启所有服务
set "YELLOW=[93m"
echo %GREEN%  %~nx0 status    %RESET% - 检查服务状态
set "YELLOW=[93m"
echo %GREEN%  %~nx0 help      %RESET% - 显示此帮助信息
set "YELLOW=[93m"
echo.
echo %BLUE%服务说明:%RESET%
echo %GREEN%  🚀 后端服务    %RESET% - FastAPI 后端 (默认端口: 8001)
echo %GREEN%  🌐 前端 Web   %RESET% - Vue 前端 (默认端口: 5173)
echo %GREEN%  📱 前端 App   %RESET% - UniApp 应用 (默认端口: 8080)
echo %GREEN%  📚 文档服务   %RESET% - VitePress 文档 (默认端口: 5174)
echo.
echo %BLUE%日志位置:%RESET%
echo %GREEN%  %LOG_DIR%\%RESET%
goto :end

:start_all
echo %CYAN%🚀 开始启动所有服务...%RESET%
echo.

:: 启动后端
echo %BLUE%🔄 启动后端服务...%RESET%
if exist "%BACKEND_PID_FILE%" (
    set /p PID=<"%BACKEND_PID_FILE%"
    tasklist /FI "PID eq %PID%" 2>NUL | find /I "%PID%" >NUL
    if %errorlevel%==0 (
        echo %YELLOW%⚠️  后端服务已在运行 (PID: %PID%)%RESET%
    ) else (
        echo %GREEN%✅ 启动后端服务...%RESET%
        cd /d "%BACKEND_DIR%"
        start "FastapiAdmin Backend" /B uv run main.py run --env=dev > "%BACKEND_LOG%" 2>&1
        :: 获取新启动进程的 PID
        for /f "tokens=2" %%a in ('tasklist /FI "WINDOWTITLE eq FastapiAdmin Backend" /NH') do (
            echo %%a > "%BACKEND_PID_FILE%"
            echo %GREEN%✅ 后端服务已启动 (PID: %%a)%RESET%
        )
        cd /d "%SCRIPT_DIR%"
    )
) else (
    echo %GREEN%✅ 启动后端服务...%RESET%
    cd /d "%BACKEND_DIR%"
    start "FastapiAdmin Backend" /B uv run main.py run --env=dev > "%BACKEND_LOG%" 2>&1
    :: 获取新启动进程的 PID
    for /f "tokens=2" %%a in ('tasklist /FI "WINDOWTITLE eq FastapiAdmin Backend" /NH') do (
        echo %%a > "%BACKEND_PID_FILE%"
        echo %GREEN%✅ 后端服务已启动 (PID: %%a)%RESET%
    )
    cd /d "%SCRIPT_DIR%"
)
echo.

:: 启动前端 Web
echo %BLUE%🔄 启动前端 Web 服务...%RESET%
if exist "%WEB_PID_FILE%" (
    set /p PID=<"%WEB_PID_FILE%"
    tasklist /FI "PID eq %PID%" 2>NUL | find /I "%PID%" >NUL
    if %errorlevel%==0 (
        echo %YELLOW%⚠️  前端 Web 服务已在运行 (PID: %PID%)%RESET%
    ) else (
        echo %GREEN%✅ 启动前端 Web 服务...%RESET%
        cd /d "%WEB_DIR%"
        start "FastapiAdmin Web" /B pnpm dev > "%WEB_LOG%" 2>&1
        :: 获取新启动进程的 PID
        for /f "tokens=2" %%a in ('tasklist /FI "WINDOWTITLE eq FastapiAdmin Web" /NH') do (
            echo %%a > "%WEB_PID_FILE%"
            echo %GREEN%✅ 前端 Web 服务已启动 (PID: %%a)%RESET%
        )
        cd /d "%SCRIPT_DIR%"
    )
) else (
    echo %GREEN%✅ 启动前端 Web 服务...%RESET%
    cd /d "%WEB_DIR%"
    start "FastapiAdmin Web" /B pnpm dev > "%WEB_LOG%" 2>&1
    :: 获取新启动进程的 PID
    for /f "tokens=2" %%a in ('tasklist /FI "WINDOWTITLE eq FastapiAdmin Web" /NH') do (
        echo %%a > "%WEB_PID_FILE%"
        echo %GREEN%✅ 前端 Web 服务已启动 (PID: %%a)%RESET%
    )
    cd /d "%SCRIPT_DIR%"
)
echo.

:: 启动前端 App
echo %BLUE%🔄 启动前端 App 服务...%RESET%
if exist "%APP_PID_FILE%" (
    set /p PID=<"%APP_PID_FILE%"
    tasklist /FI "PID eq %PID%" 2>NUL | find /I "%PID%" >NUL
    if %errorlevel%==0 (
        echo %YELLOW%⚠️  前端 App 服务已在运行 (PID: %PID%)%RESET%
    ) else (
        echo %GREEN%✅ 启动前端 App 服务...%RESET%
        cd /d "%APP_DIR%"
        start "FastapiAdmin App" /B pnpm dev:h5 > "%APP_LOG%" 2>&1
        :: 获取新启动进程的 PID
        for /f "tokens=2" %%a in ('tasklist /FI "WINDOWTITLE eq FastapiAdmin App" /NH') do (
            echo %%a > "%APP_PID_FILE%"
            echo %GREEN%✅ 前端 App 服务已启动 (PID: %%a)%RESET%
        )
        cd /d "%SCRIPT_DIR%"
    )
) else (
    echo %GREEN%✅ 启动前端 App 服务...%RESET%
    cd /d "%APP_DIR%"
    start "FastapiAdmin App" /B pnpm dev:h5 > "%APP_LOG%" 2>&1
    :: 获取新启动进程的 PID
    for /f "tokens=2" %%a in ('tasklist /FI "WINDOWTITLE eq FastapiAdmin App" /NH') do (
        echo %%a > "%APP_PID_FILE%"
        echo %GREEN%✅ 前端 App 服务已启动 (PID: %%a)%RESET%
    )
    cd /d "%SCRIPT_DIR%"
)
echo.

:: 启动文档服务
echo %BLUE%🔄 启动文档服务...%RESET%
if exist "%DOCS_PID_FILE%" (
    set /p PID=<"%DOCS_PID_FILE%"
    tasklist /FI "PID eq %PID%" 2>NUL | find /I "%PID%" >NUL
    if %errorlevel%==0 (
        echo %YELLOW%⚠️  文档服务已在运行 (PID: %PID%)%RESET%
    ) else (
        echo %GREEN%✅ 启动文档服务...%RESET%
        cd /d "%DOCS_DIR%"
        start "FastapiAdmin Docs" /B pnpm dev > "%DOCS_LOG%" 2>&1
        :: 获取新启动进程的 PID
        for /f "tokens=2" %%a in ('tasklist /FI "WINDOWTITLE eq FastapiAdmin Docs" /NH') do (
            echo %%a > "%DOCS_PID_FILE%"
            echo %GREEN%✅ 文档服务已启动 (PID: %%a)%RESET%
        )
        cd /d "%SCRIPT_DIR%"
    )
) else (
    echo %GREEN%✅ 启动文档服务...%RESET%
    cd /d "%DOCS_DIR%"
    start "FastapiAdmin Docs" /B pnpm dev > "%DOCS_LOG%" 2>&1
    :: 获取新启动进程的 PID
    for /f "tokens=2" %%a in ('tasklist /FI "WINDOWTITLE eq FastapiAdmin Docs" /NH') do (
        echo %%a > "%DOCS_PID_FILE%"
        echo %GREEN%✅ 文档服务已启动 (PID: %%a)%RESET%
    )
    cd /d "%SCRIPT_DIR%"
)
echo.
echo %GREEN%🎉 所有服务启动完成！%RESET%
echo.
echo %BLUE%访问地址:%RESET%
echo %GREEN%  🚀 后端 API: http://localhost:8001/api/v1/docs%RESET%
echo %GREEN%  🌐 前端 Web: http://localhost:5173%RESET%
echo %GREEN%  📱 前端 App: http://localhost:8080%RESET%
echo %GREEN%  📚 文档服务: http://localhost:5174%RESET%
echo.
goto :end

:stop_all
echo %CYAN%⏹️ 开始停止所有服务...%RESET%
echo.

:: 停止后端
if exist "%BACKEND_PID_FILE%" (
    set /p PID=<"%BACKEND_PID_FILE%"
    tasklist /FI "PID eq %PID%" 2>NUL | find /I "%PID%" >NUL
    if %errorlevel%==0 (
        echo %GREEN%✅ 停止后端服务 (PID: %PID%)%RESET%
        taskkill /PID %PID% /F >NUL 2>&1
        del "%BACKEND_PID_FILE%" >NUL 2>&1
    ) else (
        echo %YELLOW%⚠️  后端服务未在运行%RESET%
        del "%BACKEND_PID_FILE%" >NUL 2>&1
    )
) else (
    echo %YELLOW%⚠️  后端服务未在运行%RESET%
)
echo.

:: 停止前端 Web
if exist "%WEB_PID_FILE%" (
    set /p PID=<"%WEB_PID_FILE%"
    tasklist /FI "PID eq %PID%" 2>NUL | find /I "%PID%" >NUL
    if %errorlevel%==0 (
        echo %GREEN%✅ 停止前端 Web 服务 (PID: %PID%)%RESET%
        taskkill /PID %PID% /F >NUL 2>&1
        del "%WEB_PID_FILE%" >NUL 2>&1
    ) else (
        echo %YELLOW%⚠️  前端 Web 服务未在运行%RESET%
        del "%WEB_PID_FILE%" >NUL 2>&1
    )
) else (
    echo %YELLOW%⚠️  前端 Web 服务未在运行%RESET%
)
echo.

:: 停止前端 App
if exist "%APP_PID_FILE%" (
    set /p PID=<"%APP_PID_FILE%"
    tasklist /FI "PID eq %PID%" 2>NUL | find /I "%PID%" >NUL
    if %errorlevel%==0 (
        echo %GREEN%✅ 停止前端 App 服务 (PID: %PID%)%RESET%
        taskkill /PID %PID% /F >NUL 2>&1
        del "%APP_PID_FILE%" >NUL 2>&1
    ) else (
        echo %YELLOW%⚠️  前端 App 服务未在运行%RESET%
        del "%APP_PID_FILE%" >NUL 2>&1
    )
) else (
    echo %YELLOW%⚠️  前端 App 服务未在运行%RESET%
)
echo.

:: 停止文档服务
if exist "%DOCS_PID_FILE%" (
    set /p PID=<"%DOCS_PID_FILE%"
    tasklist /FI "PID eq %PID%" 2>NUL | find /I "%PID%" >NUL
    if %errorlevel%==0 (
        echo %GREEN%✅ 停止文档服务 (PID: %PID%)%RESET%
        taskkill /PID %PID% /F >NUL 2>&1
        del "%DOCS_PID_FILE%" >NUL 2>&1
    ) else (
        echo %YELLOW%⚠️  文档服务未在运行%RESET%
        del "%DOCS_PID_FILE%" >NUL 2>&1
    )
) else (
    echo %YELLOW%⚠️  文档服务未在运行%RESET%
)
echo.
echo %GREEN%🎉 所有服务已停止！%RESET%
echo.
goto :end

:restart_all
echo %CYAN%🔄 开始重启所有服务...%RESET%
echo.
goto :stop_all
:restart_all_continue
echo.
goto :start_all

:check_status
echo %CYAN%🔍 检查服务状态...%RESET%
echo.

:: 检查后端
if exist "%BACKEND_PID_FILE%" (
    set /p PID=<"%BACKEND_PID_FILE%"
    tasklist /FI "PID eq %PID%" 2>NUL | find /I "%PID%" >NUL
    if %errorlevel%==0 (
        echo %GREEN%✅ 后端服务: 运行中 (PID: %PID%)%RESET%
    ) else (
        echo %RED%❌ 后端服务: 已停止%RESET%
        del "%BACKEND_PID_FILE%" >NUL 2>&1
    )
) else (
    echo %RED%❌ 后端服务: 未启动%RESET%
)

:: 检查前端 Web
if exist "%WEB_PID_FILE%" (
    set /p PID=<"%WEB_PID_FILE%"
    tasklist /FI "PID eq %PID%" 2>NUL | find /I "%PID%" >NUL
    if %errorlevel%==0 (
        echo %GREEN%✅ 前端 Web: 运行中 (PID: %PID%)%RESET%
    ) else (
        echo %RED%❌ 前端 Web: 已停止%RESET%
        del "%WEB_PID_FILE%" >NUL 2>&1
    )
) else (
    echo %RED%❌ 前端 Web: 未启动%RESET%
)

:: 检查前端 App
if exist "%APP_PID_FILE%" (
    set /p PID=<"%APP_PID_FILE%"
    tasklist /FI "PID eq %PID%" 2>NUL | find /I "%PID%" >NUL
    if %errorlevel%==0 (
        echo %GREEN%✅ 前端 App: 运行中 (PID: %PID%)%RESET%
    ) else (
        echo %RED%❌ 前端 App: 已停止%RESET%
        del "%APP_PID_FILE%" >NUL 2>&1
    )
) else (
    echo %RED%❌ 前端 App: 未启动%RESET%
)

:: 检查文档服务
if exist "%DOCS_PID_FILE%" (
    set /p PID=<"%DOCS_PID_FILE%"
    tasklist /FI "PID eq %PID%" 2>NUL | find /I "%PID%" >NUL
    if %errorlevel%==0 (
        echo %GREEN%✅ 文档服务: 运行中 (PID: %PID%)%RESET%
    ) else (
        echo %RED%❌ 文档服务: 已停止%RESET%
        del "%DOCS_PID_FILE%" >NUL 2>&1
    )
) else (
    echo %RED%❌ 文档服务: 未启动%RESET%
)
echo.
goto :end

:end
echo %GREEN%========================================%RESET%
echo %GREEN%📦 FastapiAdmin 启动脚本%RESET%
echo %GREEN%========================================%RESET%
endlocal