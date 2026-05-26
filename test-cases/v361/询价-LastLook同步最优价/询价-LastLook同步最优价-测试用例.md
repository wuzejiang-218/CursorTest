# 询价 Last Look（同步最优价）— 测试用例（可执行）

| 项目 | 内容 |
|------|------|
| **需求摘要** | 机构对**非最优** Issuer 发起同步回复申请，Issuer 确认后报价同步为最优价；机构 **Manual/Automatic** 发起，Issuer **邮件/自动/手工** 确认 |
| **产品** | EasyConnect · Quotation · Lastlook · Organization/Issuer Last Look Setting |
| **知识库** | [lastlook/README.md](../../../Easyconnect/quotation/lastlook/README.md) v1.2 |
| **参考原型** | [机构配置](./需求原型-机构LastLook配置.png)、[Issuer配置](./需求原型-IssuerLastLook配置.png) |
| **版本** | v3.61 |
| **编写日期** | 2026-05-25 |
| **需求分析** | [需求分析简报.md](./需求分析简报.md) |

---

## 1. 测试判定标准

### 1.1 申请状态机

| 状态 | 进入条件 | 退出/终态 |
|------|----------|-----------|
| 待确认 | 创建成功 | → 已确认 / 已拒绝 / 已失效 |
| 已确认 | Issuer 确认 | 终态；回复价与最优价已更新 |
| 已拒绝 | Issuer 拒绝 | 终态；价格不变 |
| 已失效 | 超时、询价关闭、新回复覆盖、配置不匹配等 | 终态；价格不变 |

### 1.2 发起判定（手动+自动共用）

须同时满足：询价可比价；Matched Issuer；Issuer 有 Matched Buyside 行；有效回复且**非最优**；无同组合待确认/已确认；Manual 时用户已授权；自动时满足 Product/Trigger/价差；Price Validity 未过期。

---

## 2. 测试范围

| 在范围（Zone 1） | 不在范围（Zone 3） |
|------------------|------------------|
| 机构/Issuer Last Look Setting | 机构代 Issuer 直接改价 |
| 双向匹配、手动/自动发起 | 已确认申请撤回后再发起 |
| 申请状态、Issuer 确认、失效规则 | 询价创建/首次回复流程改造 |
| Lastlook 比价与申请展示 | |
| Zone 2：询价+回复+比价集成冒烟 | |

---

## 3. 测试数据准备

| 数据编号 | 机构 | Issuer | 机构配置要点 | Issuer 配置要点 |
|----------|------|--------|--------------|-----------------|
| D-BASE-AUTO | CAI HK | CACIB PG | Mode=Automatic, Issuer=CACIB, Product=FCN, Trigger=5min, Validity=20min | Buyside=CAI HK, MatchTime=20min, Reply=邮件 |
| D-BASE-MAN | CAI HK | CACIB PG | Mode=Manual, 授权=U1 | 同 D-BASE-AUTO |
| D-DIFF-10BP | CAI HK | CACIB PG | Difference Value=10bp | 同左 |
| D-NO-MATCH | CAI HK | CACIB PG | Issuer=CACIB | **无** CAI HK Buyside 行 |
| D-SG-ROW | CAI SG | CACIB PG | Issuer=CACIB | Buyside=CAI SG, MatchTime=-- |
| D-REPLY-AUTO | CAI HK | CACIB PG | Automatic | Reply Mode=Automatic |
| D-PVP-15 | CAI HK | CACIB PG | Validity=20min | Price Validity=15min |

**询价场景约定：**

- **INQ-FCN-2ISS**：FCN 询价，参与 Issuer 含 CACIB + 另一 Issuer；CACIB 回复非最优
- **INQ-BEST-CACIB**：CACIB 为当前最优 Issuer
- **U1/U2**：机构用户，U1 授权、U2 未授权

---

## 4. 可执行用例清单

### 4.1 模块1：机构 Last Look Setting（ORG）

