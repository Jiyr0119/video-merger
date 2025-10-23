# myproject package - 视频合并工具

from .video_merger import VideoMerger
from .subtitle_generator import SubtitleGenerator
# 移除了对不存在的 DocxFormatter 的导入
# 可以考虑导出 docx_formatter 模块中的特定函数，如 process_docx 和 batch_process

__version__ = '0.1.0'
