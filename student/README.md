# 业务测试平台 · 后端

## 安装

```bash
cd backend
pip install -r requirements.txt
```

## 启动（必须先启动，否则浏览器会显示「拒绝连接」）

**Windows：** 双击项目里的 `启动后端.bat`，或进入 `backend` 文件夹双击 `start.bat`。

**命令行：**

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

看到 `Uvicorn running on http://127.0.0.1:8000` 后再打开浏览器。

浏览器访问：

- **页面**：http://127.0.0.1:8000/
- **API 文档**：http://127.0.0.1:8000/docs

## API 一览

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/health` | 健康检查 |
| POST | `/api/rfq` | 发起询价，返回多家机构模拟报价 |
| POST | `/api/order` | 提交订单 |
| GET | `/api/order/list` | 最近订单列表 |
| GET | `/api/lifecycle/contract/{id}` | 合约快照 |
| POST | `/api/lifecycle/event` | 触发存续事件 |
| GET | `/api/lifecycle/timeline/{id}` | 事件时间线 |

数据保存在进程内存中，重启服务后清空。
