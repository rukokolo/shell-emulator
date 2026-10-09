@echo off
chcp 65001 >nul
cd /d "%~dp0.."
echo ===== Тест 1: скрипт без ошибок =====
python src\main.py --script scripts\start_ok.txt
echo.
echo ===== Тест 2: скрипт с ошибкой =====
python src\main.py --script scripts\start_error.txt
echo.
echo ===== Тест 3: скрипта не существует =====
echo exit | python src\main.py --script scripts\net_takogo.txt
pause