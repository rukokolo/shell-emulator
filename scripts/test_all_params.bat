@echo off
chcp 65001 >nul
cd /d "%~dp0.."
echo ===== Тест 1: без параметров =====
echo exit | python src\main.py
echo.
echo ===== Тест 2: оба параметра =====
python src\main.py --vfs-path vfs\test.zip --script scripts\start_ok.txt
pause