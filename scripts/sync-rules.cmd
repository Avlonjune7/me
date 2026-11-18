@echo off
setlocal
set "rules_python=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%rules_python%" (
  "%rules_python%" -B "%~dp0sync_rules.py"
) else (
  python -B "%~dp0sync_rules.py"
)
exit /b %errorlevel%
