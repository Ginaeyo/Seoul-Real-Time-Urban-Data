@echo off
"%~dp0.venv\Scripts\python.exe" "%~dp0src\main.py" %*
exit /b %errorlevel%
