::[Bat To Exe Converter]
::
::fBE1pAF6MU+EWHreyHcjLQlHcAibKWy8OpET/+b34OuDsXEYWOcxR47LyoiMNekf7nn2YJgS1HtZk84CCFVafwbL
::fBE1pAF6MU+EWHreyHcjLQlHcAibKWy8OpET/+b34OuDsXEYWOcxR47LyoiMNekf7nn2YJgS23Zli84eGhJbe1ypbxtU
::fBE1pAF6MU+EWHreyHcjLQlHcAibKWy8OpET/+b34OuDsXEYWOcxR47LyoiMNekf7nn2YJgSxHtYmsIYAQoWfBO/Dg==
::fBE1pAF6MU+EWHreyHcjLQlHcAibKWy8OpET/+b34OuDsXEYWOcxR47LyoiMNekf7nn2YJgSxH9ekdhCDhpMHg==
::fBE1pAF6MU+EWHreyHcjLQlHcAibKWy8OpET/+b34OuDsXEYWOcxR47LyoiMNekf7nn2YJgSw3MUmsoYbA==
::YAwzoRdxOk+EWAnk
::fBw5plQjdG8=
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF65
::cxAkpRVqdFKZSTk=
::cBs/ulQjdF65
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQJQ
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCyDJGyX8VAjFBdNWQOEAE+1EbsQ5+n//NaCrkgTa+MvaLP6lLGWJYA=
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
setlocal

REM 1) Определяем папку установки: сначала пробуем x86, иначе обычную
if defined ProgramFiles(x86) (
  set "INSTALLDIR=%ProgramFiles(x86)%\AnomalyDetectorStarter"
) else (
  set "INSTALLDIR=%ProgramFiles%\AnomalyDetectorStarter"
)

echo Installation directory: "%INSTALLDIR%"

REM 2) Переходим в неё
cd /d "%INSTALLDIR%" 2>nul || (
  echo ERROR: Не удалось перейти в "%INSTALLDIR%"
  pause
  exit /b 1
)

REM Остановим Redis и RabbitMQ
taskkill /F /IM redis-server.exe    >nul 2>&1
taskkill /F /IM erl.exe >nul 2>&1
taskkill /F /IM rabbitmq-server.exe >nul 2>&1

echo [STOP] Stopping existing Python services…

REM остановим оба интерпретатора из папки AnomalyDetectorStarter
wmic process where "ExecutablePath LIKE '%%LOCALAPPDATA%%\\AnomalyDetectorStarter%%' AND (Name='python.exe' OR Name='pythonw.exe')" call terminate >nul 2>&1



REM — Ждём освобождения портов
timeout /t 10 /nobreak >nul

REM 3) Запускаем ваш единый скрипт
echo Launching all from "%INSTALLDIR%"...
call "%INSTALLDIR%\run_all.bat"

endlocal
exit /b 0
