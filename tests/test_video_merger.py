#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
视频合并工具测试
"""

import os
import sys
import unittest
from unittest import mock

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from myproject.video_merger import VideoMerger


class TestVideoMerger(unittest.TestCase):
    """视频合并工具测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.input_dir = os.path.join(os.path.dirname(__file__), 'test_data', 'input')
        self.output_dir = os.path.join(os.path.dirname(__file__), 'test_data', 'output')
        
        # 确保测试目录存在
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 创建测试实例
        self.merger = VideoMerger(
            input_dir=self.input_dir,
            output_dir=self.output_dir
        )
    
    def tearDown(self):
        """测试后清理"""
        # 这里可以添加清理测试文件的代码
        pass
    
    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(self.merger.input_dir, self.input_dir)
        self.assertEqual(self.merger.output_dir, self.output_dir)
    
    @mock.patch('myproject.video_merger.VideoMerger._merge_video_group')
    def test_merge_videos_calls_merge_video_group(self, mock_merge):
        """测试merge_videos方法调用_merge_video_group"""
        # 设置模拟返回值
        mock_merge.return_value = True
        
        # 模拟视频文件
        with mock.patch('os.listdir') as mock_listdir:
            mock_listdir.return_value = ['video1.mp4', 'video2.mp4']
            
            # 调用被测试方法
            result = self.merger.merge_videos('test_output')
            
            # 验证结果
            self.assertTrue(result)
            mock_merge.assert_called_once()
    
    def test_get_video_codec(self):
        """测试获取视频编码格式"""
        # 使用mock模拟ffmpeg命令输出
        with mock.patch('subprocess.run') as mock_run:
            # 设置模拟返回值
            mock_process = mock.MagicMock()
            mock_process.stdout = b'Stream #0:0(und): Video: h264 (High) (avc1 / 0x31637661)'
            mock_run.return_value = mock_process
            
            # 调用被测试方法
            codec = self.merger._get_video_codec('dummy.mp4')
            
            # 验证结果
            self.assertEqual(codec, 'h264')
    
    def test_check_codecs_compatibility(self):
        """测试编码兼容性检查"""
        # 测试相同编码
        self.assertTrue(self.merger._check_codecs_compatibility(['h264', 'h264', 'h264']))
        
        # 测试不同编码
        self.assertFalse(self.merger._check_codecs_compatibility(['h264', 'hevc', 'h264']))


if __name__ == '__main__':
    unittest.main()