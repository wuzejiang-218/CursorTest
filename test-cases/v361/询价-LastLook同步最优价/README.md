# 询价 Last Look（同步最优价）

v3.61：机构对非最优 Issuer 发起**同步回复申请**，Issuer 确认后报价同步为最优价。

## 文件

| 文件 | 用途 |
|------|------|
| [询价-LastLook同步最优价-测试用例.md](./询价-LastLook同步最优价-测试用例.md) | 可执行用例表（154 条，含 TC 编号） |
| [需求分析简报.md](./需求分析简报.md) | 范围、规则、模块矩阵 |
| [三层交叉验证报告.md](./三层交叉验证报告.md) | 覆盖率验证 |
| [询价-LastLook同步最优价-测试用例.xmind](./询价-LastLook同步最优价-测试用例.xmind) | XMind 脑图（评审用，无 TC 编号） |
| [需求原型-机构LastLook配置.png](./需求原型-机构LastLook配置.png) | 机构配置原型 |
| [需求原型-IssuerLastLook配置.png](./需求原型-IssuerLastLook配置.png) | Issuer 配置原型 |
| [build_xmind.py](./build_xmind.py) | 重新生成脑图 |

## 需求来源

[Easyconnect/quotation/lastlook/](../../../Easyconnect/quotation/lastlook/README.md) 知识库 v1.2

## 重新生成 XMind

> 脑图不含 `TC-*` 编号，规范见 [xmind-output-rules.md](../../xmind-output-rules.md)。

```bash
cd test-cases/v361/询价-LastLook同步最优价
python build_xmind.py
```

## 需求一句话

> 非最优 Issuer 可通过 Lastlook 申请将报价同步为最优价；机构 **Manual/Automatic** 决定如何发起，Issuer **邮件/自动/手工** 决定如何确认；须 **Matched Issuer ↔ Matched Buyside** 双向配对。

## 执行冒烟建议

TC-LL-E2E-001、E2E-002、PRE-001/002、MAN-001、AUT-001、CFM-001、STA-001、UI-001（详见用例文档 §5）
