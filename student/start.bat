@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo   业务测试平台 - 启动后端 (端口 8000)
echo ========================================
echo.

where py >nul 2>&1
if %errorlevel%==0 (
  set PY=py -3
) else (
  set PY=python
)

echo [1/2] 安装依赖...
%PY% -m pip install -r requirements.txt -q
if errorlevel 1 (
  echo 若失败请手动执行: pip install -r requirements.txt
  pause
  exit /b 1
)

echo [2/2] 启动服务...
echo.
echo   订单列表: http://127.0.0.1:8000/api/order/list
echo   API 文档: http://127.0.0.1:8000/docs
echo   测试页面: http://127.0.0.1:8000/
echo.
echo 请勿关闭本窗口；关闭即停止后端。
echo ========================================
echo.

%PY% -m uvicorn main:app --host 127.0.0.1 --port 8000
if errorlevel 1 (
  echo.
  echo [失败] 若上面是红色报错，请把内容截图或复制。常见原因：未安装 Python、依赖未装好。
  echo 可手动执行: pip install -r requirements.txt
)
echo.
pause
