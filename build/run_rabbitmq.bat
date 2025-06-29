@echo off
setlocal

REM === Пути исходной установки и рабочей папки в AppData ===
set "APP_INSTALL=%~dp0rabbitmq"
set "APP_WORK=%LOCALAPPDATA%\AnomalyDetectorStarter\rabbitmq"

REM === Если в пользовательской папке нет RabbitMQ, копируем её туда ===
if not exist "%APP_WORK%\rabbitmq-server.exe" (
  echo Копируем RabbitMQ в "%APP_WORK%"...
  xcopy "%APP_INSTALL%" "%APP_WORK%" /E /I /Y >nul
)

REM === Устанавливаем ERLANG_HOME чтобы erl.ini не правился в Program Files ===
set "ERLANG_HOME=%APP_WORK%\erl8.1"
set "RABBITMQ_ENABLED_PLUGINS_FILE=%APP_WORK%\rabbitmq_server-3.6.6\etc\enabled_plugins"

REM === Пути для логов и данных в директории пользователя ===
set "DATA_DIR=%LOCALAPPDATA%\AnomalyDetectorStarter\rabbitmq\data"
set "LOG_DIR=%LOCALAPPDATA%\AnomalyDetectorStarter\rabbitmq\logs"

if not exist "%DATA_DIR%" md "%DATA_DIR%"
if not exist "%LOG_DIR%" md "%LOG_DIR%"

if exist "%LOG_DIR%\rabbit.log" del "%LOG_DIR%\rabbit.log"
if exist "%LOG_DIR%\rabbit.err" del "%LOG_DIR%\rabbit.err"

REM === Фоновый запуск из рабочей папки без окон ===
pushd "%APP_WORK%"
start "" /B cmd /C "rabbitmq-server.exe --detached --nodetach false --logfile "%LOG_DIR%\rabbit.log" 2> "%LOG_DIR%\rabbit.err" --mnesia dir ""%DATA_DIR%"" "
popd

endlocal
