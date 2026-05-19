@echo off
title 业务测试平台-后端
cd /d "%~dp0backend"
if not exist "main.py" (
  echo 错误: 未找到 backend\main.py，请把本 bat 放在 d:\cursor 下再试。
  pause
  exit /b 1
)
call start.bat
