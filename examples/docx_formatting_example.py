#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOCX文档格式化使用示例
演示如何使用docx_formatter模块批量处理DOCX文档
"""

import sys
from pathlib import Path

# 添加项目源码路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def example_basic_usage():
    """基本使用示例"""
    try:
        from myproject.docx_formatter import DocxFormatter

        # 创建格式化器实例
        formatter = DocxFormatter()

        # 格式化单个文档
        print("=== 单个文档格式化示例 ===")
        # 注意：这里需要一个实际存在的DOCX文件路径
        result = formatter.format_document("path/to/your/document.docx")
        # print(f"处理结果: {result}")
        print("请提供一个实际的DOCX文件路径来测试此功能")

    except RuntimeError as e:
        print(f"错误: {e}")
        print("请确保已安装 python-docx 库: pip install python-docx")


def example_batch_processing():
    """批量处理示例"""
    try:
        from myproject.docx_formatter import DocxFormatter

        # 创建格式化器实例
        formatter = DocxFormatter()

        # 批量处理目录中的所有DOCX文件
        print("\n=== 批量处理示例 ===")
        # 注意：这里需要一个实际存在的包含DOCX文件的目录路径
        # results = formatter.batch_format_documents("path/to/your/docx/files", recursive=True)
        #
        # print(f"批量处理完成，共处理 {len(results)} 个文件:")
        # for result in results:
        #     if 'error' in result:
        #         print(f"  失败: {result['file']} - {result['error']}")
        #     else:
        #         print(f"  成功: {result['file']}")
        #         print(f"    格式化的段落数: {result['paragraphs_processed']}")
        print("请提供一个实际包含DOCX文件的目录路径来测试此功能")

    except RuntimeError as e:
        print(f"错误: {e}")
        print("请确保已安装 python-docx 库: pip install python-docx")


def example_title_formatting():
    """标题格式化功能示例"""
    try:
        from myproject.docx_formatter import DocxFormatter

        # 创建格式化器实例
        formatter = DocxFormatter()

        print("\n=== 标题格式化功能示例 ===")

        # 测试各种标题格式
        test_titles = [
            "xx标题1",
            "yy第1章",
            "zz第二节",
            "aa附录A",
            "bb第三部分",
            "cc附录三",
            "正常标题无需修改"
        ]

        for title in test_titles:
            formatted = formatter.format_title(title)
            print(f"原始: {title:>15} -> 格式化后: {formatted}")

    except RuntimeError as e:
        print(f"错误: {e}")
        print("请确保已安装 python-docx 库: pip install python-docx")


if __name__ == "__main__":
    print("DOCX文档格式化工具使用示例")
    print("=" * 40)

    example_basic_usage()
    example_batch_processing()
    example_title_formatting()

    print("\n" + "=" * 40)
    print("要实际使用此工具，请:")
    print("1. 安装依赖: pip install python-docx")
    print("2. 准备要处理的DOCX文档")
    print("3. 运行: python -m myproject.docx_formatter path/to/documents")
