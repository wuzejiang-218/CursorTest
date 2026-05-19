#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复「文件头前有垃圾字节」的 PDF：标准 PDF 必须以 %PDF- 开头。
部分下载/接口会在最前面附加若干字节（如 176BF\\r\\n 共 7 字节），导致严格校验失败。

用法:
  python fix_pdf.py <损坏的.pdf> [输出路径]
  未指定输出路径时，在同目录生成 fixed_<原文件名>.pdf

示例:
  python fix_pdf.py report.pdf
  python fix_pdf.py report.pdf report_ok.pdf
"""
import sys
from pathlib import Path
from typing import Optional

PDF_MAGIC = b"%PDF-"


def repair_pdf(src: Path, dst: Optional[Path] = None) -> Path:
    data = src.read_bytes()
    idx = data.find(PDF_MAGIC)
    if idx < 0:
        raise ValueError("文件中未找到 %PDF- 标记，可能不是 PDF 或损坏严重")

    if idx == 0:
        fixed = data
        note = "文件已以 %PDF- 开头，无需截断；将原样复制到输出。"
    else:
        junk = data[:idx]
        fixed = data[idx:]
        note = f"已去除文件头 {idx} 字节垃圾数据（前 32 字节 hex 预览）: {junk[:32].hex()}"

    if dst is None:
        dst = src.parent / f"fixed_{src.name}"

    dst.write_bytes(fixed)
    print(note)
    print(f"已写入: {dst.resolve()} ({len(fixed)} bytes)")
    return dst


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__.strip())
        return 2

    src = Path(sys.argv[1]).resolve()
    if not src.is_file():
        print(f"错误: 找不到文件 {src}")
        return 1

    dst = Path(sys.argv[2]).resolve() if len(sys.argv) >= 3 else None

    try:
        repair_pdf(src, dst)
    except ValueError as e:
        print(f"错误: {e}")
        return 1
    except OSError as e:
        print(f"错误: {e}")
        return 1

    return 0


if __name__ == "__main__":
    # 注意: 必须是双下划线 __name__ 与 __main__
    raise SystemExit(main())
