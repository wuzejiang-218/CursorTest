# ELN 询价 · 除 UF 外条款相同拦截

v3.61：**ELN** 多行询价时，若仅 **UF (%)** 不同、其余条款相同，前端 **Submit** 拦截并提示。

## 文件

| 文件 | 用途 |
|------|------|
| `ELN-询价UF重复校验-测试用例.md` | 可执行用例表 |
| `ELN-询价UF重复校验-测试用例.xmind` | XMind 脑图 |
| `需求原型-ELN-UF校验.png` | 需求原型 |
| `build_xmind.py` | 重新生成脑图 |

## 重新生成 XMind

> 脑图不含 `TC-*` 编号，规范见 [xmind-output-rules.md](../../xmind-output-rules.md)。

```bash
cd test-cases/v361/ELN-询价UF重复校验
python build_xmind.py
```

## 需求一句话

> 多行 ELN 除 UF 外完全相同则不允许提交；英文/中文提示见用例文档。
