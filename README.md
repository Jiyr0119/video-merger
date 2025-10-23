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
- **DOCX文档格式化**：批量处理DOCX文档，规范化标题格式

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

### DOCX文档格式化

```python
from myproject.docx_formatter import DocxFormatter

# 初始化DOCX格式化器
formatter = DocxFormatter()

# 格式化单个DOCX文档
result = formatter.format_document("/path/to/document.docx")
print(f"处理完成: {result}")

# 批量格式化目录中的所有DOCX文件
results = formatter.batch_format_documents("/path/to/docx/files", recursive=True)
for result in results:
    print(f"文件: {result['file']}, 处理段落数: {result.get('paragraphs_processed', 0)}")
```

### 使用Word默认样式

```python
# 使用Word默认样式（标题1, 标题2, 正文等）
formatter = DocxFormatter(use_default_styles=True)
result = formatter.format_document("input.docx", "output.docx")
```

### 无命令行参数版本

对于不想使用命令行参数的用户，项目提供了直接在代码中配置参数的方式：

```python
# 直接运行配置脚本
python format_docs.py

# 或者运行示例配置
python examples/docx_formatting_config.py
```

在代码中直接配置参数：

```python
from myproject.docx_formatter import DocxFormatter

# 配置参数
input_path = "path/to/your/document.docx"  # 输入文件或目录
output_path = "path/to/output/document.docx"  # 输出文件或目录
title_font = "黑体"  # 标题字体（可选）
body_font = "宋体"  # 正文字体（可选）
use_default_styles = True  # 使用Word默认样式（可选）
recursive = False  # 是否递归处理子目录

# 创建格式化器并处理
formatter = DocxFormatter(
    title_font=title_font, 
    body_font=body_font,
    use_default_styles=use_default_styles
)
result = formatter.format_document(input_path, output_path)
```

### 命令行使用DOCX格式化

```bash
# 格式化单个文件
python -m myproject.docx_formatter /path/to/document.docx

# 批量格式化目录中的文件
python -m myproject.docx_formatter /path/to/docx/files

# 使用Word默认样式
python -m myproject.docx_formatter /path/to/document.docx -ds

# 递归处理子目录
python -m myproject.docx_formatter /path/to/docx/files -r
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

## DOCX格式化功能说明

DOCX格式化工具可以帮助您:

1. 自动移除标题前的无关字符（如"xx标题1" → "标题1"）
2. 标准化章节标题格式（如"第1章"、"第二节"、"附录A"等）
3. 批量处理多个DOCX文档
4. 处理文档中的段落和表格内容
5. 设置标题和正文字体
6. 应用Word默认样式（标题1, 标题2, 正文等）
7. 生成新文档而不是覆盖原文档

支持的标题格式包括:
- 数字章节：第1章、第2节、第3部分
- 中文数字章节：第一章、第二部分、第三节
- 附录格式：附录A、附录一
- 简单章节：1章、2节、3部分

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
│       ├── subtitle_generator.py  # 字幕生成功能
│       └── docx_formatter.py  # DOCX文档格式化功能
├── tests/                     # 测试文件
├── examples/                  # 使用示例
│   ├── basic_usage.py
│   ├── advanced_usage.py
│   └── docx_formatting_example.py  # DOCX格式化使用示例
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

### Q: DOCX格式化工具提示缺少依赖怎么办？
A: 安装DOCX处理依赖：`pip install python-docx`

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
- [python-docx](https://python-docx.readthedocs.io/) - DOCX文档处理库
- 所有贡献者和用户