| 用例ID | 优先级 | 类型 | 前置条件 | 测试步骤 | 预期结果 | 依据 |
|--------|--------|------|----------|----------|----------|------|
| TC-LL-ORG-001 | P0 | 功能 | 机构管理员 | 1. Organization → Last Look Setting<br>2. 配置 Matched Issuer=CACIB, Mode=Automatic, Validity=20min<br>3. 保存 | 保存成功；再次进入显示一致 | BR-ORG-01 |
| TC-LL-ORG-002 | P0 | 功能 | 机构管理员 | 1. 配置 Automatic 条件：Product=FCN, Trigger=5min<br>2. 保存 | 子项持久化 | AC-C01 |
| TC-LL-ORG-003 | P1 | 功能 | 机构管理员 | 1. 切换 Mode=Manual<br>2. 选择授权用户 U1<br>3. 保存 | Manual + U1 生效 | AC-C03 |
| TC-LL-ORG-004 | P0 | 异常 | Mode=Manual, 授权为空 | 1. 清空授权用户<br>2. 保存 | 保存成功或警告（以实现为准） | AC-C04 |
| TC-LL-ORG-005 | P1 | 边界 | — | 1. 设置 Best Price Difference Value=10bp<br>2. 保存 | 阈值持久化 | AC-C02 |
| TC-LL-ORG-006 | P2 | 边界 | — | 1. Difference Value=-- 或未配置<br>2. 保存 | 不按价差拦截自动触发 | G-04 |
| TC-LL-ORG-007 | P1 | 功能 | — | 1. 修改 Validity=30min<br>2. 创建申请 | 待确认有效期按 30min 计算 | BR-ORG |
| TC-LL-ORG-008 | P2 | 边界 | — | 1. Validity 最小值（如 1min） | 系统接受或校验提示 | 边界 |
| TC-LL-ORG-009 | P1 | 安全 | 机构普通用户 | 1. 尝试进入 Last Look Setting | 无编辑权限或只读 | SR-01 |
| TC-LL-ORG-010 | P0 | 功能 | 原型对齐 | 1. 对照 [机构原型](./需求原型-机构LastLook配置.png) 逐项配置 | 字段与原型一致 | UI |
| TC-LL-ORG-011 | P2 | 异常 | 必填项为空 | 1. Matched Issuer 为空保存 | 校验失败或禁止保存 | 异常 |
| TC-LL-ORG-012 | P2 | 功能 | 多 Issuer（若支持） | 1. 配置多个 Matched Issuer | 仅匹配 Issuer 进入候选 | G-05 |
| TC-LL-ORG-013 | P1 | 功能 | D-BASE-AUTO | 1. 修改 Product 为非 FCN 产品询价 | 非 FCN 不自动触发 | 自动条件 |
| TC-LL-ORG-014 | P2 | 回归 | — | 1. 保存后切换 Tab 再返回 | 配置不丢失 | 回归 |
| TC-LL-ORG-015 | P3 | 性能 | — | 1. 打开 Setting 页 | 加载 ≤3s（环境基线） | 性能 |
| TC-LL-ORG-016 | P1 | 功能 | Automatic | 1. 授权列表配置 U1（自动模式） | 记录可审计；是否可手工补发见 G-03 | G-03 |
| TC-LL-ORG-017 | P2 | 边界 | Trigger 未满足 | 1. 回复未满 5min | 不自动创建 | AC-C01 负向 |
| TC-LL-ORG-018 | P1 | 功能 | — | 1. 删除/禁用机构配置 | Lastlook 不可发起或提示配置 | 异常 |

### 4.2 模块2：Issuer Last Look Setting（ISS）

