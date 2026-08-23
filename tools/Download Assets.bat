@echo off
REM Downloads and installs game assets from the public R2 distribution.
REM Requires Python 3.9+ and: pip install -r requirements.txt
cd /d "%~dp0"
python "download_assets.py" %*
if errorlevel 1 pause
