# Sharkfin · 按触发事件拆分明细

---

## Sharkfin · Final Fixing: Performance Coupon

| 项 | 内容 |
|----|------|
| **可编辑事实值** | Final Settlement: Principal；**Coupon** |
| **数据编号** | D-SF-FF-PC |

| 用例ID | 优先级 | 测试步骤 | 预期结果 | 实际结果 | 状态 |
|--------|--------|----------|----------|----------|------|
| TC-SF-FF-PC-FACT-001 | P0 | 编辑 **Principal** | 可编辑；保存持久化 | | |
| TC-SF-FF-PC-FACT-002 | P0 | 编辑 **Coupon** | 可编辑 | | |
| TC-SF-FF-PC-TIME-001 | P0 | 修改事件 **时间** | 保存成功 | | |
| TC-SF-FF-PC-NEG-001 | P0 | 事件未结束 | 无 ✏️ | | |

---

## Sharkfin · Final Fixing: KO Coupon

| 项 | 内容 |
|----|------|
| **可编辑事实值** | Final Settlement: Principal；**Coupon** |
| **数据编号** | D-SF-FF-KOC |

| 用例ID | 优先级 | 测试步骤 | 预期结果 | 实际结果 | 状态 |
|--------|--------|----------|----------|----------|------|
| TC-SF-FF-KOC-FACT-001 | P0 | 编辑 **Principal** | 可编辑 | | |
| TC-SF-FF-KOC-FACT-002 | P0 | 编辑 **Coupon** | 可编辑 | | |
| TC-SF-FF-KOC-TIME-001 | P0 | 修改 **事件时间** | 保存成功 | | |
| TC-SF-FF-KOC-DIFF-001 | P1 | 与 Performance Coupon 实例对比 | 两触发路径字段集合相同、入口独立 | | |
