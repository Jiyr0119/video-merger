#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOCX文档格式化工具 - 使用Word默认样式
将文档格式化为使用Word默认样式（标题1, 标题2, 正文等）
"""

import sys
from pathlib import Path

# 添加项目源码路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from myproject.docx_formatter import DocxFormatter

def main():
    """主函数 - 使用Word默认样式格式化文档"""

    # 配置参数
    input_file = "sample_docs/test_document.docx"
    output_file = "sample_docs/default_styles_output.docx"

    # 使用Word默认样式
    formatter = DocxFormatter(use_default_styles=True)

    try:
        # 处理文档（使用Word默认样式）
        result = formatter.format_document(input_file, output_file)

        print("处理完成:")
        print(f"  输入文件: {result['input_file']}")
        print(f"  输出文件: {result['output_file']}")
        print(f"  格式化的段落数: {result['paragraphs_processed']}")
        print(f"  格式化的表格单元格数: {result['tables_processed']}")
        print("\n此操作将:")
        print("1. 格式化标题文本（如将'xx标题1'改为'标题1'）")
        print("2. 应用Word默认样式（标题1, 标题2, 正文等）")
        print("3. 保持Word默认字体设置")

    except Exception as e:
        print(f"处理过程中发生错误: {e}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
