@echo off
REM Creates assets.zip and uploads it to Cloudflare R2.
REM Requires Python 3.9+, pip install -r requirements.txt, and a local .env file.
cd /d "%~dp0"
python "upload_assets.py" %*
if errorlevel 1 pause