| 用例ID | 优先级 | 类型 | 前置条件 | 测试步骤 | 预期结果 | 依据 |
|--------|--------|------|----------|----------|----------|------|
| TC-LL-ISS-001 | P0 | 功能 | Issuer 管理员 | 1. Issuers → CACIB PG → Last Look Setting<br>2. 新增行 Buyside=CAI HK, MatchTime=20min<br>3. Reply Mode View 配置邮件 | 保存成功 | AC-I01 |
| TC-LL-ISS-002 | P0 | 功能 | — | 1. 再增行 Buyside=CAI SG | 多行独立参数 | 03§3.2 |
| TC-LL-ISS-003 | P1 | 功能 | — | 1. Reply Mode 改为 Automatic | confirm_channel 将为 automatic | AC-I04 |
| TC-LL-ISS-004 | P1 | 功能 | — | 1. Reply Mode 改为 Manual | Issuer 待办确认 | AC-04～07 |
| TC-LL-ISS-005 | P0 | 集成 | D-BASE-AUTO + 双向配置 | 1. 触发 Last Look | 创建申请；记录 issuer_buyside_row_id | AC-I01 |
| TC-LL-ISS-006 | P1 | 功能 | — | 1. 设置 Price Validity=15min | 保存成功 | AC-I05 |
| TC-LL-ISS-007 | P0 | 异常 | D-NO-MATCH | 1. 删除 CAI HK 行<br>2. 机构触发 | 不创建；提示配置不匹配 | AC-I02 |
| TC-LL-ISS-008 | P1 | 异常 | 机构未配 CACIB | 1. Issuer 有行但机构 Matched Issuer 不含 CACIB | 不创建 | 双向匹配 |
| TC-LL-ISS-009 | P1 | 安全 | 机构管理员 | 1. 尝试编辑 Issuer Last Look Setting | 无权限 | SR-01 |
| TC-LL-ISS-010 | P0 | 异常 | D-NO-MATCH | 1. 机构 CAI HK 发起 | 明确错误提示 Issuer/机构不匹配 | AC-I02 |
| TC-LL-ISS-011 | P2 | 功能 | 原型对齐 | 1. 对照 [Issuer原型](./需求原型-IssuerLastLook配置.png) | 列表字段一致 | UI |
| TC-LL-ISS-012 | P1 | 边界 | D-SG-ROW | 1. CAI SG 行 MatchTime=--<br>2. CAI SG 询价满足其它条件 | 按默认规则或不允许（对齐 G-01） | AC-I03 |
| TC-LL-ISS-013 | P2 | 边界 | Price Validity=-- | 1. 不配置 PVP | 仅受机构 Validity 约束 | G-02 |
| TC-LL-ISS-014 | P2 | 异常 | 禁用 Buyside 行 | 1. enabled=false | 不创建申请 | 08§8.3 |
| TC-LL-ISS-015 | P1 | 边界 | AC-I03 | 1. 记录实际行为与产品确认 | 用例结果标注通过/阻塞 | AC-I03 |
| TC-LL-ISS-016 | P2 | 回归 | — | 1. View 子页取消/保存 | 不污染列表页 | 回归 |
| TC-LL-ISS-017 | P3 | 功能 | — | 1. 修改 MatchTime 与机构 Trigger 不一致 | 取较严者（假设 G-02） | G-02 |
| TC-LL-ISS-018 | P1 | 功能 | 邮件模式 | 1. 创建申请 | 发送邮件含确认/拒绝链接 | AC-04 |

### 4.3 模块3：发起条件与拦截（PRE）

