#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOCX格式化器测试
"""

import unittest
from pathlib import Path
import sys

# 添加项目源码路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# 尝试导入DOCX格式化器
try:
    from myproject.docx_formatter import DocxFormatter
    DOCX_AVAILABLE = True
except RuntimeError:
    DOCX_AVAILABLE = False


class TestDocxFormatter(unittest.TestCase):

    def setUp(self):
        """测试前准备"""
        if not DOCX_AVAILABLE:
            self.skipTest("python-docx库未安装，跳过测试")

    def test_format_title(self):
        """测试标题格式化功能"""
        # 确保DOCX支持可用
        if not DOCX_AVAILABLE:
            self.skipTest("python-docx库未安装，跳过测试")

        formatter = DocxFormatter()

        # 测试用例
        test_cases = [
            ("xx标题1", "标题1"),
            ("yy第1章", "第1章"),
            ("zz第二节", "第二节"),
            ("aa附录A", "附录A"),
            ("正常标题", "正常标题"),
            ("第1部分", "第1部分"),
        ]

        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = formatter.format_title(input_text)
                self.assertEqual(result, expected)

    def test_format_title_chinese_numerals(self):
        """测试中文数字标题格式化"""
        # 确保DOCX支持可用
        if not DOCX_AVAILABLE:
            self.skipTest("python-docx库未安装，跳过测试")

        formatter = DocxFormatter()

        # 测试中文数字标题
        test_cases = [
            ("xx第一章", "第一章"),
            ("yy第二部分", "第二部分"),
            ("zz第三节", "第三节"),
            ("aa附录一", "附录一"),
        ]

        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = formatter.format_title(input_text)
                self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
