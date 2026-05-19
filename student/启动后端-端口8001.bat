@echo off
title 业务测试平台-后端:8001
cd /d "%~dp0backend"
if not exist "main.py" (
  echo 未找到 main.py
  pause
  exit /b 1
)
echo 使用端口 8001（8000 被占用时可选用本脚本）
echo 浏览器请打开: http://127.0.0.1:8001/
echo.
py -3 -m pip install -r requirements.txt -q 2>nul
if errorlevel 1 python -m pip install -r requirements.txt -q
py -3 -m uvicorn main:app --host 127.0.0.1 --port 8001 2>nul
if errorlevel 1 python -m uvicorn main:app --host 127.0.0.1 --port 8001
pause
