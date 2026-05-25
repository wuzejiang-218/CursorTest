# 询价下单 · Quotation ID 询价摘要

v3.61 优化：订单详情 **Quotation ID** 旁增加信息图标，点击展示各 Payoff **Best Price** 询价摘要；权限遵循 AQDQVAN / AQDQ 规则。

## 文件

| 文件 | 用途 |
|------|------|
| `询价下单-QuotationID摘要-测试用例.md` | 可执行用例表 |
| `询价下单-QuotationID摘要-测试用例.xmind` | XMind 脑图 |
| `需求原型-QuotationID信息图标.png` | 需求原型 |
| `build_xmind.py` | 重新生成脑图 |

## 重新生成 XMind

> 脑图不含 `TC-*` 编号，规范见 [xmind-output-rules.md](../../xmind-output-rules.md)。

```bash
cd test-cases/v361/询价下单-QuotationID摘要
python build_xmind.py
```

## 需求一句话

> Quotation ID 旁加 ⓘ，点图标看询价最优价摘要；点 ID 文本仍跳转询价页；AQDQVAN 看 credit charge，AQDQ 看 user uf。
