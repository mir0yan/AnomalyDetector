@echo off
setlocal

REM 
set "APPDIR=%~dp0"
set "REDIS_DIR=%APPDIR%redis"
set "DATA_DIR=%LOCALAPPDATA%\AnomalyDetectorStarter\data"
set "LOG_DIR=%LOCALAPPDATA%\AnomalyDetectorStarter\logs"

REM 
if not exist "%DATA_DIR%"  mkdir "%DATA_DIR%"
if not exist "%LOG_DIR%"  mkdir "%LOG_DIR%"

REM 
if exist "%LOG_DIR%\server.log" del "%LOG_DIR%\server.log"
if exist "%LOG_DIR%\server.err" del "%LOG_DIR%\server.err"

REM 
pushd "%REDIS_DIR%"
start "" /B cmd /C "redis-server.exe redis.windows.conf --dir "%DATA_DIR%" > "%LOG_DIR%\server.log" 2>&1"
popd

endlocal
