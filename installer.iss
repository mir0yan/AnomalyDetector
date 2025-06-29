; installer.iss

[Setup]
AppName=AnomalyDetector
AppVersion=1.0
DefaultDirName={pf}\AnomalyDetectorStarter
DefaultGroupName=AnomalyDetectorStarter
DisableProgramGroupPage=yes
OutputDir=.
OutputBaseFilename=AnomalyDetectorInstaller
Compression=lzma
SolidCompression=yes

[Code]
const
  NET35_FEATURE = 'NetFx3';

function IsNetFx35Installed(): Boolean;
var
  val: Cardinal;
begin
  { Проверяем в реестре ключ Install = 1 }
  if RegQueryDWordValue(
      HKLM,
      'SOFTWARE\Microsoft\NET Framework Setup\NDP\v3.5',
      'Install',
      val) then
    Result := (val = 1)
  else
    Result := False;
end;

function InitializeSetup(): Boolean;
var
  resCode: Integer;
begin
  Result := True;
  if not IsNetFx35Installed() then
  begin
    if MsgBox(
         'Для RabbitMQ требуется .NET Framework 3.5. ' +
         'Установить его сейчас?',
         mbConfirmation, MB_YESNO) = IDYES then
    begin
      { Запускаем DISM для включения функции }
      if not Exec(
           ExpandConstant('{sys}\dism.exe'),
           '/Online /Enable-Feature /FeatureName:'+NET35_FEATURE+' /All',
           '', SW_HIDE, ewWaitUntilTerminated, resCode)
      or (resCode <> 0) then
      begin
        MsgBox('Не удалось включить .NET 3.5 (код '+IntToStr(resCode)+')', mbError, MB_OK);
        Result := False;
      end;
    end
    else
      Result := False;  { отменяем установку всего инсталлятора }
  end;
end;

[Files]
; Redis
Source: "build\redis\*";        DestDir: "{app}\redis";    Flags: recursesubdirs createallsubdirs ignoreversion
Source: "build\run_redis.bat";  DestDir: "{app}";          Flags: ignoreversion

; RabbitMQ
Source: "build\rabbitmq\*";       DestDir: "{app}\rabbitmq"; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "build\run_rabbitmq.bat";  DestDir: "{app}";         Flags: ignoreversion


; Скрипты вашего backend
Source: "build\backend\*"; DestDir: "{app}\backend"; Flags: recursesubdirs createallsubdirs ignoreversion
; Лаунчер для backend
Source: "build\run_backend.bat"; DestDir: "{app}"; Flags: ignoreversion

; Скрипты вашего ui
Source: "build\ui\*"; DestDir: "{app}\ui"; Flags: recursesubdirs createallsubdirs ignoreversion
; Лаунчер для ui
Source: "build\run_ui.bat"; DestDir: "{app}"; Flags: ignoreversion

; Скрипты вашего ml_service
Source: "build\ml_service\*"; DestDir: "{app}\ml_service"; Flags: recursesubdirs createallsubdirs ignoreversion
; Лаунчер для ml_service
Source: "build\run_ml_service.bat"; DestDir: "{app}"; Flags: ignoreversion

Source: "build\run_all.bat"; DestDir: "{app}"; Flags: ignoreversion

Source: "build\AnomalyDetector.exe";            DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autodesktop}\AnomalyDetector Launcher"; \
Filename: "{app}\AnomalyDetector.exe"; \
WorkingDir: "{app}"; \
IconFilename: "{app}\anomaly.ico"; \
    
[Run]
Filename: "{sys}\cmd.exe"; \
Parameters: "/C cd /d ""{app}"" && run_all.bat"; \
WorkingDir: "{app}"; \
Flags: nowait runhidden shellexec runasoriginaluser