@echo off
call .venv/Scripts/activate
start /B "" cmd /c "pythonw app.py > nul 2>&1"