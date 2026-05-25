# Step-down FCN · 按触发事件拆分明细

> **规则：** 与 [01-FCN.md](./01-FCN.md) **完全一致**（矩阵标注「同 FCN」）。  
> 本文件用 **TC-SDFCN-*** 编号便于台账区分产品；步骤与预期 **照抄 FCN 对应节**，仅替换测试数据为 Step-down FCN 实例。

| 触发事件 | 可编辑事实值 | 复用 FCN 章节 | 本目录用例编号前缀 |
|----------|--------------|---------------|-------------------|
| KO: Crossed | Coupon payment；Principal | [FCN·KO-X](./01-FCN.md#fcn--knock-out-observation-crossed) | TC-SDFCN-KO-X-* |
| Final Fixing: Cash | Coupon payment；Principal | [FCN·FF Cash](./01-FCN.md#fcn--final-fixing-cash) | TC-SDFCN-FF-CASH-* |
| Final Fixing: Physical | Shares；Fractional | [FCN·FF Physical](./01-FCN.md#fcn--final-fixing-physical) | TC-SDFCN-FF-PHY-* |
| KO: Not Crossed | Coupon Payment | [FCN·KO-NC](./01-FCN.md#fcn--knock-out-observation-not-crossed) | TC-SDFCN-KO-NC-* |

## 抽样执行（不必重复全量时可只跑下表）

| 用例ID | 优先级 | 测试步骤 | 预期结果 | 实际结果 | 状态 |
|--------|--------|----------|----------|----------|------|
| TC-SDFCN-KO-X-SMOKE | P0 | Step-down FCN 实例 + KO Crossed 已结束；编辑 Coupon、Principal | 同 TC-FCN-KO-X-* | | |
| TC-SDFCN-FF-PHY-SMOKE | P1 | FF Physical 路径编辑 Shares | 同 TC-FCN-FF-PHY-* | | |
| TC-SDFCN-KO-NC-SMOKE | P1 | 正确观察顺序下编辑 Coupon Payment | 同 TC-FCN-KO-NC-* | | |
