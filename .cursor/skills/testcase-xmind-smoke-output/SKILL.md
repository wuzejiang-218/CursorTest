---
name: testcase-xmind-smoke-output
description: Generate Chinese test cases from requirements with XMind as the final deliverable, mark a proportional smoke subset, and export smoke cases to an Excel table. Use when the user asks to generate test cases, XMind test cases, smoke cases, 冒烟案例, 冒烟测试, or Excel smoke execution sheets.
disable-model-invocation: false
---

# 测试案例输出技能（XMind + 冒烟 Excel）

## 角色定位

作为资深测试工程师，根据需求文档、接口说明、页面原型或用户描述生成高覆盖率测试用例。最终交付以 **XMind 脑图** 为主，同时按比例抽取并标记冒烟案例，再额外生成一份 **Excel 冒烟执行表**。

## 触发场景

当用户提出以下需求时使用本技能：

- 生成测试用例、测试案例、测试方案
- 输出 XMind 脑图
- 生成冒烟案例、冒烟测试集
- 需要把冒烟案例整理成 Excel 表格

## 输入处理

1. 读取用户提供的需求文档、接口文档、页面截图、原型图或文字说明。
2. 提取功能点、业务规则、状态流转、数据约束、权限、异常路径和风险点。
3. 使用等价类、边界值、决策表、状态转换、场景法、错误推测法组合设计用例。
4. 若信息缺失，标注「待确认」，并基于合理测试假设生成补充用例。

## 输出原则

### 1. 最终主交付必须是 XMind

最终输出需生成 `.xmind` 文件，脑图结构建议：

```text
根主题：版本 / 模块 / 需求名
├── 模块一
│   ├── [SMOKE] TC-XXX-001 核心正向流程
│   │   ├── 测试数据：...
│   │   ├── 前置：...
│   │   ├── 步骤：...
│   │   └── 预期：...
│   └── TC-XXX-002 异常流程
└── 模块二
```

要求：

- XMind 场景节点标题必须明确案例编码，格式为 `TC-前缀-序号 场景名`；冒烟用例格式为 `[SMOKE] TC-前缀-序号 场景名`。
- 冒烟用例节点标题前加 `[SMOKE]` 标记。
- 叶子节点顺序固定为 `测试数据：`、`前置：`、`步骤：`、`预期：`、`优先级：`。
- XMind 节点**不输出用例类型**（如功能/边界/异常），类型仅可保留在 JSON 或 Markdown 追溯信息中。
- 测试数据必须以文字形式明确写入 `测试数据：` 节点；不要只引用数据编号。
- 每个模块至少包含正向、异常、边界三类场景；有状态机时必须覆盖状态转换。

### 2. 冒烟案例比例

默认冒烟比例：

- **默认比例**：总用例数的 **20%**
- **最小数量**：不少于 5 条；总用例不足 5 条时全部作为冒烟
- **上限建议**：不超过 30%，除非用户指定

冒烟选择规则：

1. 必选 P0 核心主流程。
2. 必选登录/权限/下单/支付/提交/保存/状态变更等阻塞发布路径。
3. 必选高风险接口或核心数据链路。
4. P0 不足比例时，从 P1 中按业务风险补齐。
5. P2/P3 仅在用户明确要求时进入冒烟。

### 3. 冒烟 Excel 输出格式

除 XMind 外，必须额外输出一份冒烟 Excel，字段严格按以下顺序：

| 字段 | 类型 | 说明 |
|------|------|------|
| 案例需求 | 文本 | 需求/模块/功能点 |
| 用例标题 | 文本 | 明确案例场景即可，Excel 中不带案例编码，如 `英文环境两行仅 UF 不同提交被拦截` |
| 测试数据 | 文本 | 明确写出执行数据，不能只写数据编号 |
| 前置条件 | 文本 | 执行前准备 |
| 测试步骤 | 文本 | 多步骤用换行 |
| 预期结果 | 文本 | 预期行为 |
| 执行人员 | 文本 | 默认留空 |
| 冒烟结果 | 文本 | 默认留空，可填 通过/不通过/阻塞 |
| 不通过原因 | 文本 | 默认留空 |
| 开发 | 文本 | 默认留空 |

Excel 文件命名建议：

```text
<需求名>-冒烟测试用例.xlsx
```

### 4. 辅助 Markdown

如用户需要可同时生成 Markdown 追溯表，但不得替代 XMind 主交付。Markdown 表字段建议：

```text
用例ID | 是否冒烟 | 优先级 | 模块 | 用例标题 | 测试数据 | 前置条件 | 测试步骤 | 预期结果 | 测试方法 | 需求依据
```

## 推荐工作流

1. 明确测试范围：核心区、交互区、排除区。
2. 拆分模块：按业务域、页面、接口或状态机分组。
3. 设计全量用例：覆盖正向、异常、边界、权限、兼容、性能、安全、端到端。
4. 标记冒烟用例：按默认 20% 或用户指定比例选取。
5. 生成结构化用例 JSON。
6. 使用 `scripts/generate_xmind_smoke_excel.py` 输出 `.xmind` 与冒烟 `.xlsx`。
7. 校验输出：XMind 能打开，Excel 字段顺序正确，冒烟比例符合要求。

## 结构化 JSON 格式

使用脚本时，将用例整理为以下格式：

```json
{
  "title": "v3.61 冒烟案例",
  "output_prefix": "v3.61冒烟案例",
  "case_id_prefix": "TC-SMOKE",
  "smoke_ratio": 0.2,
  "cases": [
    {
      "requirement": "配置管理",
      "module": "机构配置",
      "title": "保存 Last Look 自动模式配置",
      "precondition": "机构管理员已登录",
      "test_data": "Matched Issuer=CACIB；Mode=Automatic；Product=FCN；Trigger=5min；Validity=20min",
      "steps": ["进入 Organization", "配置 Last Look Setting", "保存"],
      "expected": "保存成功，配置再次进入仍展示一致",
      "priority": "P0",
      "type": "功能",
      "is_smoke": true,
      "developer": ""
    }
  ]
}
```

若 `is_smoke` 未显式填写，脚本会按 `smoke_ratio` 和优先级自动补齐。

## 脚本

- `scripts/generate_xmind_smoke_excel.py`

运行示例：

```bash
python scripts/generate_xmind_smoke_excel.py cases.json output/
```

输出：

```text
output/
├── <output_prefix>-测试用例.xmind
└── <output_prefix>-冒烟测试用例.xlsx
```

## 质量检查清单

- [ ] XMind 已生成，节点语义清晰
- [ ] 冒烟节点有 `[SMOKE]` 标记
- [ ] 冒烟比例接近目标比例，且 P0 核心路径已覆盖
- [ ] Excel 字段顺序与表格要求一致
- [ ] Excel 仅包含冒烟案例
- [ ] 每条用例都有前置条件、测试数据、步骤、预期结果
- [ ] XMind 不输出「类型」节点
- [ ] 需求缺口已标注「待确认」
