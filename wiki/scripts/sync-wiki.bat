@echo off
REM Build and publish the wiki/ folder to the GitHub Wiki repository (pushes!).
REM Pass extra args through, e.g.: sync-wiki.bat -Message "Update guide"
pwsh -NoProfile -ExecutionPolicy Bypass -File "%~dp0sync-wiki.ps1" %*
echo.
pause
