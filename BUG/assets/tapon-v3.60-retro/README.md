# Tapon v3.60 复盘图资源

## 中文显示修复

PNG 须用本机 **Chrome + 微软雅黑** 渲染。勿使用 Kroki 等无 CJK 字体的在线服务，否则中文会显示为 `???`。

## 重新生成 PNG

```powershell
cd d:\cursor\BUG\assets\tapon-v3.60-retro
node render-charts.mjs
```

或：

```powershell
cd d:\cursor\Tapon-v3.60-retro
node render-charts.mjs
```

（仓库根目录 `Tapon-v3.60-retro/render-charts.mjs` 运行后会自动同步 PNG 到本目录。）

## 文件说明

| 文件 | 说明 |
|------|------|
| `*.mmd` | Mermaid 源文件（可编辑） |
| `*.png` | 评审用导出图 |
| `../../../Tapon-v3.60-retro/render-charts.mjs` | 渲染脚本（仓库根目录） |
