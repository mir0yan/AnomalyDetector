@echo off
setlocal EnableDelayedExpansion

REM === Пути ===
set "APPDIR=%~dp0"
set "VENV=%LOCALAPPDATA%\AnomalyDetectorStarter\ml_service_venv"
set "REQ=%APPDIR%ml_service\requirements.txt"
set "ENTRY=%APPDIR%ml_service\src\start.py"
set "LOG=%LOCALAPPDATA%\AnomalyDetectorStarter\ml_service.log"

REM ============ Обнуляем и пишем шапку лога ============
>"%LOG%" echo ===== ml_service Full Debug Log =====
>>"%LOG%" echo [%DATE% %TIME%] APPDIR=!APPDIR!
>>"%LOG%" echo [%DATE% %TIME%] VENV=!VENV!
>>"%LOG%" echo [%DATE% %TIME%] REQ=!REQ!
>>"%LOG%" echo [%DATE% %TIME%] ENTRY=!ENTRY!
>>"%LOG%" echo.  

where py.exe >nul 2>&1 && set "PYCMD=py -3.11" || set "PYCMD=python"

>"%LOG%" echo ===== ml_service Startup Log =====
>>"%LOG%" echo [%DATE% %TIME%] using PYCMD=!PYCMD!


REM === 1) Проверка и установка Python 3.11 ===
>>"%LOG%" echo [%DATE% %TIME%] Проверяем версию через !PYCMD!...
for /f "tokens=2 delims= " %%V in ('!PYCMD! --version 2^>^&1') do set "PV=%%V"
>>"%LOG%" echo [%DATE% %TIME%] Найдена версия Python !PV!

if not "!PV:~0,5!"=="3.11." (
  >>"%LOG%" echo [%DATE% %TIME%] Нужна 3.11.x, а не !PV!. Устанавливаем через winget...
  winget install --id Python.Python.3.11 -e --silent --accept-package-agreements --accept-source-agreements >>"%LOG%" 2>&1
  if errorlevel 1 (
    >>"%LOG%" echo [%DATE% %TIME%] ОШИБКА: не удалось установить Python 3.11
    goto END
  )
  >>"%LOG%" echo [%DATE% %TIME%] Python 3.11 установлен.
)

where py.exe >nul 2>&1 && set "PYCMD=py -3.11" || set "PYCMD=python"
>>"%LOG%" echo [%DATE% %TIME%] После установки PYCMD=!PYCMD!
REM === 2) Создаём venv (в AppData) ===
>>"%LOG%" echo.
>>"%LOG%" echo [%DATE% %TIME%] 2) Работа с venv...
if not exist "!VENV!\Scripts\activate.bat" (
  >>"%LOG%" echo [%DATE% %TIME%] venv не найден, создаём...
  !PYCMD! -m venv "!VENV!" >>"%LOG%" 2>&1
  if errorlevel 1 (
    >>"%LOG%" echo [%DATE% %TIME%] ОШИБКА: не удалось создать venv.
    goto END
  )
  >>"%LOG%" echo [%DATE% %TIME%] venv создан.
) else (
  >>"%LOG%" echo [%DATE% %TIME%] venv уже существует.
)

REM === 3) Активируем venv и ставим зависимости ===
>>"%LOG%" echo.
>>"%LOG%" echo [%DATE% %TIME%] 3) Устанавливаем зависимости...
call "!VENV!\Scripts\activate.bat" >>"%LOG%" 2>&1
pip install --no-warn-script-location -r "!REQ!" >>"%LOG%" 2>&1
if errorlevel 1 (
  >>"%LOG%" echo [%DATE% %TIME%] ОШИБКА: pip install вернул код %ERRORLEVEL%.
  goto END
)
>>"%LOG%" echo [%DATE% %TIME%] Зависимости установлены.

:wait_rabbit
netstat -ano | findstr /R /C:":5672 .*LISTENING" >nul
if %ERRORLEVEL% NEQ 0 (
  timeout /t 1 >nul
  goto :wait_rabbit
)

set "JAVA_BIN="
for /f "delims=" %%J in ('where java.exe 2^>nul') do (
  set "JAVA_BIN=%%~dpJ"
  goto :foundJava
)
echo Ошибка: java.exe не найден в PATH. Попробуйте установить Java.>&2
goto :runPython

:foundJava
echo Найдена Java в %JAVA_BIN%
set "PATH=%JAVA_BIN%;%PATH%"

REM === 4) Запускаем приложение (в фоне) ===

pushd "%APPDIR%ml_service"
"%VENV%\Scripts\python.exe" "%ENTRY%" >> "%LOG%" 2>&1
set "EXITCODE=%ERRORLEVEL%"
popd
>>"%LOG%" echo [%DATE% %TIME%] ml_service завершился с кодом %EXITCODE%

:END
endlocal
