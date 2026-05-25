# 存续 · 事实值与事件时间可编辑

v3.61：触发事件结束后，按 **产品 × 触发事件** 编辑事实值与事件时间。

## 文档结构

```
存续-事实值与事件时间编辑/
├── 存续-事实值与事件时间编辑-测试用例.md   # 索引 + 矩阵速查
├── 存续-事实值与事件时间编辑-测试用例.xmind
├── cases/                                  # 按产品×触发事件明细
│   ├── 00-通用-UI与负向.md
│   ├── 01-FCN.md              （4 个触发事件）
│   ├── 02-Step-down-FCN.md
│   ├── 03-Sharkfin.md         （2）
│   ├── 04-ELN.md              （2）
│   ├── 05-BEN.md              （2）
│   ├── 06-Step-down-SCN.md    （4，含 FF Cash A/B）
│   ├── 07-AQ.md               （3）
│   └── 08-DQ.md               （3）
└── 需求原型-*.png
```

## 用例编号规则

`TC-{产品缩写}-{触发缩写}-{类型}-{序号}`

| 类型 | 含义 |
|------|------|
| FACT | 事实值编辑 |
| TIME | 事件时间编辑 |
| NEG | 负向（未结束/越权字段） |
| ORD | 观察顺序约束 |
| DIFF | 产品间差异对比 |

示例：`TC-FCN-KO-X-FACT-001`、`TC-SCN-FF-CASH-B-NEG-001`

## 重新生成 XMind

> 脑图不含 `TC-*` 编号，规范见 [xmind-output-rules.md](../../xmind-output-rules.md)。

```bash
cd test-cases/v361/存续-事实值与事件时间编辑
python build_xmind.py
```
