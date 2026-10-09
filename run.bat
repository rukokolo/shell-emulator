@echo off
chcp 65001 >nul
cd /d "%~dp0"

if /i "%1"=="test" (
    python -m unittest discover -v
    goto :eof
)

python src\main.py %*