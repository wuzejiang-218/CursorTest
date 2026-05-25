# 询价下单 · Quotation ID 询价摘要优化 — 测试用例（可执行）

| 项目 | 内容 |
|------|------|
| **需求摘要** | 订单详情 **Quotation ID** 旁增加 **信息图标（ⓘ）**；点击图标展示该订单询价 **各 Payoff 最优价（Best Price）** 相关字段摘要；**不替代** 原 Quotation ID 跳转询价页能力 |
| **产品** | EasyConnect · Blotter · **FCN - Trade Order Details**（询价下单类订单） |
| **参考原型** | [需求原型-QuotationID信息图标.png](./需求原型-QuotationID信息图标.png) |
| **版本** | v3.61 |
| **编写日期** | 2026-05-19 |

---

## 1. 需求要点（测试依据）

| 项 | 说明 |
|----|------|
| **现状** | 点击 Quotation ID → 直接跳转询价页 |
| **优化** | Quotation ID 右侧增加 ⓘ；点击 ⓘ → 浮层/弹窗展示询价摘要（各 Payoff **Best Price** 对应字段） |
| **权限** | 展示字段遵循既有询价权限：**AQDQVAN** 受 `credit charge` 控制；**AQDQ** 受 `user uf` 限制 |
| **回归** | 点击 **Quotation ID 文本**（非图标）仍跳转询价页 |

---

## 2. 测试范围

| 在范围 | 不在范围 |
|--------|----------|
| FCN 询价下单 · Trade Order Details · General Info 区 | 非询价下单（无 Quotation ID）订单 |
| ⓘ 图标展示、点击、摘要内容 | 询价页内编辑/重新报价流程 |
| Quotation ID 原跳转逻辑 | App 端（若本期仅 Web，见 TC-ENV-001） |
| AQDQVAN / AQDQ 权限字段显隐 | 其他品类订单详情（除非复用组件） |

---

## 3. 测试数据准备

| 数据编号 | 订单类型 | Quotation ID 示例 | Payoff / 标的 | 权限账号 | 用途 |
|----------|----------|-------------------|---------------|----------|------|
| D-FCN-01 | FCN 询价下单 | 10420260515138 | AAPL.US 等 | 全量询价权限 | 主路径（对齐原型） |
| D-FCN-02 | FCN 询价下单 | 有效 ID | 多 Payoff | 全量权限 | 多 Payoff 摘要列表 |
| D-AQDQVAN-01 | AQDQVAN | 有效 ID | — | **无** credit charge | 敏感字段隐藏 |
| D-AQDQVAN-02 | AQDQVAN | 有效 ID | — | **有** credit charge | 敏感字段可见 |
| D-AQDQ-01 | AQDQ | 有效 ID | — | **受限** user uf | 字段按 uf 限制 |
| D-AQDQ-02 | AQDQ | 有效 ID | — | **完整** user uf | 字段完整展示 |
| D-NO-RFQ-01 | 非询价单 | 无或空 | — | 普通用户 | 无 ⓘ 或不可用 |

**环境：** SIT / UAT；订单状态至少到达 **Created / Parked**（与原型步骤条一致即可打开详情）。

**摘要字段基准（与询价 Best Price 对齐，以产品字段表为准）：**  
Currency、Underlying、Strike(%)、KO Type、KO(%)、Coupon p.a.(%)、Gross Margin(%)、Note Price(%)、Tenor(m)、Barrier Type KI(%)、Effective Date Offset、Issue Date、Final Valuation Date、Maturity Date 等。

---

## 4. 可执行用例清单

> **执行说明：** 每条用例独立执行；填写「实际结果」「状态」列。

### 4.1 UI 与交互

| 用例ID | 优先级 | 前置条件 | 测试步骤 | 预期结果 | 实际结果 | 状态 |
|--------|--------|----------|----------|----------|----------|------|
| TC-UI-001 | P0 | D-FCN-01；打开 Trade Order Details | 1. 查看 General Info · **Quotation ID** 行 | 1. 展示 ID `10420260515138`（或与数据一致）<br>2. ID **右侧** 有 ⓘ 图标（样式与原型一致）<br>3. 图标与 ID 垂直居中对齐 | | |
| TC-UI-002 | P0 | D-FCN-01 | 1. 鼠标悬停 ⓘ（若设计有 tooltip） | 有 hover 提示（如「查看询价摘要」）或无明显报错 | | |
| TC-UI-003 | P0 | D-FCN-01 | 1. **仅点击 ⓘ**<br>2. 观察页面 | 1. 打开摘要浮层/弹窗<br>2. **当前页不跳转**<br>3. 浮层可关闭（X / 点击遮罩 / ESC） | | |
| TC-UI-004 | P0 | D-FCN-01 | 1. **点击 Quotation ID 文本**（非 ⓘ） | 1. 跳转至对应 **询价页/询价历史**<br>2. 与优化前行为一致 | | |
| TC-UI-005 | P1 | D-FCN-01 | 1. 打开摘要后点击 ID 文本 | 1. 摘要可先关闭或保持；ID 点击仍正常跳转（以设计为准，不得死链） | | |
| TC-UI-006 | P1 | D-NO-RFQ-01 | 1. 打开非询价下单详情 | 无 Quotation ID 或无 ⓘ；页面无 JS 报错 | | |

### 4.2 摘要内容与数据准确性

