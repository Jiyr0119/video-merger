import os
import subprocess
from typing import List, Tuple, Optional
from vosk import Model, KaldiRecognizer, SetLogLevel
import wave
import json

class SubtitleGenerator:
    def __init__(self, model_path="vosk-model-cn-0.22", input_dir=".", output_dir="."):
        """初始化字幕生成器
        
        Args:
            model_path (str): Vosk语音识别模型路径
            input_dir (str): 输入视频文件夹路径
            output_dir (str): 输出字幕文件的文件夹路径
        """
        self.model_path = os.path.join(os.path.dirname(__file__), model_path)
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        SetLogLevel(-1)  # 禁用Vosk的日志输出
        
    def extract_audio(self, video_path: str, audio_path: str) -> bool:
        """从视频中提取音频
        
        Args:
            video_path (str): 视频文件路径
            audio_path (str): 输出音频文件路径
            
        Returns:
            bool: 提取是否成功
        """
        try:
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-vn',  # 不处理视频
                '-acodec', 'pcm_s16le',  # 音频编码为PCM
                '-ar', '16000',  # 采样率16kHz
                '-ac', '1',  # 单声道
                '-y',  # 覆盖已存在的文件
                audio_path
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"音频提取失败：{str(e)}")
            return False
            
    def generate_subtitle(self, video_path: str, output_format: str = 'srt') -> Optional[str]:
        """生成字幕文件
        
        Args:
            video_path (str): 视频文件路径
            output_format (str): 输出字幕格式，支持'srt'或'txt'
            
        Returns:
            Optional[str]: 生成的字幕文件路径，失败则返回None
        """
        # 准备临时音频文件
        temp_audio = os.path.join(self.output_dir, 'temp_audio.wav')
        if not self.extract_audio(video_path, temp_audio):
            return None
            
        try:
            # 加载语音识别模型
            if not os.path.exists(self.model_path):
                print(f"错误：找不到语音识别模型，请确保{self.model_path}目录存在")
                return None
                
            model = Model(self.model_path)
            wf = wave.open(temp_audio, "rb")
            rec = KaldiRecognizer(model, wf.getframerate())
            rec.SetWords(True)  # 启用词级别时间戳
            
            # 准备字幕文件
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            subtitle_path = os.path.join(self.output_dir, f"{base_name}.{output_format}")
            
            # 处理音频并生成字幕
            results = []
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    if result.get('result'):
                        results.extend(result['result'])
            
            # 处理最后的识别结果
            final_result = json.loads(rec.FinalResult())
            if final_result.get('result'):
                results.extend(final_result['result'])
            
            # 生成字幕文件
            with open(subtitle_path, 'w', encoding='utf-8') as f:
                if output_format == 'srt':
                    self._write_srt(f, results)
                else:
                    self._write_txt(f, results)
            
            return subtitle_path
            
        except Exception as e:
            print(f"字幕生成失败：{str(e)}")
            return None
            
        finally:
            # 清理临时文件
            if os.path.exists(temp_audio):
                os.remove(temp_audio)
                
    def _write_srt(self, file, results: List[dict]):
        """写入SRT格式字幕
        
        Args:
            file: 文件对象
            results (List[dict]): 识别结果列表
        """
        for i, group in enumerate(self._group_words(results), 1):
            start_time = self._format_time(group[0]['start'])
            end_time = self._format_time(group[-1]['end'])
            text = ' '.join(word['word'] for word in group)
            
            file.write(f"{i}\n")
            file.write(f"{start_time} --> {end_time}\n")
            file.write(f"{text}\n\n")
            
    def _write_txt(self, file, results: List[dict]):
        """写入纯文本格式字幕
        
        Args:
            file: 文件对象
            results (List[dict]): 识别结果列表
        """
        for group in self._group_words(results):
            text = ' '.join(word['word'] for word in group)
            file.write(f"{text}\n")
            
    def _group_words(self, words: List[dict], max_chars: int = 40) -> List[List[dict]]:
        """将词组合成字幕行
        
        Args:
            words (List[dict]): 词列表
            max_chars (int): 每行最大字符数
            
        Returns:
            List[List[dict]]: 分组后的词列表
        """
        groups = []
        current_group = []
        current_length = 0
        
        for word in words:
            word_len = len(word['word'])
            if current_length + word_len > max_chars and current_group:
                groups.append(current_group)
                current_group = []
                current_length = 0
            current_group.append(word)
            current_length += word_len
            
        if current_group:
            groups.append(current_group)
            
        return groups
        
    def _format_time(self, seconds: float) -> str:
        """格式化时间为SRT格式
        
        Args:
            seconds (float): 秒数
            
        Returns:
            str: 格式化的时间字符串 (HH:MM:SS,mmm)
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{int((seconds % 1) * 1000):03d}"