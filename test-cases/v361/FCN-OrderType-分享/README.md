# FCN · Order Type 分享测试案例目录

本目录归档 **「分享增加 Order Type 字段（Web + App）」** 相关测试资产。

## 目录说明

| 文件 | 用途 |
|------|------|
| `FCN-OrderType-分享-测试用例.md` | 可执行用例表（含步骤、预期、执行记录列） |
| `FCN-OrderType-分享-测试用例.xmind` | XMind 脑图（模块 → 用例 → 步骤/预期） |
| `需求原型-OrderType.png` | 需求原型截图 |
| `build_xmind.py` | 重新生成 `.xmind` 的脚本 |

## 重新生成 XMind

> 脑图不含 `TC-*` 编号，规范见 [xmind-output-rules.md](../../xmind-output-rules.md)。

```bash
cd test-cases/v361/FCN-OrderType-分享
python build_xmind.py
```

## 需求一句话

> 分享增加 Order Type 字段，**Web 分享和 App 分享都需要改**；详情页需区分 **Limit Price**（含标的 @ 价格）与 **Market Price**。