| 用例ID | 优先级 | 类型 | 前置条件 | 测试步骤 | 预期结果 | 依据 |
|--------|--------|------|----------|----------|----------|------|
| TC-LL-PRE-001 | P0 | 功能 | INQ-FCN-2ISS, CACIB 非最优 | 1. 手动或自动发起 | 创建待确认；trigger_mode 正确 | AC-01 |
| TC-LL-PRE-002 | P0 | 功能 | INQ-BEST-CACIB | 1. 对 CACIB 发起 | **拒绝**；最优不可发起 | AC-02 |
| TC-LL-PRE-003 | P1 | 功能 | 另一 Issuer 非最优 | 1. 对非 Matched Issuer 发起 | 拒绝或不可见入口 | BR-ORG-01 |
| TC-LL-PRE-004 | P0 | 异常 | 询价已关闭 | 1. 尝试发起 | 拒绝；不创建 | STA |
| TC-LL-PRE-005 | P1 | 异常 | 回复已作废 | 1. 对作废回复发起 | 拒绝 | 06§6.1 |
| TC-LL-PRE-006 | P1 | 异常 | 草稿未提交回复 | 1. 对草稿发起 | 拒绝 | 06§6.1 |
| TC-LL-PRE-007 | P0 | 异常 | 已有待确认申请 | 1. 同 inquiry+issuer+reply 再次发起 | **拦截** | AC-03 |
| TC-LL-PRE-008 | P0 | 异常 | 已有已确认申请 | 1. 同组合再发起 | **拦截** | BR-PRE-03 |
| TC-LL-PRE-009 | P1 | 功能 | 待确认期间 Issuer 新回复 | 1. 新回复提交 | 原申请**已失效**；可按新回复再评估 | 05§5.3 |
| TC-LL-PRE-010 | P0 | 功能 | INQ-BEST-CACIB | 1. Lastlook 入口 | 对最优行无「发起」或置灰 | AC-02 |
| TC-LL-PRE-011 | P1 | 边界 | 价差=最优 | 1. 价格等于最优（非优方另一 Issuer） | 不可发起 | BR-PRE-01 |
| TC-LL-PRE-012 | P2 | 集成 | Zone 2 | 1. 仅 1 个 Issuer 回复 | 比价与最优正确；发起逻辑仍适用 | INT |
| TC-LL-PRE-013 | P1 | 功能 | D-PVP-15 过期 | 1. 回复超 15min 后发起 | 拒绝或已失效 | AC-I05 |
| TC-LL-PRE-014 | P0 | 功能 | 有效回复 | 1. 检查 applicant_reply_id | 绑定正确 reply_id | 08§8.1 |
| TC-LL-PRE-015 | P1 | 异常 | 双向不匹配 | 1. D-NO-MATCH 触发 | 不创建 | AC-I02 |
| TC-LL-PRE-016 | P2 | 边界 | 多 Issuer 回复 | 1. 最优切换后 | 仅非最优方可对新回复发起 | AC-09 |
| TC-LL-PRE-017 | P1 | 功能 | — | 1. 创建时记录 target_best_price 快照 | 字段有值且合理 | 06§6.3 |
| TC-LL-PRE-018 | P2 | 异常 | 询价不可比价状态 | 1. 草稿询价 | 不可发起 | 05§5.2-1 |
| TC-LL-PRE-019 | P1 | 功能 | — | 1. 幂等：自动+手动同时满足 | 仅 **1** 条待确认 | BR-CON-02 |
| TC-LL-PRE-020 | P0 | 异常 | AC-03 | 1. 重复点击发起按钮 | 仍仅一条申请 | AC-03 |
| TC-LL-PRE-021 | P2 | 功能 | 买/卖方向 | 1. 卖向询价更优价高；买向更优价低 | 与询价引擎一致 | 06§6.1 |
| TC-LL-PRE-022 | P1 | 集成 | — | 1. 排除过期/作废回复后比价 | 最优价计算正确 | 06§6.1 |

### 4.4 模块4：手动发起（MAN）

| 用例ID | 优先级 | 类型 | 前置条件 | 测试步骤 | 预期结果 | 依据 |
|--------|--------|------|----------|----------|----------|------|
| TC-LL-MAN-001 | P0 | 功能 | D-BASE-MAN, U1 | 1. U1 在 Lastlook 对非最优 CACIB 发起 | 创建成功；trigger_mode=manual | AC-C03 |
| TC-LL-MAN-002 | P0 | 异常 | D-BASE-MAN, U2 未授权 | 1. U2 发起 | **拒绝** | AC-C03 |
| TC-LL-MAN-003 | P0 | 功能 | AC-C03 | 1. U1 发起后查申请单 | applicant_user_id=U1 | AC-C03 |
| TC-LL-MAN-004 | P0 | 异常 | Manual, 授权为空 | 1. 任意用户发起 | 拒绝；提示配置 Setting | AC-C04 |
| TC-LL-MAN-005 | P1 | 功能 | Automatic 模式 | 1. 授权 U1 手工补发（G-03 假设允许） | 创建成功 | G-03 |
| TC-LL-MAN-006 | P1 | 异常 | Automatic 模式 | 1. 未授权 U2 手工补发 | 拒绝 | G-03 |
| TC-LL-MAN-007 | P2 | 功能 | — | 1. Lastlook 按钮/菜单入口 | 仅 Manual 或补发场景可见 | UI |
| TC-LL-MAN-008 | P1 | 边界 | 并发点击 | 1. U1 双击发起 | 仍一条申请 | 幂等 |
| TC-LL-MAN-009 | P2 | 回归 | — | 1. 发起后刷新页面 | 申请列表仍显示 | 回归 |
| TC-LL-MAN-010 | P0 | 异常 | AC-C04 | 1. 提示文案检查 | 含 Last Look Setting 配置指引 | AC-C04 |
| TC-LL-MAN-011 | P2 | 安全 | — | 1. 审计日志 | 记录手动发起人与时间 | 审计 |
| TC-LL-MAN-012 | P1 | 功能 | — | 1. 发起后 Issuer 通知 | 按 Reply Mode 通知 | PR-主流程 |

