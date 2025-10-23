#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOCX文档格式化工具配置示例
展示如何使用不同的配置来格式化DOCX文档
"""

import sys
from pathlib import Path

# 添加项目源码路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from myproject.docx_formatter import DocxFormatter

def format_single_document():
    """格式化单个文档示例"""
    print("=== 格式化单个文档示例 ===")

    # 配置参数
    input_file = "sample_docs/test_document.docx"
    output_file = "sample_docs/single_formatted.docx"
    title_font = "华文黑体"
    body_font = "华文楷体"

    try:
        formatter = DocxFormatter(title_font=title_font, body_font=body_font)
        result = formatter.format_document(input_file, output_file)

        print(f"输入文件: {result['input_file']}")
        print(f"输出文件: {result['output_file']}")
        print(f"处理段落数: {result['paragraphs_processed']}")
        print(f"处理表格数: {result['tables_processed']}")
        print("单个文档格式化完成！\n")

    except Exception as e:
        print(f"处理单个文档时出错: {e}")

def format_batch_documents():
    """批量格式化文档示例"""
    print("=== 批量格式化文档示例 ===")

    # 配置参数
    input_dir = "sample_docs/batch_input"
    output_dir = "sample_docs/batch_output"
    title_font = "微软雅黑"
    body_font = "宋体"
    recursive = True  # 递归处理子目录

    try:
        formatter = DocxFormatter(title_font=title_font, body_font=body_font)
        results = formatter.batch_format_documents(input_dir, output_dir, recursive)

        print(f"批量处理完成，共处理 {len(results)} 个文件:")
        for result in results:
            if 'error' in result:
                print(f"  失败: {result['input_file']} - {result['error']}")
            else:
                print(f"  成功: {result['input_file']} -> {result['output_file']}")

        print("批量文档格式化完成！\n")

    except Exception as e:
        print(f"批量处理文档时出错: {e}")

def format_document_with_default_fonts():
    """使用默认字体格式化文档示例"""
    print("=== 使用默认字体格式化文档示例 ===")

    # 配置参数（不指定字体，使用默认值）
    input_file = "sample_docs/test_document.docx"
    output_file = "sample_docs/default_fonts_formatted.docx"

    try:
        # 不指定字体参数，使用默认字体
        formatter = DocxFormatter()
        result = formatter.format_document(input_file, output_file)

        print(f"输入文件: {result['input_file']}")
        print(f"输出文件: {result['output_file']}")
        print(f"处理段落数: {result['paragraphs_processed']}")
        print("使用默认字体格式化完成！\n")

    except Exception as e:
        print(f"使用默认字体处理时出错: {e}")

def format_document_title_only():
    """仅格式化标题示例"""
    print("=== 仅格式化标题示例 ===")

    # 配置参数（只设置标题字体，不设置正文字体）
    input_file = "sample_docs/test_document.docx"
    output_file = "sample_docs/title_only_formatted.docx"
    title_font = "隶书"
    # body_font 不设置，保持原文档字体

    try:
        formatter = DocxFormatter(title_font=title_font)
        result = formatter.format_document(input_file, output_file)

        print(f"输入文件: {result['input_file']}")
        print(f"输出文件: {result['output_file']}")
        print(f"处理段落数: {result['paragraphs_processed']}")
        print("仅标题格式化完成！\n")

    except Exception as e:
        print(f"仅标题处理时出错: {e}")

def main():
    """主函数"""
    print("DOCX文档格式化工具配置示例")
    print("=" * 40)

    # 运行所有示例
    format_single_document()
    format_batch_documents()
    format_document_with_default_fonts()
    format_document_title_only()

    print("所有示例运行完成！")

if __name__ == "__main__":
    main()
