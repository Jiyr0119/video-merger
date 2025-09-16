#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
基本使用示例

这个脚本展示了视频合并工具的基本用法。
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from myproject.video_merger import VideoMerger


def main():
    # 设置输入和输出目录
    input_dir = os.path.join(os.path.dirname(__file__), '..', 'input')
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    
    # 确保目录存在
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"输入目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    
    # 检查输入目录中的视频文件
    video_files = [f for f in os.listdir(input_dir) 
                  if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    
    if not video_files:
        print(f"警告: 在 {input_dir} 中没有找到视频文件")
        print("请将要合并的视频文件放入输入目录，然后重新运行此脚本")
        return
    
    print(f"找到 {len(video_files)} 个视频文件: {', '.join(video_files)}")
    
    # 初始化视频合并器
    merger = VideoMerger(
        input_dir=input_dir,
        output_dir=output_dir
    )
    
    # 合并视频
    output_filename = "merged_video"
    print(f"\n开始合并视频到: {output_filename}.mp4")
    
    # 使用默认设置合并
    merger.merge_videos(output_filename)
    
    print(f"\n合并完成! 输出文件保存在: {os.path.join(output_dir, output_filename + '.mp4')}")


if __name__ == "__main__":
    main()