### 4.5 模块5：自动发起（AUT）

| 用例ID | 优先级 | 类型 | 前置条件 | 测试步骤 | 预期结果 | 依据 |
|--------|--------|------|----------|----------|----------|------|
| TC-LL-AUT-001 | P0 | 功能 | D-BASE-AUTO, AC-C01 | 1. FCN 询价 CACIB 回复满 5min 且非最优 | 自动创建待确认；trigger_mode=automatic | AC-C01 |
| TC-LL-AUT-002 | P0 | 功能 | — | 1. 创建后 20min 内未确认 | 第 20min 后状态=已失效 | AC-C01 |
| TC-LL-AUT-003 | P1 | 功能 | 回复未满 5min | 1. 等待 4min | 不创建 | AC-C01 负向 |
| TC-LL-AUT-004 | P0 | 异常 | D-DIFF-10BP, 价差 15bp | 1. 满足其它自动条件 | **不**自动创建 | AC-C02 |
| TC-LL-AUT-005 | P1 | 功能 | D-DIFF-10BP, 价差 8bp | 1. 满足其它条件 | 自动创建 | AC-C02 |
| TC-LL-AUT-006 | P1 | 功能 | Product≠FCN | 1. 非 FCN 询价 | 不自动创建 | 02§2.3 |
| TC-LL-AUT-007 | P1 | 边界 | 价差=10bp 边界 | 1. 恰好 10bp | 创建（≤阈值） | 边界 |
| TC-LL-AUT-008 | P2 | 功能 | Manual 模式 | 1. 满足自动条件 | 不自动创建 | 02§2.4 |
| TC-LL-AUT-009 | P1 | 功能 | — | 1. 自动创建后查 validity_minutes | =20（机构配置） | 08§8.1 |
| TC-LL-AUT-010 | P0 | 异常 | AC-C02 | 1. 日志/界面无申请记录 | 确认未静默失败 | AC-C02 |
| TC-LL-AUT-011 | P1 | 功能 | Issuer 更新回复 | 1. 回复更新后重新计时 5min | 按新回复评估 | 02§2.3 |
| TC-LL-AUT-012 | P2 | 性能 | — | 1. 多 Issuer 同时满 5min | 各候选独立评估；无卡顿 | 性能 |
| TC-LL-AUT-013 | P1 | 功能 | — | 1. 自动创建通知 Issuer | 邮件/待办按 Reply Mode | AC-I01 |
| TC-LL-AUT-014 | P2 | 边界 | Difference 未配置 | 1. 大价差 | 仍自动创建 | G-04 |
| TC-LL-AUT-015 | P1 | 异常 | 最优 Issuer | 1. 仅最优回复满 5min | 不创建 | AC-02 |
| TC-LL-AUT-016 | P2 | 回归 | — | 1. 关闭 Automatic 改 Manual | 停止后续自动创建 | 回归 |
| TC-LL-AUT-017 | P1 | 功能 | — | 1. 后台任务延迟 | 在合理 SLA 内创建（如 1min 内） | 性能 |
| TC-LL-AUT-018 | P0 | 功能 | BR-CON-02 | 1. 自动已创建后 U1 手工点发起 | 不第二条待确认 | BR-CON-02 |

### 4.6 模块6：Issuer 确认通道（CFM）

