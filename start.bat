@echo off
title Admin Bot (auto-reload)

:: 1. Проверяем, какая команда работает: python или py
set PYTHON_CMD=python
py --version >nul 2>&1
if %errorlevel% == 0 set PYTHON_CMD=py

echo [SYSTEM] Using command: %PYTHON_CMD%
echo [SYSTEM] Starting watchfiles...
echo.

:: 2. Запуск
:: Мы убрали папку "app", так как твой main.py лежит в корне
%PYTHON_CMD% -m watchfiles "%PYTHON_CMD% main.py" . --ignore-paths database

:: 3. Если что-то пошло не так, консоль не закроется
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Что-то пошло не так. Проверь, установлена ли библиотека:
    echo pip install watchfiles
    pause
)