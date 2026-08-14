@echo off
REM Launches the standalone Paperdoll Viewer.
REM Requires Python 3.9+ with Pillow (pip install pillow).
cd /d "%~dp0"
python "paperdoll_viewer.py" %*
if errorlevel 1 pause
