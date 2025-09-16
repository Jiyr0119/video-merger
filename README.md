# 视频合并工具 (Video Merger)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

这是一个基于FFmpeg的视频合并工具，用于将多个视频文件智能合并为一个，并可选择性地生成字幕。工具会自动检测视频编码格式，选择最佳合并策略，提高合并效率和视频质量。

## 功能特性

- **智能编码选择**：自动检测视频编码格式，选择最佳合并策略
- **自然排序**：确保视频按照自然顺序合并（例如：video1.mp4, video2.mp4, video10.mp4）
- **自动分割**：当视频总时长过长时，自动分割为多个文件
- **字幕生成**：可选择性地为合并后的视频生成字幕
- **进度显示**：实时显示合并进度
- **编码预设**：支持多种编码预设，平衡速度和质量

## 系统要求

- Python 3.6+
- FFmpeg（需要预先安装）

## 安装

### 1. 克隆仓库

```bash
git clone https://github.com/YOUR_USERNAME/video-merger.git
cd video-merger
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
pip install -e .
```

### 3. 安装FFmpeg

#### macOS
```bash
brew install ffmpeg
```

#### Ubuntu/Debian
```bash
apt-get install ffmpeg
```

#### Windows
下载[FFmpeg](https://ffmpeg.org/download.html)并添加到系统PATH。

## 使用方法

### 基本用法

```python
from myproject.video_merger import VideoMerger

# 初始化视频合并器
merger = VideoMerger(
    input_dir="/path/to/videos",  # 输入视频所在文件夹
    output_dir="/path/to/output"  # 输出文件夹
)

# 合并视频（自动检测编码兼容性）
merger.merge_videos("合并后的视频名称")
```

### 高级用法

```python
# 使用不同的编码预设
merger.merge_videos(
    "高质量视频", 
    force_encode=True,  # 强制重编码
    encode_preset="slow",  # 较慢但质量更高
    generate_subtitles=True  # 生成字幕
)

# 快速合并（质量较低）
merger.merge_videos(
    "快速合并", 
    encode_preset="ultrafast",  # 最快的编码速度
    auto_split=False  # 不自动分割
)
```

## 编码预设选项

工具支持以下FFmpeg编码预设：

| 预设 | 速度 | 质量 | 推荐用途 |
|------|------|------|----------|
| ultrafast | 最快 | 最低 | 测试或临时预览 |
| superfast | 非常快 | 较低 | 快速预览 |
| veryfast | 很快 | 较低 | 一般预览 |
| faster | 较快 | 适中 | 默认选项 |
| fast | 快 | 较好 | 一般使用 |
| medium | 中等 | 平衡 | 平衡速度和质量 |
| slow | 慢 | 好 | 高质量需求 |
| slower | 较慢 | 很好 | 更高质量需求 |
| veryslow | 非常慢 | 最高 | 最终成品 |

## 项目结构

```
.
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── video_merger.py    # 视频合并核心功能
│       └── subtitle_generator.py  # 字幕生成功能
├── tests/                     # 测试文件
├── input/                     # 输入视频目录
├── output/                    # 输出视频目录
├── requirements.txt           # 项目依赖
└── setup.py                   # 安装配置
```

## 常见问题

### Q: 合并视频时出现编码错误怎么办？
A: 尝试使用`force_encode=True`参数强制重新编码所有视频。

### Q: 合并速度很慢怎么办？
A: 如果视频编码格式兼容，设置`force_encode=False`可以显著提高速度。也可以尝试使用更快的编码预设，如`encode_preset='superfast'`。

### Q: 如何提高输出视频质量？
A: 使用更高质量的编码预设，如`encode_preset='slow'`或`'veryslow'`。

## 贡献指南

欢迎贡献代码、报告问题或提出改进建议！请遵循以下步骤：

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 致谢

- [FFmpeg](https://ffmpeg.org/) - 强大的视频处理工具
- [Vosk](https://alphacephei.com/vosk/) - 离线语音识别工具
- 所有贡献者和用户