| 用例ID | 优先级 | 类型 | 前置条件 | 测试步骤 | 预期结果 | 依据 |
|--------|--------|------|----------|----------|----------|------|
| TC-LL-CFM-001 | P0 | 功能 | 邮件模式, 待确认 | 1. 点击邮件确认链接 | 已确认；回复价=同步目标价；最优价更新 | AC-04 |
| TC-LL-CFM-002 | P0 | 功能 | 邮件模式 | 1. 点击拒绝链接 | 已拒绝；价格不变 | AC-05 |
| TC-LL-CFM-003 | P1 | 异常 | 邮件链接过期 | 1. 超时后点确认 | 失败或已失效 | 异常 |
| TC-LL-CFM-004 | P1 | 安全 | 邮件链接 | 1. 篡改 token | 拒绝操作 | 安全 |
| TC-LL-CFM-005 | P0 | 功能 | D-REPLY-AUTO | 1. 创建待确认 | 自动确认；confirm_channel=automatic | AC-I04 |
| TC-LL-CFM-006 | P1 | 功能 | Manual Reply | 1. Issuer 待办确认 | 已确认；channel=manual | AC-06 |
| TC-LL-CFM-007 | P1 | 功能 | Manual Reply | 1. Issuer 待办拒绝 | 已拒绝 | AC-05 |
| TC-LL-CFM-008 | P0 | 功能 | 确认前最优价变化 | 1. 创建后另一 Issuer 更优价<br>2. CACIB 确认 | 跟 **latest_best_price**；审计记录差异 | 06§6.3 |
| TC-LL-CFM-009 | P1 | 功能 | — | 1. 确认后查 confirmed_price | 与同步目标一致 | 08§8.1 |
| TC-LL-CFM-010 | P0 | 功能 | AC-I04 | 1. 验证 confirm_channel 字段 | automatic | AC-I04 |
| TC-LL-CFM-011 | P1 | 边界 | 重复确认 | 1. 已确认后再点邮件链接 | 幂等或提示已处理 | 边界 |
| TC-LL-CFM-012 | P2 | 功能 | — | 1. 确认后 Lastlook 展示 | 最优 Issuer 变为 CACIB（若其价最优） | AC-01 |
| TC-LL-CFM-013 | P1 | 异常 | 待确认时回复作废 | 1. Issuer 确认 | 失败或已失效 | 异常 |
| TC-LL-CFM-014 | P1 | 功能 | — | 1. 确认后 trigger_mode 快照 | 仍为创建时 manual/automatic | 08§8.1 |
| TC-LL-CFM-015 | P2 | 集成 | — | 1. 确认后 Blotter/订单价 | 展示新最优价（若集成） | INT |
| TC-LL-CFM-016 | P1 | 功能 | 邮件+手工混合 Issuer | 1. 不同 Buyside 不同 Mode | 各行独立确认方式 | 03§3.2 |
| TC-LL-CFM-017 | P2 | 回归 | — | 1. 拒绝后再次发起（新 reply） | 允许对新回复发起 | 05§5.3 |
| TC-LL-CFM-018 | P1 | 异常 | Zone 3 | 1. 机构用户尝试代替 Issuer 确认 | **拒绝** | 06§6.5 |
| TC-LL-CFM-019 | P0 | 功能 | AC-07 | 1. 手工确认完整步骤 | 与 AC-06 一致 | AC-06/07 |
| TC-LL-CFM-020 | P1 | 功能 | — | 1. 确认成功记录 confirmed_at | 时间戳正确 | 08§8.1 |
| TC-LL-CFM-021 | P2 | 边界 | 部分确认失败 | 1. 网络中断重试 | 最终一致 | 可靠性 |
| TC-LL-CFM-022 | P1 | 功能 | — | 1. 确认后 setting 快照 ID | 有 last_look_setting_snapshot_id | 08§8.1 |
| TC-LL-CFM-023 | P2 | 功能 | 自动拒绝规则（若有） | 1. Issuer 配置自动拒绝 | 已拒绝 | 扩展 |
| TC-LL-CFM-024 | P1 | 异常 | D-PVP-15 | 1. 超 PVP 后 Issuer 确认 | 不可确认；已失效 | AC-I05 |

### 4.7 模块7：状态与失效（STA）

