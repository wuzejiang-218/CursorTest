# 结构化金融产品测试 — 使用示例

## 调用方式

```text
请使用 structured-finance-testcase，根据 Easyconnect/quotation/lastlook 知识库，
输出案例分析 MD、cases.json、XMind 和冒烟 Excel，放到 test-cases/v361/询价-LastLook同步最优价/
```

---

## 示例一：询价 — ELN 多行 UF 校验

### 输入摘要

- 产品：EasyConnect · Quotation · ELN Tab
- 规则：多行除 UF 外条款相同则 Submit 拦截

### 案例分析 MD 片段

| 类别 | 示例条目 |
|------|----------|
| 需求点 RP-01 | ≥2 行 ELN 且仅 UF 不同 → 拦截 Submit |
| 影响点 IP-01 | ELN 新增/编辑页、Submit 前端校验 |
| 风险点 RK-01 | 误拦/漏拦导致错误提交或错误拦截 |
| 回归点 RG-01 | FCN 等其他 Tab 不触发 ELN 专用提示 |

### cases.json 片段

```json
{
  "title": "v3.61 · ELN UF 重复校验",
  "output_prefix": "ELN-询价UF重复校验-覆盖输出",
  "case_id_prefix": "TC-ELN-COV",
  "smoke_ratio": 0.2,
  "cases": [
    {
      "requirement": "ELN 多行除 UF 外相同拦截",
      "module": "核心拦截",
      "title": "英文环境两行仅 UF 不同提交被拦截",
      "test_data": "两行 ELN；Currency=USD；Underlying=3888.HK；Strike=95；Tenor=6；UF=1 和 1.2；其余字段相同",
      "precondition": "系统语言 English；位于 ELN Tab",
      "steps": ["新增 2 行", "仅 UF 不同", "Submit"],
      "expected": "拦截；英文提示正确；数据保留",
      "priority": "P0",
      "is_smoke": true
    }
  ]
}
```

### 生成命令

```bash
python .cursor/skills/testcase-xmind-smoke-output/scripts/generate_xmind_smoke_excel.py \
  test-cases/v361/ELN-询价UF重复校验/ELN-询价UF重复校验-覆盖输出-cases.json \
  test-cases/v361/ELN-询价UF重复校验/
```

---

## 示例二：询价 — Last Look 同步最优价

### 输入摘要

- 机构/Issuer 双端 Last Look 配置
- 非最优 Issuer 可申请同步最优价

### 案例分析要点

| 类别 | 示例 |
|------|------|
| 需求点 | Manual/Automatic 发起；Issuer 邮件/自动/手工确认 |
| 影响点 | Organization Setting、Issuer Setting、Lastlook 列表、邮件通知 |
| 风险点 | 双向配置不匹配、确认时最优价变化、有效期叠加 |
| 回归点 | 询价创建、首次回复、比价引擎 |

### 冒烟必选（结构化产品询价）

1. 双向配置成功创建申请
2. 非最优可发起 / 最优不可发起
3. Issuer 确认后最优价更新
4. 超时失效

---

## 示例三：下单 — Quotation ID 摘要

### 输入摘要

- 订单详情展示 Quotation ID 信息图标与 Best Price 摘要浮层

### 案例分析要点

| 类别 | 示例 |
|------|------|
| 需求点 | 图标展示、浮层字段、权限控制 AQDQ/AQDQVAN |
| 影响点 | Trade Order Details、Blotter、跳转询价页 |
| 风险点 | 权限泄露 credit charge / user uf；摘要与源询价不一致 |
| 回归点 | 原订单详情字段、分享卡片一致性 |

---

## 示例四：存续 — 事实值与事件时间编辑

### 输入摘要

- Event Schedule 触发事件结束后可编辑事实值与事件时间
- 8 类产品矩阵

### 案例分析要点

| 类别 | 示例 |
|------|------|
| 需求点 | 产品×事件矩阵、可编辑字段、保存校验 |
| 影响点 | 存续详情页、事件列表、后端持久化 |
| 风险点 | 错误产品类型误开放编辑；历史事件被误改 |
| 回归点 | 只读展示、敲入敲出原逻辑、日期计算 |

### 模块划分建议

1. 产品详情 UI（Limit Price 等展示）
2. 事件日程可编辑矩阵（按产品拆分用例文件可选）
3. 负向与权限
4. 端到端：触发事件结束 → 编辑 → 保存 → 刷新验证

---

## 交付物对照

| 阶段 | 文件 | 说明 |
|------|------|------|
| 分析 | `*-案例分析.md` | 需求/影响/风险/回归 |
| 设计 | `*-cases.json` | 全量用例结构化数据 |
| 主交付 | `*-测试用例.xmind` | 含 TC 编码与 [SMOKE] |
| 执行 | `*-冒烟测试用例.xlsx` | 标题无编码，含测试数据列 |
