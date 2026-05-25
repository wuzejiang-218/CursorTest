# BEN · 按触发事件拆分明细

---

## BEN · Final Fixing: Cash

| 项 | 内容 |
|----|------|
| **可编辑事实值** | Coupon payment；Final Settlement: Principal |
| **数据编号** | D-BEN-FF-CASH |

| 用例ID | 优先级 | 测试步骤 | 预期结果 | 实际结果 | 状态 |
|--------|--------|----------|----------|----------|------|
| TC-BEN-FF-CASH-FACT-001 | P0 | 编辑 **Coupon payment** | 可编辑 | | |
| TC-BEN-FF-CASH-FACT-002 | P0 | 编辑 **Principal** | 可编辑 | | |
| TC-BEN-FF-CASH-TIME-001 | P0 | 修改两行 **事件时间** | 分别可改 | | |

---

## BEN · Final Fixing: Physical

| 项 | 内容 |
|----|------|
| **可编辑事实值** | Shares；Fractional Share Amount |
| **数据编号** | D-BEN-FF-PHY |

| 用例ID | 优先级 | 测试步骤 | 预期结果 | 实际结果 | 状态 |
|--------|--------|----------|----------|----------|------|
| TC-BEN-FF-PHY-FACT-001 | P0 | 编辑 **Shares** | 可编辑 | | |
| TC-BEN-FF-PHY-FACT-002 | P0 | 编辑 **Fractional Share Amount** | 可编辑 | | |
| TC-BEN-FF-PHY-TIME-001 | P0 | 修改 **事件时间** | 保存成功 | | |
