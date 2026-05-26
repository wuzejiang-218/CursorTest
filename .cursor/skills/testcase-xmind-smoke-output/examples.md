# 示例：结构化输入

将需求分析后的用例保存为 `cases.json`：

```json
{
  "title": "v3.61 冒烟案例",
  "output_prefix": "v3.61冒烟案例",
  "case_id_prefix": "TC-SMOKE",
  "smoke_ratio": 0.2,
  "cases": [
    {
      "requirement": "询价 Last Look",
      "module": "机构配置",
      "title": "保存自动触发配置",
      "precondition": "机构管理员已登录",
      "test_data": "Matched Issuer=CACIB；Mode=Automatic；Product=FCN；Trigger=5min；Validity=20min",
      "steps": ["进入 Organization", "打开 Last Look Setting", "配置 Automatic 并保存"],
      "expected": "保存成功，再次进入配置保持一致",
      "priority": "P0",
      "type": "功能",
      "is_smoke": true,
      "developer": ""
    },
    {
      "requirement": "询价 Last Look",
      "module": "Issuer确认",
      "title": "邮件确认后同步为最优价",
      "precondition": "已存在待确认申请",
      "test_data": "Issuer=CACIB；当前回复价=98.50；当前最优价=99.00；Reply Mode=Email",
      "steps": ["打开邮件链接", "点击确认", "返回询价查看价格"],
      "expected": "申请状态为已确认，Issuer 回复价同步为最优价",
      "priority": "P0",
      "type": "端到端"
    }
  ]
}
```

运行：

```bash
python scripts/generate_xmind_smoke_excel.py cases.json output/
```

输出：

```text
output/
├── v3.61冒烟案例-测试用例.xmind
└── v3.61冒烟案例-冒烟测试用例.xlsx
```
