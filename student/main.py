"""
业务测试平台 - 后端 API
询价(RFQ) / 下单(Order) / 存续(Lifecycle)
兼容 Python 3.8+（避免 list[X]、X | Y 等新语法在旧环境报错）
"""
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="业务测试平台 API",
    description="询价、下单、存续 — 演示用内存存储",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BANKS = ["Barclays", "UBS", "JPM", "MS", "HSBC", "GS", "BNP"]
EVENT_LABELS = {
    "OBSERVATION": "观察日",
    "COUPON": "派息",
    "KNOCK_OUT": "敲出",
    "MATURITY": "到期",
    "AMENDMENT": "条款变更",
}

# ---------- 内存库 ----------
rfq_store: List[Dict[str, Any]] = []
order_store: List[Dict[str, Any]] = []
lifecycle_store: Dict[str, List[Dict[str, Any]]] = {}


# ---------- 模型 ----------
class RFQRequest(BaseModel):
    product: str = "FCN"
    underlying: str = ""
    notional: float = Field(ge=0, default=1_000_000)
    tenor_months: int = Field(ge=1, le=360, default=12)
    currency: str = "USD"
    solve_for: str = "strike"
    strike_pct: str = ""
    ko_type: str = "period_end"
    ko_pct: str = "100"
    coupon_pct: str = "12"
    par_pct: str = "99"
    ki_type: str = "na"
    ki_pct: str = ""
    obs_freq: str = "1"
    settle_cycle: str = "10"


class QuoteItem(BaseModel):
    institution: str
    quote_id: str
    coupon_annual_pct: str
    status: str


class RFQResponse(BaseModel):
    """quotes 用 Dict 避免旧版 Python/Pydantic 解析 List[QuoteItem] 报错"""
    rfq_batch_id: str
    quotes: List[Dict[str, Any]]
    message: str


class OrderRequest(BaseModel):
    rfq_id: str = Field(min_length=1)
    side: str = "BUY"
    qty: int = Field(ge=1, default=1)
    price_type: str = "LIMIT"
    extra: Optional[str] = None


class OrderResponse(BaseModel):
    order_id: str
    status: str
    message: str


class LifecycleEventRequest(BaseModel):
    contract_id: str = Field(min_length=1)
    event_type: str
    event_date: str
    outcome: str = "success"


class ContractSnapshot(BaseModel):
    contract_id: str
    status: str
    phase: str
    coupon_paid: int
    ko_barrier_pct: str
    message: str


# ---------- 路由 ----------
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    """避免浏览器请求站点图标时出现 404 红字"""
    return Response(status_code=204)


@app.get("/api/health")
def health():
    return {"ok": True, "service": "easytrade-test-platform", "ts": datetime.now().isoformat()}


@app.post("/api/rfq", response_model=RFQResponse)
def create_rfq(request: Request, body: RFQRequest):
    day = datetime.now().strftime("%Y%m%d")
    batch = f"RFQ-{day}-{random.randint(100, 999)}"
    quotes: List[QuoteItem] = []
    for i, bank in enumerate(BANKS[:5]):
        qid = f"{batch}-{i + 1}"
        coupon = f"{8 + random.random() * 6:.2f}"
        quotes.append(
            QuoteItem(
                institution=bank,
                quote_id=qid,
                coupon_annual_pct=coupon,
                status="已回价",
            )
        )
    def _dump(m):
        return m.model_dump() if hasattr(m, "model_dump") else m.dict()

    source = (request.headers.get("X-Source") or "web").lower()
    if source not in ("web", "automation", "script"):
        source = "web"

    record = {
        "batch_id": batch,
        "created_at": time.time(),
        "source": source,
        "request": _dump(body),
        "quotes": [_dump(q) for q in quotes],
    }
    rfq_store.append(record)
    return RFQResponse(
        rfq_batch_id=batch,
        quotes=[_dump(q) for q in quotes],
        message=f"已收到 {len(quotes)} 家机构报价",
    )


