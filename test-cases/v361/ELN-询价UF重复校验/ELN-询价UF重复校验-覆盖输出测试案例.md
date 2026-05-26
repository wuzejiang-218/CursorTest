# ELN 询价 UF 重复校验 — 覆盖输出测试案例

| 项目 | 内容 |
|------|------|
| **需求摘要** | ELN 多行询价提交时，若多行**除 UF (%) 外其余条款完全相同**，前端 Submit 拦截并提示 |
| **输出标准** | [testcase-xmind-smoke-output](../../../.cursor/skills/testcase-xmind-smoke-output/SKILL.md) |
| **主交付** | [ELN-询价UF重复校验-覆盖输出-测试用例.xmind](./ELN-询价UF重复校验-覆盖输出-测试用例.xmind) |
| **冒烟 Excel** | [ELN-询价UF重复校验-覆盖输出-冒烟测试用例.xlsx](./ELN-询价UF重复校验-覆盖输出-冒烟测试用例.xlsx) |
| **结构化输入** | [ELN-询价UF重复校验-覆盖输出-cases.json](./ELN-询价UF重复校验-覆盖输出-cases.json) |
| **参考原型** | [需求原型-ELN-UF校验.png](./需求原型-ELN-UF校验.png) |
| **版本** | v3.61 |
| **生成日期** | 2026-05-25 |

---

## 1. 范围确认

| 区域 | 内容 | 用例策略 |
|------|------|----------|
| 核心区 | ELN Tab 多行 Submit 前校验、提示文案、数据保留、修改后重提 | 完整覆盖 |
| 交互区 | Tab 切换、Add/Copy 行、浏览器兼容、原有校验回归 | 回归与兼容覆盖 |
| 排除区 | 后端入库后校验、非 ELN 产品规则改造、批量导入模板 | 不生成阻塞用例，仅验证无误触发 |

---

## 2. 冒烟策略

按技能默认规则抽取冒烟：

- 总用例数：24 条
- 冒烟比例：5/24，约 20.8%
- 选择规则：P0 核心主流程 + 阻塞提交路径 + 关键放行边界

| 冒烟用例 | 选择原因 |
|----------|----------|
| TC-ELN-COV-001 | 英文核心拦截，覆盖发布阻塞主路径 |
| TC-ELN-COV-002 | 中文提示核心拦截，覆盖多语言发布风险 |
| TC-ELN-COV-003 | 三行仅 UF 不同，覆盖多行组合 |
| TC-ELN-COV-004 | 拦截后修正字段再提交，覆盖恢复路径 |
| TC-ELN-COV-005 | UF 也相同时不触发本规则，覆盖关键边界 |

---

## 3. 覆盖矩阵

| 模块 | 正向 | 异常 | 边界 | 状态/交互 | 回归/兼容 | 冒烟 |
|------|------|------|------|-----------|-----------|------|
| 核心拦截 | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| 放行场景 | ✅ | — | ✅ | — | — | ✅ |
| 字段覆盖 | ✅ | — | ✅ | — | — | — |
| 品类范围 | ✅ | ✅ | — | — | ✅ | — |
| 交互体验 | ✅ | ✅ | ✅ | ✅ | — | — |
| 兼容与回归 | ✅ | — | — | — | ✅ | — |

---

## 4. 测试数据

| 数据编号 | 行数 | 设计要点 | 预期 |
|----------|------|----------|------|
| D-BLOCK-01 | 2 | 除 UF 外全同；UF=1 / 1.2 | 拦截 |
| D-BLOCK-02 | 3 | 三行仅 UF 分别为 1 / 1.2 / 1.5，其余同 | 拦截 |
| D-PASS-01 | 2 | 除 UF 外全同；UF 也相同 | 不因此规则拦截 |
| D-PASS-02 | 2 | UF 不同，Strike 不同 | 不拦截 |
| D-PASS-03 | 2 | UF 不同，Gross Margin 不同 | 不拦截 |
| D-PASS-04 | 2 | UF 不同，Underlying 不同 | 不拦截 |
| D-PASS-05 | 1 | 单行 ELN | 不拦截 |
| D-OTHER-01 | 2 | FCN Tab 两行仅 UF 不同 | 不触发 ELN 规则 |

