# v3.61 测试案例

本目录归档 **v3.61** 版本相关可执行测试用例与脑图。

## 子目录

| 目录 | 说明 |
|------|------|
| [FCN-OrderType-分享](./FCN-OrderType-分享/) | FCN 分享增加 **Order Type** 字段（Web + App） |
| [询价下单-QuotationID摘要](./询价下单-QuotationID摘要/) | 询价下单订单详情 **Quotation ID ⓘ 询价摘要**（Blotter） |
| [ELN-询价UF重复校验](./ELN-询价UF重复校验/) | ELN 多行询价 **仅 UF 不同** 时前端 Submit 拦截 |
| [存续-事实值与事件时间编辑](./存续-事实值与事件时间编辑/) | 存续 **Event Schedule** 事实值 + 事件时间可编辑（8 类产品矩阵） |
| [询价-LastLook同步最优价](./询价-LastLook同步最优价/) | 询价 **Last Look** 同步最优价（机构/Issuer 双端配置、申请状态机） |

## 版本范围

**分享**
- 产品详情/拼单卡片展示 Order Type（Limit Price / Market Price）
- Web 分享、App 分享内容与详情一致

**询价下单**
- FCN Trade Order Details：Quotation ID 旁信息图标、Best Price 摘要浮层
- 权限：AQDQVAN（credit charge）、AQDQ（user uf）；ID 文本跳转询价页回归

**ELN 询价**
- Add New Quotation · ELN Tab：除 UF 外条款相同则拦截 Submit（中英提示）

**存续**
- Event Schedule：触发事件结束后可改事实值（产品×事件矩阵）与事件时间

**询价 Last Look**
- Organization / Issuer Last Look Setting；Manual/Automatic 发起；邮件/自动/手工确认；同步回复申请状态机

详见各子目录内 `*-测试用例.md` 与 `.xmind`
