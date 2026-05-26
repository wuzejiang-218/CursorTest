# 测试案例库

按版本归档可执行测试用例、XMind 脑图与需求原型。

## 版本目录

| 版本 | 路径 | 说明 |
|------|------|------|
| **v3.61** | [v361/](./v361/) | 分享、询价摘要、ELN UF 校验、存续事实值/事件时间、询价 Last Look |

## XMind 输出规范

脑图 **不使用** `TC-UI-001` 类用例编号，仅保留业务场景描述；执行追溯见同目录 `*.md`。详见 [xmind-output-rules.md](./xmind-output-rules.md)。

## 目录规范

```
test-cases/
├── README.md
├── xmind-output-rules.md
├── _xmind_common.py       # 脑图生成公共库
└── v361/
    ├── README.md      # 版本说明
    └── <功能模块>/    # 如 FCN-OrderType-分享
        ├── *-测试用例.md
        ├── *-测试用例.xmind   # 评审用脑图（无 TC 编号）
        ├── build_xmind.py
        └── 需求原型*.png
```