@app.post("/api/order", response_model=OrderResponse)
def place_order(body: OrderRequest):
    oid = f"ORD-{int(time.time() * 1000)}"
    rec = {
        "order_id": oid,
        "created_at": time.time(),
        **(body.model_dump() if hasattr(body, "model_dump") else body.dict()),
        "status": "FILLED",
    }
    order_store.append(rec)
    return OrderResponse(order_id=oid, status="FILLED", message="成交通知已生成（演示）")


@app.get("/api/order/list")
def list_orders(limit: int = 20):
    return {"items": list(reversed(order_store[-limit:]))}


@app.get("/api/rfq/list")
def list_rfq(limit: int = 50):
    """询价执行记录（含页面提交与自动化脚本调用）"""
    items = []
    for r in reversed(rfq_store[-limit:]):
        req = r.get("request") or {}
        items.append({
            "batch_id": r.get("batch_id", ""),
            "created_at": r.get("created_at", 0),
            "created_at_iso": datetime.fromtimestamp(r.get("created_at", 0)).strftime("%Y-%m-%d %H:%M:%S"),
            "source": r.get("source", "web"),
            "product": req.get("product", ""),
            "underlying": req.get("underlying", ""),
            "notional": req.get("notional", 0),
            "tenor_months": req.get("tenor_months", 0),
            "quote_count": len(r.get("quotes") or []),
        })
    return {"items": items}


@app.get("/api/rfq/{batch_id}")
def get_rfq_detail(batch_id: str):
    """单条询价详情（含全部请求参数 + 各机构报价）"""
    for r in rfq_store:
        if r.get("batch_id") == batch_id:
            req = r.get("request") or {}
            return {
                "batch_id": r.get("batch_id", ""),
                "created_at_iso": datetime.fromtimestamp(r.get("created_at", 0)).strftime("%Y-%m-%d %H:%M:%S"),
                "source": r.get("source", "web"),
                "product": req.get("product", ""),
                "underlying": req.get("underlying", ""),
                "notional": req.get("notional", 0),
                "tenor_months": req.get("tenor_months", 0),
                "currency": req.get("currency", "USD"),
                "solve_for": req.get("solve_for", ""),
                "strike_pct": req.get("strike_pct", ""),
                "ko_type": req.get("ko_type", ""),
                "ko_pct": req.get("ko_pct", ""),
                "coupon_pct": req.get("coupon_pct", ""),
                "par_pct": req.get("par_pct", ""),
                "ki_type": req.get("ki_type", ""),
                "ki_pct": req.get("ki_pct", ""),
                "obs_freq": req.get("obs_freq", ""),
                "settle_cycle": req.get("settle_cycle", ""),
                "quotes": r.get("quotes") or [],
            }
    return {"error": "未找到该询价记录", "batch_id": batch_id}


@app.get("/api/lifecycle/contract/{contract_id}", response_model=ContractSnapshot)
def get_contract(contract_id: str):
    events = lifecycle_store.get(contract_id, [])
    return ContractSnapshot(
        contract_id=contract_id,
        status="ACTIVE",
        phase="LIVE",
        coupon_paid=min(3 + len([e for e in events if e.get("event_type") == "COUPON"]), 12),
        ko_barrier_pct="100%",
        message=f"共 {len(events)} 条存续事件记录",
    )


@app.post("/api/lifecycle/event")
def trigger_lifecycle_event(body: LifecycleEventRequest):
    cid = body.contract_id
    if cid not in lifecycle_store:
        lifecycle_store[cid] = []
    entry = {
        "time": datetime.now().isoformat(),
        "event_type": body.event_type,
        "event_label": EVENT_LABELS.get(body.event_type, body.event_type),
        "event_date": body.event_date,
        "outcome": body.outcome,
    }
    lifecycle_store[cid].append(entry)
    return {"ok": True, "entry": entry}


@app.get("/api/lifecycle/timeline/{contract_id}")
def timeline(contract_id: str):
    rows = list(reversed(lifecycle_store.get(contract_id, [])))
    return {"contract_id": contract_id, "items": rows}


@app.get("/")
def serve_index():
    html = ROOT / "test-platform.html"
    if not html.is_file():
        return {"error": "请将 test-platform.html 放在与 backend 同级的 cursor 目录下"}
    return FileResponse(html)


@app.get("/test-platform.html")
def serve_platform():
    return FileResponse(ROOT / "test-platform.html")
