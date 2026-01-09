@echo off
chcp 65001 >nul
title Admin Bot (Smart Reload)

set PYTHON_CMD=python
py --version >nul 2>&1
if %errorlevel% == 0 set PYTHON_CMD=py

echo [SYSTEM] Слежу ТОЛЬКО за файлами .py...
echo.

:: Запускаем watchfiles, но следим только за расширением .py
:: Файлы .db теперь будут полностью игнорироваться
%PYTHON_CMD% -m watchfiles --filter python "%PYTHON_CMD% main.py" .