基准行：Currency=USD，Underlying=3888.HK，Solve For=Note Price (%)，Strike=95，KO Type=NA，Tenor=6，Gross Margin=1，日期三列相同。

---

## 5. 覆盖用例清单

| 用例ID | 是否冒烟 | 优先级 | 模块 | 用例标题 | 前置条件 | 测试步骤 | 预期结果 | 测试方法 | 需求依据 |
|--------|----------|--------|------|----------|----------|----------|----------|----------|----------|
| TC-ELN-COV-001 | 是 | P0 | 核心拦截 | 英文环境两行仅 UF 不同提交被拦截 | D-BLOCK-01；English；ELN Tab | 1. 新增 2 行 ELN<br>2. 除 UF 外字段一致，UF=1/1.2<br>3. Submit | 不提交成功；英文提示正确；数据保留 | 场景法 | 核心规则 |
| TC-ELN-COV-002 | 是 | P0 | 核心拦截 | 中文环境两行仅 UF 不同提交被拦截 | D-BLOCK-01；简体中文；ELN Tab | 1. 新增 2 行 ELN<br>2. 仅 UF 不同<br>3. Submit | 不提交成功；中文提示正确；数据保留 | 场景法 | 多语言提示 |
| TC-ELN-COV-003 | 是 | P0 | 核心拦截 | 三行仅 UF 不同提交被拦截 | D-BLOCK-02 | 1. 新增 3 行<br>2. UF=1/1.2/1.5，其余字段一致<br>3. Submit | 触发拦截；不进入成功流程 | 场景法 | 多行组合 |
| TC-ELN-COV-004 | 是 | P0 | 核心拦截 | 拦截后修改 Strike 再提交放行 | 已触发 D-BLOCK-01 拦截 | 1. 修改其中一行 Strike<br>2. 再次 Submit | 不再因本规则拦截 | 状态转换 | 修改后重提 |
| TC-ELN-COV-005 | 是 | P0 | 放行场景 | 两行完全一致含 UF 相同不触发本规则 | D-PASS-01 | 1. 填写两行完全一致 ELN<br>2. Submit | 不出现本需求指定文案 | 边界值 | UF 相同边界 |
| TC-ELN-COV-006 | 否 | P0 | 放行场景 | UF 与 Strike 同时不同不拦截 | D-PASS-02 | 1. UF 不同<br>2. Strike 不同<br>3. Submit | 不因本规则拦截 | 等价类 | 非仅 UF 不同 |
| TC-ELN-COV-007 | 否 | P1 | 放行场景 | UF 与 Gross Margin 同时不同不拦截 | D-PASS-03 | 1. UF 不同<br>2. Gross Margin 不同<br>3. Submit | 不因本规则拦截 | 等价类 | 非仅 UF 不同 |
| TC-ELN-COV-008 | 否 | P1 | 放行场景 | UF 与 Underlying 同时不同不拦截 | D-PASS-04 | 1. UF 不同<br>2. Underlying 不同<br>3. Submit | 不因本规则拦截 | 等价类 | 非仅 UF 不同 |
| TC-ELN-COV-009 | 否 | P0 | 放行场景 | 单行 ELN 不触发多行比对 | D-PASS-05 | 1. 仅填写 1 行 ELN<br>2. Submit | 不触发多行 UF 校验 | 边界值 | 单行边界 |
| TC-ELN-COV-010 | 否 | P1 | 放行场景 | 三行中任意两行仅 UF 不同即拦截 | 第 1、3 行仅 UF 不同 | 1. 新增 3 行<br>2. 构造任意一对仅 UF 不同<br>3. Submit | 存在任意一对即拦截；若产品定义不同则待确认 | 决策表 | 多行任意对 |
| TC-ELN-COV-011 | 否 | P1 | 字段覆盖 | Currency 不同则不拦截 | 两行 UF 不同，仅 Currency 不同 | 1. Currency=USD/HKD<br>2. Submit | 不因本规则拦截 | 等价类 | 比对字段 |
| TC-ELN-COV-012 | 否 | P1 | 字段覆盖 | Solve For 不同则不拦截 | 两行 UF 不同，仅 Solve For 不同 | 1. 选择不同 Solve For<br>2. Submit | 不因本规则拦截 | 等价类 | 比对字段 |
| TC-ELN-COV-013 | 否 | P1 | 字段覆盖 | Tenor 不同则不拦截 | 两行 UF 不同，仅 Tenor 不同 | 1. Tenor=6/12<br>2. Submit | 不因本规则拦截 | 等价类 | 比对字段 |
| TC-ELN-COV-014 | 否 | P1 | 字段覆盖 | 日期字段不同则不拦截 | 两行 UF 不同，仅日期字段不同 | 1. 修改 Issue Date 或 Maturity Date<br>2. Submit | 不因本规则拦截 | 边界值 | 比对字段 |
| TC-ELN-COV-015 | 否 | P2 | 字段覆盖 | KO Type 不同则不拦截 | 两行 UF 不同，仅 KO Type 不同 | 1. 修改 KO Type<br>2. Submit | 不因本规则拦截 | 等价类 | 比对字段 |
| TC-ELN-COV-016 | 否 | P1 | 品类范围 | FCN Tab 两行仅 UF 不同不触发 ELN 专用提示 | D-OTHER-01；FCN Tab | 1. 构造两行仅 UF 不同<br>2. Submit | 不出现 ELN 专用提示 | 范围分析 | 非 ELN |
| TC-ELN-COV-017 | 否 | P2 | 品类范围 | 其它产品 Tab 不加载 ELN UF 校验 | 存在其它产品 Tab | 1. 切换 Step-down FCN/Sharkfin/BEN<br>2. 执行基础提交 | 无 ELN UF 校验报错 | 回归 | 非 ELN |
| TC-ELN-COV-018 | 否 | P1 | 交互体验 | 切换 Tab 后返回 ELN 再提交仍拦截 | ELN 已填写 D-BLOCK-01 | 1. 切到 FCN<br>2. 切回 ELN<br>3. Submit | 数据保留；仍触发拦截 | 状态转换 | Tab 状态 |
| TC-ELN-COV-019 | 否 | P1 | 交互体验 | 拦截后 Submit 按钮可再次点击 | 已触发拦截 | 1. 等提示消失<br>2. 不改数据再次 Submit | 按钮可点击；继续提示；页面不卡死 | 可用性 | 交互 |
| TC-ELN-COV-020 | 否 | P2 | 交互体验 | 删除到只剩一行后提交不拦截 | D-BLOCK-01 已触发拦截 | 1. 删除一行<br>2. Submit | 不触发多行 UF 校验 | 状态转换 | 行删除 |
| TC-ELN-COV-021 | 否 | P2 | 交互体验 | 修改 UF 为相同后不触发本规则 | D-BLOCK-01 已触发拦截 | 1. 将 UF 改为相同值<br>2. Submit | 不出现本需求指定提示；其它重复规则另判 | 边界值 | UF 相同 |
| TC-ELN-COV-022 | 否 | P2 | 兼容与回归 | Chrome 与 Edge 行为一致 | D-BLOCK-01；Chrome/Edge | 1. 两浏览器分别执行核心拦截 | 拦截逻辑、提示、数据保留一致 | 兼容测试 | 浏览器 |
| TC-ELN-COV-023 | 否 | P1 | 兼容与回归 | ELN 单行合法提交原有校验不受影响 | 单行合法数据 | 1. 填写单行合法数据<br>2. Submit | 原有必填、格式、日期校验正常；无本需求提示 | 回归 | 原有流程 |
| TC-ELN-COV-024 | 否 | P1 | 兼容与回归 | Add 行与 Copy 行后仍按最新数据比对 | ELN Tab 支持 Add/Copy | 1. 新增或复制一行<br>2. 调整为仅 UF 不同<br>3. Submit | 按当前最新行数据校验并拦截 | 回归 | 行操作 |

---

## 6. 质量检查清单

- [x] XMind 主交付已规划为最终输出
- [x] 冒烟节点使用 `[SMOKE]` 标记
- [x] 冒烟比例约 20%
- [x] Excel 冒烟字段顺序符合技能标准
- [x] 每条用例包含前置、步骤、预期
- [x] 已覆盖正向、异常、边界、交互、兼容、回归

---

## 7. 生成命令

```powershell
python ".cursor/skills/testcase-xmind-smoke-output/scripts/generate_xmind_smoke_excel.py" `
  "test-cases/v361/ELN-询价UF重复校验/ELN-询价UF重复校验-覆盖输出-cases.json" `
  "test-cases/v361/ELN-询价UF重复校验"
```