| 用例ID | 优先级 | 前置条件 | 测试步骤 | 预期结果 | 实际结果 | 状态 |
|--------|--------|----------|----------|----------|----------|------|
| TC-DATA-001 | P0 | D-FCN-01 | 1. 点击 ⓘ 打开摘要<br>2. 对照询价页该 Quotation **Best Price** | 摘要中各字段与 Best Price **一致**（含币种、百分比、日期格式） | | |
| TC-DATA-002 | P0 | D-FCN-02 多 Payoff | 1. 打开摘要 | 1. **每个 Payoff** 均有 Best Price 摘要区块<br>2. 区块标题可区分 Payoff/标的<br>3. 顺序与询价页一致 | | |
| TC-DATA-003 | P1 | D-FCN-01 | 1. 对比摘要与详情页下方参数表 | 详情表与摘要 **同源**：不因摘要展示导致详情表数据变化 | | |
| TC-DATA-004 | P1 | 询价端更新 Best Price 后 | 1. 刷新订单详情<br>2. 再点 ⓘ | 摘要展示 **最新** Best Price，非缓存旧值 | | |
| TC-DATA-005 | P2 | D-FCN-01 | 1. 检查 Gross Margin、Note Price 等 | 与原型/询价页一致；空值显示 `--` 或留空规则统一 | | |

### 4.3 权限（AQDQVAN / AQDQ）

| 用例ID | 优先级 | 前置条件 | 测试步骤 | 预期结果 | 实际结果 | 状态 |
|--------|--------|----------|----------|----------|----------|------|
| TC-PERM-001 | P0 | D-AQDQVAN-01 无 credit charge | 1. 打开 AQDQVAN 询价下单详情<br>2. 点击 ⓘ | 受 `credit charge` 限制的字段 **不展示或脱敏**（与询价页权限一致） | | |
| TC-PERM-002 | P0 | D-AQDQVAN-02 有 credit charge | 1. 同上 | 敏感字段 **可见**，与询价页 Best Price 可见性一致 | | |
| TC-PERM-003 | P0 | D-AQDQ-01 受限 user uf | 1. 打开 AQDQ 订单详情<br>2. 点击 ⓘ | 按 `user uf` 限制隐藏/禁用字段；**不少于**询价页已授权范围 | | |
| TC-PERM-004 | P0 | D-AQDQ-02 完整 user uf | 1. 同上 | 摘要字段完整展示 | | |
| TC-PERM-005 | P1 | 两账号对比 | 1. 高权限 vs 低权限各打开同一 Quotation 摘要 | 低权限 **看不到** 的字段在高权限可见；不得越权露出 | | |
| TC-PERM-006 | P2 | 无询价权限用户 | 1. 直接访问订单详情 URL | 无权限时 ⓘ 不展示或点击提示无权限；不通过摘要泄露数据 | | |

### 4.4 边界与异常

| 用例ID | 优先级 | 前置条件 | 测试步骤 | 预期结果 | 实际结果 | 状态 |
|--------|--------|----------|----------|----------|----------|------|
| TC-EDGE-001 | P1 | Quotation 无 Best Price | 1. 点击 ⓘ | 友好提示（如「暂无最优价数据」）；不白屏 | | |
| TC-EDGE-002 | P2 | 超长 Quotation ID | 1. 查看 ID + ⓘ 布局 | ID 换行/省略时 ⓘ 仍可见可点 | | |
| TC-EDGE-003 | P2 | 弱网 / 接口慢 | 1. 点击 ⓘ | Loading 状态；超时提示可重试 | | |
| TC-EDGE-004 | P2 | 接口 500 | 1. 模拟摘要接口失败 | 错误提示；不影响 ID 跳转与其它 General Info | | |

### 4.5 回归与兼容

| 用例ID | 优先级 | 前置条件 | 测试步骤 | 预期结果 | 实际结果 | 状态 |
|--------|--------|----------|----------|----------|----------|------|
| TC-REG-001 | P0 | D-FCN-01 | 1. 检查步骤条 Created/Parked/…<br>2. Requested By、Trade Order ID、Order Type、Tenor ID | 与原页面一致，无布局错位 | | |
| TC-REG-002 | P1 | D-FCN-01 | 1. 检查下方 Underlying/Coupon/Tenor 表 | 表格排序、滚动、导出（若有）无回归 | | |
| TC-REG-003 | P1 | 从 Quotation → RFQ History 入口 | 1. 经列表进入同一订单 | Quotation ID、ⓘ、摘要行为与 Blotter 进入一致 | | |

### 4.6 环境与范围

| 用例ID | 优先级 | 前置条件 | 测试步骤 | 预期结果 | 实际结果 | 状态 |
|--------|--------|----------|----------|----------|----------|------|
| TC-ENV-001 | P1 | 确认本期范围 | 1. 与 PM 确认 Web/App | 若仅 Web：App 无 ⓘ 或排期下一版本（记录 N/A） | | |
| TC-ENV-002 | P2 | Chrome / Edge / Safari | 1. 分别打开摘要浮层 | 样式与关闭交互一致 | | |

---

## 5. 执行优先级

| 轮次 | 用例 |
|------|------|
| **冒烟** | TC-UI-001～004、TC-DATA-001、TC-PERM-001/003、TC-REG-001 |
| **全量** | 上表全部 |
| **权限专项** | TC-PERM-001～006 |

---

## 6. 通过准则

- P0 **100%** 通过。
- ⓘ 摘要与询价 Best Price **不一致** → **Blocker**。
- 权限 **越权展示** → **Blocker**。
- Quotation ID **无法跳转**询价页 → **Blocker**。

---

## 7. 关联文档

| 文件 | 说明 |
|------|------|
| [询价下单-QuotationID摘要-测试用例.xmind](./询价下单-QuotationID摘要-测试用例.xmind) | XMind 脑图 |
| [需求原型-QuotationID信息图标.png](./需求原型-QuotationID信息图标.png) | 需求截图 |
