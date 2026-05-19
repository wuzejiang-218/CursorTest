#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FCN 按默认参数询价 - 自动化执行案例
使用方式：
  1. 先启动后端：cd backend && python -m uvicorn main:app --host 127.0.0.1 --port 8000
  2. 执行：python run_fcn_rfq.py
  可选：python run_fcn_rfq.py --port 8001
        python run_fcn_rfq.py --product FCN --tenor 6
"""
import json
import sys
import urllib.error
import urllib.request

# 默认参数（与前端新增询价 FCN 默认一致）
DEFAULT = {
    "product": "FCN",
    "underlying": "NVDA,AAPL,TSLA,AMZN",
    "notional": 1_000_000,
    "tenor_months": 6,
}


def run_rfq(base_url: str, product: str, underlying: str, notional: float, tenor_months: int):
    url = f"{base_url}/api/rfq"
    payload = {
        "product": product,
        "underlying": underlying,
        "notional": notional,
        "tenor_months": tenor_months,
        "currency": "USD",
        "solve_for": "strike",
        "strike_pct": "",
        "ko_type": "period_end",
        "ko_pct": "100",
        "coupon_pct": "12",
        "par_pct": "99",
        "ki_type": "na",
        "ki_pct": "",
        "obs_freq": "1",
        "settle_cycle": "10",
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "X-Source": "automation"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    port = 8000
    product = DEFAULT["product"]
    underlying = DEFAULT["underlying"]
    notional = DEFAULT["notional"]
    tenor_months = DEFAULT["tenor_months"]

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--port" and i + 1 < len(sys.argv):
            port = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--product" and i + 1 < len(sys.argv):
            product = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--underlying" and i + 1 < len(sys.argv):
            underlying = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--tenor" and i + 1 < len(sys.argv):
            tenor_months = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--notional" and i + 1 < len(sys.argv):
            notional = float(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    base_url = f"http://127.0.0.1:{port}"
    print(f"[FCN 询价] 请求: product={product} underlying={underlying} notional={notional} tenor_months={tenor_months}")
    print(f"[FCN 询价] 地址: {base_url}/api/rfq")
    print()

    try:
        out = run_rfq(base_url, product, underlying, notional, tenor_months)
    except urllib.error.URLError as e:
        print(f"失败: 无法连接后端 ({e})")
        print("请先启动: cd backend && python -m uvicorn main:app --host 127.0.0.1 --port", port)
        sys.exit(1)
    except Exception as e:
        print(f"失败: {e}")
        sys.exit(1)

    rfq_batch_id = out.get("rfq_batch_id", "")
    quotes = out.get("quotes") or []
    message = out.get("message", "")

    if not quotes:
        print("失败: 未收到任何报价 (quotes 为空)")
        print("响应:", json.dumps(out, ensure_ascii=False, indent=2))
        sys.exit(1)

    print("询价成功")
    print(f"  batch_id: {rfq_batch_id}")
    print(f"  message:  {message}")
    print(f"  报价数:   {len(quotes)}")
    print()
    print("报价明细:")
    for q in quotes:
        print(f"  - {q.get('institution', '')}  {q.get('quote_id', '')}  年化票息 {q.get('coupon_annual_pct', '')}%  {q.get('status', '')}")
    print()
    print("自动化案例通过。")


if __name__ == "__main__":
    main()
