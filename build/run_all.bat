@echo off
setlocal

taskkill /F /IM redis-server.exe    >nul 2>&1
taskkill /F /IM erl.exe >nul 2>&1
taskkill /F /IM rabbitmq-server.exe >nul 2>&1

wmic process where "ExecutablePath LIKE '%%LOCALAPPDATA%%\\AnomalyDetectorStarter%%' AND (Name='python.exe' OR Name='pythonw.exe')" call terminate >nul 2>&1

REM === 1) Установка Python и JRE через winget (если есть) ===
if exist "%windir%\system32\winget.exe" (
  winget install --id Python.Python.3.11 -e --silent --accept-package-agreements --accept-source-agreements
  winget install --id EclipseAdoptium.Temurin.8.JRE -e --silent --accept-package-agreements --accept-source-agreements
)

REM === 2) Запуск сервисов асинхронно ===
cd /d "%~dp0"

start "" /B cmd /C run_rabbitmq.bat
start "" /B cmd /C run_redis.bat
start "" /B cmd /C run_backend.bat
start "" /B cmd /C run_ui.bat
start "" /B cmd /C run_ml_service.bat

endlocal
