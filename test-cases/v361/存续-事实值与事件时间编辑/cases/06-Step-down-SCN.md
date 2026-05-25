# Step-down SCN · 按触发事件拆分明细

> **注意：** 矩阵中 **两行**「Final Fixing: Cash」可编辑字段不同，须 **分场景** 各测一套。

---

## Step-down SCN · Knock Out Observation: Crossed

| 项 | 内容 |
|----|------|
| **可编辑事实值** | Coupon payment；Final Settlement: Principal |
| **数据编号** | D-SCN-KO-X |

| 用例ID | 优先级 | 测试步骤 | 预期结果 | 实际结果 | 状态 |
|--------|--------|----------|----------|----------|------|
| TC-SCN-KO-X-FACT-001 | P0 | 编辑 Coupon payment | 可编辑 | | |
| TC-SCN-KO-X-FACT-002 | P0 | 编辑 Principal | 可编辑 | | |
| TC-SCN-KO-X-TIME-001 | P0 | 修改事件时间 | 保存成功 | | |

---

## Step-down SCN · Final Fixing: Cash（场景 A · 含 Coupon）

| 项 | 内容 |
|----|------|
| **可编辑事实值** | Coupon payment；Final Settlement: Principal |
| **数据编号** | D-SCN-FF-CASH-A |
| **说明** | 矩阵 **第一行** FF Cash |

| 用例ID | 优先级 | 测试步骤 | 预期结果 | 实际结果 | 状态 |
|--------|--------|----------|----------|----------|------|
| TC-SCN-FF-CASH-A-FACT-001 | P0 | 编辑 **Coupon payment** | 可编辑 | | |
| TC-SCN-FF-CASH-A-FACT-002 | P0 | 编辑 **Principal** | 可编辑 | | |
| TC-SCN-FF-CASH-A-TIME-001 | P0 | 修改事件时间 | 保存成功 | | |

---

## Step-down SCN · Final Fixing: Cash（场景 B · 仅 Principal）

| 项 | 内容 |
|----|------|
| **可编辑事实值** | Final Settlement: **Principal**（仅） |
| **数据编号** | D-SCN-FF-CASH-B |
| **说明** | 矩阵 **第二行** FF Cash；与场景 A 区分实例或阶段 |

| 用例ID | 优先级 | 测试步骤 | 预期结果 | 实际结果 | 状态 |
|--------|--------|----------|----------|----------|------|
| TC-SCN-FF-CASH-B-FACT-001 | P0 | 编辑 **Principal** | 可编辑 | | |
| TC-SCN-FF-CASH-B-NEG-001 | P1 | 尝试编辑 Coupon payment | **不可编辑**（本场景无 Coupon 字段） | | |
| TC-SCN-FF-CASH-B-TIME-001 | P0 | 修改事件时间 | 保存成功 | | |
| TC-SCN-FF-CASH-B-DIFF-001 | P1 | 与场景 A 同产品对比 | 两场景可编辑字段集合符合矩阵两行差异 | | |

---

## Step-down SCN · Final Fixing: Physical

| 项 | 内容 |
|----|------|
| **可编辑事实值** | Shares；Fractional Share Amount |
| **数据编号** | D-SCN-FF-PHY |

| 用例ID | 优先级 | 测试步骤 | 预期结果 | 实际结果 | 状态 |
|--------|--------|----------|----------|----------|------|
| TC-SCN-FF-PHY-FACT-001 | P0 | 编辑 Shares | 可编辑 | | |
| TC-SCN-FF-PHY-FACT-002 | P0 | 编辑 Fractional Share Amount | 可编辑 | | |
| TC-SCN-FF-PHY-TIME-001 | P0 | 修改事件时间 | 保存成功 | | |
