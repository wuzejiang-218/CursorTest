# ELN · 按触发事件拆分明细

---

## ELN · Final Fixing: Cash

| 项 | 内容 |
|----|------|
| **可编辑事实值** | Final Settlement: **Principal**（仅） |
| **数据编号** | D-ELN-FF-CASH |

| 用例ID | 优先级 | 测试步骤 | 预期结果 | 实际结果 | 状态 |
|--------|--------|----------|----------|----------|------|
| TC-ELN-FF-CASH-FACT-001 | P0 | 编辑 **Principal** | 可编辑；**无** Coupon payment 行可编辑 | | |
| TC-ELN-FF-CASH-TIME-001 | P0 | 修改 **事件时间** | 保存成功 | | |
| TC-ELN-FF-CASH-NEG-001 | P0 | FF Cash 未结束 | 无 ✏️ | | |

---

## ELN · Final Fixing: Physical

| 项 | 内容 |
|----|------|
| **可编辑事实值** | Final Settlement: Shares；Fractional Share Amount |
| **数据编号** | D-ELN-FF-PHY |

| 用例ID | 优先级 | 测试步骤 | 预期结果 | 实际结果 | 状态 |
|--------|--------|----------|----------|----------|------|
| TC-ELN-FF-PHY-FACT-001 | P0 | 编辑 **Shares** | 可编辑 | | |
| TC-ELN-FF-PHY-FACT-002 | P0 | 编辑 **Fractional Share Amount** | 可编辑 | | |
| TC-ELN-FF-PHY-TIME-001 | P0 | 修改 **事件时间** | 保存成功 | | |
| TC-ELN-FF-PHY-NEG-001 | P1 | Cash 路径 Principal | Physical 触发下 **不可编辑** Principal | | |
