# FCN · 按触发事件拆分明细

> 父文档：[存续-事实值与事件时间编辑-测试用例.md](../存续-事实值与事件时间编辑-测试用例.md)

---

## FCN · Knock Out Observation: Crossed

| 项 | 内容 |
|----|------|
| **触发事件** | Knock Out Observation: **Crossed**（敲出观察已触发/已结束） |
| **可编辑事实值** | Coupon payment；Final Settlement: Principal |
| **数据编号** | D-FCN-KO-X |

| 用例ID | 优先级 | 测试步骤 | 预期结果 | 实际结果 | 状态 |
|--------|--------|----------|----------|----------|------|
| TC-FCN-KO-X-FACT-001 | P0 | 编辑 **Coupon payment** 事实值并保存 | 可编辑；持久化 | | |
| TC-FCN-KO-X-FACT-002 | P0 | 编辑 **Final Settlement: Principal** | 可编辑；持久化 | | |
| TC-FCN-KO-X-TIME-001 | P0 | 修改本事件行 **事件时间** | 保存后时间轴更新 | | |
| TC-FCN-KO-X-NEG-001 | P0 | KO 观察 **未 Crossed/未结束** | 无 ✏️ | | |

---

## FCN · Final Fixing: Cash

| 项 | 内容 |
|----|------|
| **触发事件** | Final Fixing: **Cash** |
| **可编辑事实值** | Coupon payment；Final Settlement: Principal |
| **数据编号** | D-FCN-FF-CASH |

| 用例ID | 优先级 | 测试步骤 | 预期结果 | 实际结果 | 状态 |
|--------|--------|----------|----------|----------|------|
| TC-FCN-FF-CASH-FACT-001 | P0 | 编辑 **Coupon payment** | 可编辑 | | |
| TC-FCN-FF-CASH-FACT-002 | P0 | 编辑 **Final Settlement: Principal** | 可编辑；与 Coupon 行互不影响 | | |
| TC-FCN-FF-CASH-TIME-001 | P0 | 修改票息行、本金行 **事件时间** 各一次 | 两行时间可分别修改 | | |
| TC-FCN-FF-CASH-NEG-001 | P0 | FF Cash **未结束** | 无 ✏️ | | |

---

## FCN · Final Fixing: Physical

| 项 | 内容 |
|----|------|
| **触发事件** | Final Fixing: **Physical** |
| **可编辑事实值** | Final Settlement: **Shares**；**Fractional Share Amount** |
| **数据编号** | D-FCN-FF-PHY |

| 用例ID | 优先级 | 测试步骤 | 预期结果 | 实际结果 | 状态 |
|--------|--------|----------|----------|----------|------|
| TC-FCN-FF-PHY-FACT-001 | P0 | 编辑 **Shares** | 可编辑；**不出现** Cash 路径 Principal 字段 | | |
| TC-FCN-FF-PHY-FACT-002 | P0 | 编辑 **Fractional Share Amount** | 可编辑 | | |
| TC-FCN-FF-PHY-TIME-001 | P0 | 修改本路径事件 **时间** | 保存成功 | | |
| TC-FCN-FF-PHY-NEG-001 | P1 | 同实例若存在 Cash 字段行 | Cash 字段在本触发下 **不可编辑** | | |

---

## FCN · Knock Out Observation: Not Crossed

| 项 | 内容 |
|----|------|
| **触发事件** | Knock Out Observation: **Not Crossed** |
| **可编辑事实值** | **Coupon Payment**（仅此） |
| **顺序约束** | 须为 **有 Coupon payment 的敲出观察的前一次观察** |
| **数据编号** | D-FCN-KO-NC |

| 用例ID | 优先级 | 测试步骤 | 预期结果 | 实际结果 | 状态 |
|--------|--------|----------|----------|----------|------|
| TC-FCN-KO-NC-FACT-001 | P0 | 在正确顺序下编辑 **Coupon Payment** | 可编辑并保存 | | |
| TC-FCN-KO-NC-FACT-002 | P1 | 仅编辑 Coupon；尝试 Principal | Principal **不可编辑** | | |
| TC-FCN-KO-NC-ORD-001 | P1 | 观察顺序错误（非「有 Coupon 的前一次」） | 不可编辑或业务提示 | | |
| TC-FCN-KO-NC-TIME-001 | P0 | 修改该观察行 **事件时间** | 保存成功 | | |
