#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
高级使用示例

这个脚本展示了视频合并工具的高级用法，包括不同的编码预设、字幕生成等功能。
"""

import os
import sys
import argparse

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from myproject.video_merger import VideoMerger


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="视频合并工具高级示例")
    
    parser.add_argument(
        "--input-dir", 
        default=os.path.join(os.path.dirname(__file__), '..', 'input'),
        help="输入视频目录路径"
    )
    
    parser.add_argument(
        "--output-dir", 
        default=os.path.join(os.path.dirname(__file__), '..', 'output'),
        help="输出视频目录路径"
    )
    
    parser.add_argument(
        "--output-name", 
        default="merged_video",
        help="输出视频文件名（不含扩展名）"
    )
    
    parser.add_argument(
        "--preset", 
        choices=[
            "ultrafast", "superfast", "veryfast", "faster", 
            "fast", "medium", "slow", "slower", "veryslow"
        ],
        default="faster",
        help="编码预设，平衡速度和质量"
    )
    
    parser.add_argument(
        "--force-encode", 
        action="store_true",
        help="强制重新编码所有视频"
    )
    
    parser.add_argument(
        "--generate-subtitles", 
        action="store_true",
        help="为合并后的视频生成字幕"
    )
    
    parser.add_argument(
        "--no-auto-split", 
        action="store_true",
        help="禁用自动分割长视频"
    )
    
    return parser.parse_args()


def main():
    # 解析命令行参数
    args = parse_args()
    
    # 确保目录存在
    os.makedirs(args.input_dir, exist_ok=True)
    os.makedirs(args.output_dir, exist_ok=True)
    
    print(f"输入目录: {args.input_dir}")
    print(f"输出目录: {args.output_dir}")
    print(f"编码预设: {args.preset}")
    print(f"强制重编码: {'是' if args.force_encode else '否'}")
    print(f"生成字幕: {'是' if args.generate_subtitles else '否'}")
    print(f"自动分割: {'否' if args.no_auto_split else '是'}")
    
    # 检查输入目录中的视频文件
    video_files = [f for f in os.listdir(args.input_dir) 
                  if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    
    if not video_files:
        print(f"警告: 在 {args.input_dir} 中没有找到视频文件")
        print("请将要合并的视频文件放入输入目录，然后重新运行此脚本")
        return
    
    print(f"找到 {len(video_files)} 个视频文件: {', '.join(video_files)}")
    
    # 初始化视频合并器
    merger = VideoMerger(
        input_dir=args.input_dir,
        output_dir=args.output_dir
    )
    
    # 合并视频
    print(f"\n开始合并视频到: {args.output_name}.mp4")
    
    # 使用高级设置合并
    merger.merge_videos(
        args.output_name,
        force_encode=args.force_encode,
        encode_preset=args.preset,
        generate_subtitles=args.generate_subtitles,
        auto_split=not args.no_auto_split
    )
    
    print(f"\n合并完成! 输出文件保存在: {os.path.join(args.output_dir, args.output_name + '.mp4')}")


if __name__ == "__main__":
    main()