| 用例ID | 优先级 | 类型 | 前置条件 | 测试步骤 | 预期结果 | 依据 |
|--------|--------|------|----------|----------|----------|------|
| TC-LL-STA-001 | P0 | 功能 | 待确认 | 1. 等待超过机构 Validity 20min | 已失效；价格不变 | AC-08 |
| TC-LL-STA-002 | P1 | 功能 | — | 1. 查 expired_at | 记录失效时间 | 08§8.1 |
| TC-LL-STA-003 | P0 | 功能 | 待确认 | 1. 关闭询价 | 所有待确认→已失效 | AC-10 |
| TC-LL-STA-004 | P1 | 功能 | AC-09 | 1. 待确认期间最优价被他人更新 | 确认时仍跟 latest；或失效策略 | AC-09 |
| TC-LL-STA-005 | P1 | 功能 | AC-11 | 1. Issuer 提交新回复 | 原申请失效 | AC-11 |
| TC-LL-STA-006 | P1 | 功能 | AC-12 | 1. 两 Issuer 并发确认不同申请 | 数据一致；无脏最优价 | AC-12 |
| TC-LL-STA-007 | P1 | 边界 | 失效边界时间 | 1. Validity 第 19:59 确认 | 仍可确认 | 边界 |
| TC-LL-STA-008 | P0 | 边界 | 失效边界时间 | 1. Validity 第 20:01 确认 | 已失效不可确认 | AC-08 |
| TC-LL-STA-009 | P1 | 功能 | 已拒绝 | 1. 尝试再次确认 | 不允许 | 状态机 |
| TC-LL-STA-010 | P0 | 功能 | AC-09 | 1. 最优切换后列表展示 | 申请状态与比价一致 | AC-09 |
| TC-LL-STA-011 | P1 | 功能 | — | 1. 已确认申请 | 不可改为待确认 | 状态机 |
| TC-LL-STA-012 | P0 | 异常 | Zone 3 | 1. 已确认后同 reply 再发起 | **拒绝** | 06§6.5 |
| TC-LL-STA-013 | P1 | 功能 | 询价关闭 | 1. 已确认申请保留 | 历史可查；不再变更 | AC-10 |
| TC-LL-STA-014 | P2 | 功能 | — | 1. 失效后 Lastlook | 显示已失效；可对新回复发起 | UI |
| TC-LL-STA-015 | P1 | 功能 | G-02 | 1. 机构 20min + Issuer PVP 15min | 15min 后不可确认（较严） | G-02 |
| TC-LL-STA-016 | P1 | 异常 | 配置变更 | 1. 待确认期间删除 Buyside 行 | 已失效或不匹配 | 异常 |
| TC-LL-STA-017 | P2 | 功能 | — | 1. 状态筛选器 | 可按待确认/已确认/已拒绝/已失效筛选 | UI |
| TC-LL-STA-018 | P1 | 功能 | — | 1. 失效后价格回复 | 仍为原 Issuer 报价（未同步） | 05§5.5 |
| TC-LL-STA-019 | P2 | 集成 | — | 1. 失效通知 Issuer | 无确认入口或提示过期 | 集成 |
| TC-LL-STA-020 | P0 | 功能 | AC-I05 | 1. D-PVP-15 场景全流程 | 申请已失效或不可确认 | AC-I05 |
| TC-LL-STA-021 | P1 | 功能 | — | 1. 定时任务扫失效 | 状态准确；无遗漏 | 可靠性 |
| TC-LL-STA-022 | P2 | 边界 | 时区 | 1. 跨时区 Validity | 按机构时区或 UTC 一致 | 边界 |
| TC-LL-STA-023 | P1 | 功能 | AC-12 | 1. DB 层并发锁 | 仅一条确认生效 | AC-12 |
| TC-LL-STA-024 | P2 | 回归 | — | 1. 失效申请不参与比价 | 最优价不受失效单影响 | 回归 |
| TC-LL-STA-025 | P1 | 功能 | — | 1. 列表排序 | 按创建时间倒序 | UI |
| TC-LL-STA-026 | P2 | 功能 | — | 1. 导出申请列表 | 含状态与 trigger_mode | 可选 |
| TC-LL-STA-027 | P1 | 异常 | 邮件延迟 | 1. 失效后邮件才到达 | 确认失败 | 异常 |
| TC-LL-STA-028 | P1 | 功能 | — | 1. 快照 target_best_issuer_id | 审计字段正确 | 06§6.3 |

### 4.8 模块8：端到端（E2E）

