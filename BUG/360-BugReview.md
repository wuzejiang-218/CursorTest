# 360 迭代 Bug Review（前端）

> **已同步至：** [Tapon-v3.60-BUG复盘总结.md §3.2.1](Tapon-v3.60-BUG复盘总结.md#321-前端专项复盘360-迭代-bug-review) · 问题域 5 · 改进项 **S7/M7**

## 总览

| 负责人 | Bug 总数 | 文档中已说明原因 | 未说明/未归类 |
| ------ | ------ | ------------- | ------------- |
| 聂颖 | 6 | 2 | **4** |
| 罗嘉胜 | 14 | 6 | **8** |
| 黄浩 | 12 | 3 | **9** |
| 林桃君 | 16 | 8 | **8** |
| **合计** | **48** | **约 19 条有原因** | **约 29 条缺说明** |

**复盘结论（摘要）：** 约 **60%** 缺陷关闭时无书面根因；已归类项以 **需求不明、产品文档缺失、设计稿滞后、UI 交互未定义** 为主——详见主文档 **§3.2.1**。

---

### 聂颖

总共：6 个

**外部原因**

- [#8082](http://zentao.easyviewsz.com:81/zentao/bug-view-8082.html)
- [#7994](http://zentao.easyviewsz.com:81/zentao/bug-view-7994.html)

*（另有 4 条未在本文档写明原因，需在禅道补全分类。）*

---

### 罗嘉胜

总共：14 个

**外部原因**

- [#8013](http://zentao.easyviewsz.com:81/zentao/bug-view-8013.html)（需求不明确）
- [#8000](http://zentao.easyviewsz.com:81/zentao/bug-view-8000.html)（需求不明确）
- [#7998](http://zentao.easyviewsz.com:81/zentao/bug-view-7998.html)（需求不明确）
- [#7992](http://zentao.easyviewsz.com:81/zentao/bug-view-7992.html)（没有提测）

**历史原因**

- [#8086](http://zentao.easyviewsz.com:81/zentao/bug-view-8086.html)
- [#8071](http://zentao.easyviewsz.com:81/zentao/bug-view-8071.html)

---

### 黄浩

总共：12 个

**外部原因**

- [#8119](http://zentao.easyviewsz.com:81/zentao/bug-view-8119.html)（UI 交互没有）
- [#8100](http://zentao.easyviewsz.com:81/zentao/bug-view-8100.html)（UI 交互没有）
- [#8111](http://zentao.easyviewsz.com:81/zentao/bug-view-8111.html)（设计如此）

---

### 林桃君

总共：16 个

- **1 个** 样式 bug：[#8035](http://zentao.easyviewsz.com:81/zentao/bug-view-8035.html)
- **7 个** 外部原因、产品 bug、UI bug、设计如此：
  - [#8081](http://zentao.easyviewsz.com:81/zentao/bug-view-8081.html)（产品文档没写）
  - [#8033](http://zentao.easyviewsz.com:81/zentao/bug-view-8033.html)（产品文档没写，且产品文档上截图的设计稿也是全量的产品）
  - [#8040](http://zentao.easyviewsz.com:81/zentao/bug-view-8040.html)（产品演示 html 上如此，后续补的 UI）
  - [#8061](http://zentao.easyviewsz.com:81/zentao/bug-view-8061.html)（后续才出设计稿）
  - [#8062](http://zentao.easyviewsz.com:81/zentao/bug-view-8062.html)（后续才出设计稿）
  - [#8019](http://zentao.easyviewsz.com:81/zentao/bug-view-8019.html)（设计稿无如此详细）
  - [#8041](http://zentao.easyviewsz.com:81/zentao/bug-view-8041.html)（设计如此）

*（另有 8 条未在本文档写明原因，需在禅道补全分类。）*

---

## 根因分类速查（已登记项）

| 类型 | 编号 |
|------|------|
| 需求/产品文档不明 | #8013、#8000、#7998、#8081、#8033 |
| 设计稿滞后/缺失 | #8061、#8062、#8019、#8040、#8119、#8100 |
| 设计如此 | #8111、#8041 |
| 未提测 | #7992 |
| 历史遗留 | #8086、#8071 |
| 样式 | #8035 |
