@echo off
setlocal
pushd "%~dp0"

rem 选择系统 Python（优先 WindowsApps 自带/商店版），找不到再用 PATH 里的 python
set "PYCMD="
for %%P in ("%LocalAppData%\Microsoft\WindowsApps\python.exe" "%SystemRoot%\py.exe" "%SystemRoot%\System32\python.exe") do (
  if not defined PYCMD if exist "%%~fP" set "PYCMD=%%~fP"
)
if not defined PYCMD (
  for /f "delims=" %%P in ('where python 2^>nul') do (
    if not defined PYCMD set "PYCMD=%%P"
  )
)
if not defined PYCMD (
  echo 未找到可用的系統 Python，請安裝或在「應用執行別名」中啟用 python。
  pause
  exit /b 1
)

echo 使用的 Python: %PYCMD%
"%PYCMD%" -m pip install --upgrade pyautogui keyboard pillow pyperclip
if errorlevel 1 (
  echo 依賴安裝失敗，請檢查網絡或 pip 配置。
  pause
  exit /b 1
)

"%PYCMD%" "%~dp01.py"
if errorlevel 1 (
  echo 運行失敗，請確認依賴已安裝且 Python 可用。
  pause
)

popd