| 用例ID | 优先级 | 类型 | 前置条件 | 测试步骤 | 预期结果 | 依据 |
|--------|--------|------|----------|----------|----------|------|
| TC-LL-E2E-001 | P0 | 端到端 | D-BASE-MAN | 1. 配置双端→询价→回复→U1 手动发起→邮件确认 | 全链路成功；最优价更新 | PR-主流程 |
| TC-LL-E2E-002 | P0 | 端到端 | D-BASE-AUTO | 1. 配置双端→FCN 询价→5min 自动→自动确认 | automatic 全链路 | AC-C01+I04 |
| TC-LL-E2E-003 | P0 | 端到端 | 邮件拒绝 | 1. 手动发起→邮件拒绝 | 已拒绝；价不变 | AC-05 |
| TC-LL-E2E-004 | P1 | 端到端 | 超时 | 1. 自动创建→20min 不确认 | 已失效 | AC-08 |
| TC-LL-E2E-005 | P1 | 端到端 | 不匹配 | 1. 仅配机构不配 Issuer 行→发起 | 失败提示 | AC-I02 |
| TC-LL-E2E-006 | P1 | 端到端 | 最优切换 | 1. 确认前他人更优→确认 | 跟 latest 价 | 06§6.3 |
| TC-LL-E2E-007 | P2 | 端到端 | 多 Buyside | 1. CAI HK + CAI SG 两行独立流程 | 互不干扰 | 03§3.2 |
| TC-LL-E2E-008 | P1 | 端到端 | Zone 3 负向 | 1. 尝试机构代确认 | 失败 | 06§6.5 |

### 4.9 模块9：Lastlook UI 与集成（UI/INT）

| 用例ID | 优先级 | 类型 | 前置条件 | 测试步骤 | 预期结果 | 依据 |
|--------|--------|------|----------|----------|----------|------|
| TC-LL-UI-001 | P0 | 功能 | 多 Issuer 回复 | 1. 打开 Lastlook | 展示各 Issuer 价 vs 最优价 | AC-13 |
| TC-LL-UI-002 | P1 | 功能 | 有待确认 | 1. 查看申请状态列 | 显示待确认及 trigger_mode | AC-13 |
| TC-LL-UI-003 | P1 | 功能 | — | 1. 查看 Issuer Reply Mode 摘要 | 与配置一致 | AC-13 |
| TC-LL-UI-004 | P2 | 功能 | — | 1. 机构触发模式摘要 | Manual/Automatic 标识 | AC-13 |
| TC-LL-UI-005 | P2 | 回归 | — | 1. 刷新/切换询价 | 数据不串单 | 回归 |
| TC-LL-UI-006 | P1 | 集成 | Zone 2 | 1. 新建询价→回复→进 Lastlook | 无缝；最优价与询价页一致 | INT |
| TC-LL-INT-001 | P1 | 集成 | Zone 2 | 1. 首次回复流程 | 不改变原有流程 | 06§6.5 |
| TC-LL-INT-002 | P2 | 集成 | — | 1. 询价详情跳转 Lastlook | 链接正确 | INT |

---

## 5. 执行优先级

| 轮次 | 用例范围 |
|------|----------|
| **冒烟 P0** | TC-LL-ORG-001, ISS-005, PRE-001/002/007, MAN-001/002, AUT-001/004, CFM-001/005, STA-001/003, E2E-001/002, UI-001 |
| **全量** | 上表全部 ~154 条 |

---

## 6. 通过准则

- P0 **100%** 通过方可发布
- 双向不匹配仍创建申请 → **Blocker**
- 最优方可发起或重复待确认 → **Blocker**
- 确认后最优价未更新 → **Blocker**
- G-01/G-02 未对齐产品仍失败 → 标注阻塞并升级产品

---

## 7. 关联文档

| 文件 | 说明 |
|------|------|
| [需求分析简报.md](./需求分析简报.md) | 范围、规则、矩阵 |
| [三层交叉验证报告.md](./三层交叉验证报告.md) | 覆盖率验证 |
| [询价-LastLook同步最优价-测试用例.xmind](./询价-LastLook同步最优价-测试用例.xmind) | 评审脑图 |
| [需求原型-机构LastLook配置.png](./需求原型-机构LastLook配置.png) | 机构配置原型 |
| [需求原型-IssuerLastLook配置.png](./需求原型-IssuerLastLook配置.png) | Issuer 配置原型 |
