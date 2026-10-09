@echo off
chcp 65001 >nul
cd /d "%~dp0.."
echo ===== Тест: только --vfs-path =====
echo exit | python src\main.py --vfs-path vfs\test.zip
pause