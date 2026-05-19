"""
用法:
  python corrupt_pdf.py <正常PDF文件> <输出损坏PDF文件> [垃圾数据字符串]

未指定垃圾数据字符串时，默认使用 "17740\r\n"。

示例:
  python corrupt_pdf.py normal.pdf corrupted.pdf
  python corrupt_pdf.py report.pdf broken_report.pdf "BAD_HEADER\n"
  python corrupt_pdf.py doc.pdf broken_doc.pdf "HTTP/1.1 200 OK\r\nContent-Type: application/pdf\r\n\r\n"
"""
import sys
import os

def corrupt_pdf(src_path: str, dst_path: str, junk_data_str: str):
    """
    将指定的垃圾数据添加到正常 PDF 文件的开头，生成一个“损坏”的 PDF。

    Args:
        src_path: 正常 PDF 文件的路径。
        dst_path: 输出损坏 PDF 文件的路径。
        junk_data_str: 要添加到文件开头的垃圾数据字符串。
                       例如: "17740\r\n" 或 "some_junk_bytes\n"
    """
    if not os.path.exists(src_path):
        print(f"❌ 错误：源文件 '{src_path}' 不存在。")
        return False

    try:
        with open(src_path, 'rb') as f_src:
            original_content = f_src.read()
    except Exception as e:
        print(f"❌ 错误：无法读取源文件 '{src_path}'，原因：{e}")
        return False

    # 将垃圾数据字符串编码为字节
    try:
        junk_bytes = junk_data_str.encode('utf-8')
    except UnicodeEncodeError:
        print(f"❌ 错误：垃圾数据字符串 '{junk_data_str}' 无法使用 UTF-8 编码。请尝试只包含 ASCII 字符。")
        return False

    # 将垃圾数据添加到原始 PDF 内容的开头
    corrupted_content = junk_bytes + original_content

    # 写入损坏后的文件
    try:
        with open(dst_path, 'wb') as f_dst:
            f_dst.write(corrupted_content)
        print(f"✅ 成功：已将 {len(junk_bytes)} 字节垃圾数据添加到 '{src_path}' 的开头。")
        print(f"✅ 已生成损坏的 PDF 文件：'{dst_path}' ({len(corrupted_content)} bytes)")
        return True
    except Exception as e:
        print(f"❌ 错误：无法写入目标文件 '{dst_path}'，原因：{e}")
        return False


if __name__ == "__main__":
    default_junk = "17740\r\n"

    if len(sys.argv) < 3:
        print(__doc__.strip()) # 现在__doc__会指向模块的文档字符串
        sys.exit(1)

    src = sys.argv[1]
    dst = sys.argv[2]
    junk_data = sys.argv[3] if len(sys.argv) >= 4 else default_junk

    if corrupt_pdf(src, dst, junk_data):
        sys.exit(0)
    else:
        sys.exit(1)