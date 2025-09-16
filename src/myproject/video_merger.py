import os
import re
import subprocess
from typing import List, Tuple
from myproject.subtitle_generator import SubtitleGenerator

class VideoMerger:
    def __init__(self, input_dir=".", output_dir="."):
        """初始化视频合并器
        
        Args:
            input_dir (str): 输入视频文件夹路径
            output_dir (str): 输出合并视频的文件夹路径
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def natural_sort_key(self, s):
        """实现自然排序的键函数
        
        将字符串中的数字部分转换为整数，以实现自然排序
        例如：video1.mp4 < video2.mp4 < video10.mp4
        """
        return [int(text) if text.isdigit() else text.lower()
                for text in re.split('([0-9]+)', s)]
    
    def get_video_files(self, extensions=('.mp4', '.avi', '.mkv', '.mov')):
        """获取指定目录下的所有视频文件
        
        Args:
            extensions (tuple): 支持的视频文件扩展名
            
        Returns:
            list: 排序后的视频文件列表
        """
        video_files = [
            f for f in os.listdir(self.input_dir)
            if f.lower().endswith(extensions)
        ]
        # 使用自然排序算法对文件名进行排序
        return sorted(video_files, key=self.natural_sort_key)

    def get_video_duration(self, video_path: str) -> float:
        """获取视频时长

        Args:
            video_path (str): 视频文件路径

        Returns:
            float: 视频时长（秒）
        """
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]
        try:
            # 不使用check=True，以便我们可以自己处理错误
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"获取视频时长失败：ffprobe返回错误码 {result.returncode}")
                print(f"错误信息: {result.stderr.strip()}")
                # 检查文件是否存在
                if not os.path.exists(video_path):
                    print(f"文件不存在: {video_path}")
                elif os.path.getsize(video_path) == 0:
                    print(f"文件大小为0: {video_path}")
                return 0.0
            
            duration_str = result.stdout.strip()
            if not duration_str or duration_str == 'N/A':
                print(f"无法获取视频时长，ffprobe返回: {duration_str}")
                return 0.0
                
            return float(duration_str)
        except ValueError as e:
            print(f"解析视频时长失败：{str(e)}，ffprobe返回: {result.stdout.strip()}")
            return 0.0
        except Exception as e:
            print(f"获取视频时长时发生未知错误：{str(e)}")
            return 0.0

    def check_video_info(self, video_files: List[str]) -> List[Tuple[str, float]]:
        """检查所有视频文件的信息

        Args:
            video_files (List[str]): 视频文件列表

        Returns:
            List[Tuple[str, float]]: 包含视频文件路径和时长的列表
        """
        video_info = []
        total_duration = 0

        print("\n检查视频文件信息...")
        for video in video_files:
            full_path = os.path.join(self.input_dir, video)
            duration = self.get_video_duration(full_path)
            total_duration += duration
            video_info.append((full_path, duration))
            print(f"{video}: {duration/60:.2f}分钟")

        print(f"\n所有视频总时长: {total_duration/60:.2f}分钟")
        return video_info
    
    def create_merge_list(self, video_files, list_file='filelist.txt'):
        """创建用于FFmpeg的合并列表文件
        
        Args:
            video_files (list): 要合并的视频文件列表
            list_file (str): 生成的列表文件名
            
        Returns:
            str: 列表文件的路径
        """
        list_path = os.path.join(self.input_dir, list_file)
        with open(list_path, 'w', encoding='utf-8') as f:
            for video in video_files:
                # 使用完整路径，避免空格等特殊字符问题
                full_path = os.path.join(self.input_dir, video)
                f.write(f"file '{full_path}'\n")
        return list_path
    
    def get_video_codec(self, video_path: str) -> Tuple[str, str]:
        """获取视频的编码格式

        Args:
            video_path (str): 视频文件路径

        Returns:
            Tuple[str, str]: (视频编码格式, 音频编码格式)
        """
        # 检查文件是否存在和有效
        if not os.path.exists(video_path):
            print(f"文件不存在: {video_path}")
            return '', ''
        elif os.path.getsize(video_path) == 0:
            print(f"文件大小为0: {video_path}")
            return '', ''
        elif os.path.getsize(video_path) < 1024:  # 小于1KB的文件可能不是有效视频
            print(f"文件过小，可能不是有效视频: {video_path} ({os.path.getsize(video_path)} 字节)")
            return '', ''
            
        # 获取视频编码
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=codec_name',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"获取视频编码失败: {os.path.basename(video_path)}，错误码: {result.returncode}")
                print(f"错误信息: {result.stderr.strip()}")
                return '', ''
                
            video_codec = result.stdout.strip()
            if not video_codec or video_codec == 'N/A':
                print(f"无法获取视频编码: {os.path.basename(video_path)}，ffprobe返回: '{video_codec}'")
                return '', ''
            
            # 获取音频编码
            cmd[4] = 'a:0'
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"获取音频编码失败: {os.path.basename(video_path)}，错误码: {result.returncode}")
                print(f"错误信息: {result.stderr.strip()}")
                return video_codec, ''
                
            audio_codec = result.stdout.strip()
            if not audio_codec or audio_codec == 'N/A':
                print(f"无法获取音频编码或视频没有音轨: {os.path.basename(video_path)}")
                audio_codec = ''
            
            print(f"检测到编码: {os.path.basename(video_path)} - 视频: {video_codec}, 音频: {audio_codec or '无音轨'}")
            return video_codec, audio_codec
        except ValueError as e:
            print(f"解析编码信息时发生错误: {os.path.basename(video_path)}, {str(e)}")
            return '', ''
        except subprocess.SubprocessError as e:
            print(f"执行ffprobe命令失败: {os.path.basename(video_path)}, {str(e)}")
            return '', ''
        except Exception as e:
            print(f"获取编码信息时发生未知错误: {os.path.basename(video_path)}, {str(e)}")
            return '', ''

    def check_codecs_compatibility(self, video_files: List[str]) -> bool:
        """检查所有视频的编码格式是否兼容

        Args:
            video_files (List[str]): 视频文件列表

        Returns:
            bool: 如果所有视频编码格式相同返回True，否则返回False
        """
        if not video_files:
            print("没有视频文件，无法检查编码兼容性")
            return False
            
        print("\n检查视频编码兼容性...")
        print(f"共有 {len(video_files)} 个视频文件需要检查")
        
        first_video = os.path.join(self.input_dir, video_files[0])
        base_video_codec, base_audio_codec = self.get_video_codec(first_video)
        
        if not base_video_codec:
            print(f"无法获取基准视频的编码信息: {video_files[0]}")
            return False
            
        print(f"基准编码格式 - 视频: {base_video_codec}, 音频: {base_audio_codec or '无音轨'}")
        
        incompatible_videos = []
        for video in video_files[1:]:
            video_path = os.path.join(self.input_dir, video)
            video_codec, audio_codec = self.get_video_codec(video_path)
            
            if not video_codec:
                print(f"警告: 无法获取视频编码 {video}，将视为不兼容")
                incompatible_videos.append((video, '未知', '未知'))
                continue
                
            if video_codec != base_video_codec or audio_codec != base_audio_codec:
                incompatible_videos.append((video, video_codec, audio_codec))
        
        if incompatible_videos:
            print("\n检测到编码不兼容的视频:")
            for video, v_codec, a_codec in incompatible_videos:
                print(f"  - {video}: 视频编码={v_codec}, 音频编码={a_codec or '无音轨'}")
            print("\n由于编码不兼容，将使用重编码模式合并视频（速度较慢但兼容性更好）")
            return False
        
        print("\n所有视频编码格式兼容，将使用快速合并模式（直接拷贝，速度更快）")
        return True

    def split_videos_by_duration(self, video_info: List[Tuple[str, float]], target_duration: float) -> Tuple[List[str], List[str]]:
        """根据目标时长将视频文件分成两组

        Args:
            video_info (List[Tuple[str, float]]): 包含视频路径和时长的列表
            target_duration (float): 目标时长（秒）

        Returns:
            Tuple[List[str], List[str]]: 两组视频文件列表
        """
        first_group = []
        second_group = []
        first_duration = 0
        second_duration = 0

        # 按照时长动态分配视频到两个组
        for video_path, duration in video_info:
            video_name = os.path.basename(video_path)
            if first_duration <= second_duration:
                first_group.append(video_name)
                first_duration += duration
            else:
                second_group.append(video_name)
                second_duration += duration

        print(f"\n第一组视频总时长: {first_duration/60:.2f}分钟")
        print(f"第二组视频总时长: {second_duration/60:.2f}分钟")

        return first_group, second_group

    def generate_subtitle(self, video_path: str, output_format: str = 'srt') -> str:
        """为视频生成字幕
        
        Args:
            video_path (str): 视频文件路径
            output_format (str): 输出字幕格式，支持'srt'或'txt'
            
        Returns:
            str: 生成的字幕文件路径
        """
        generator = SubtitleGenerator(
            input_dir=self.input_dir,
            output_dir=self.output_dir
        )
        return generator.generate_subtitle(video_path, output_format)

    def merge_videos(self, output_name, video_files=None, force_encode=False, auto_split=True, generate_subtitles=False, encode_preset='faster'):
        """合并视频文件
        
        Args:
            output_name (str): 输出文件名（不包含扩展名）
            video_files (list, optional): 指定要合并的视频文件列表
            force_encode (bool): 是否强制重新编码以确保时间同步
            auto_split (bool): 当视频总时长超过120分钟时是否自动分割
            generate_subtitles (bool): 是否为合并后的视频生成字幕
            encode_preset (str): FFmpeg编码速度预设，可选值：
                                 ultrafast (最快，质量最低)
                                 superfast (非常快，质量较低)
                                 veryfast (很快，质量较低)
                                 faster (默认，较快且质量适中)
                                 fast
                                 medium (平衡速度和质量)
                                 slow
                                 slower
                                 veryslow (最慢，质量最高)
            
        Returns:
            bool: 合并是否成功
        """
        if video_files is None:
            video_files = self.get_video_files()
        
        if not video_files:
            print("没有找到可合并的视频文件")
            return False

        # 首先将所有视频合并成一个完整文件
        temp_output = f"{output_name}_temp"
        merge_success = self._merge_video_group(temp_output, video_files, force_encode, encode_preset)
        
        if not merge_success:
            print("视频合并失败，无法继续处理")
            return False
            
        # 获取合并后视频的完整路径
        temp_video_path = os.path.join(self.output_dir, f"{temp_output}.mp4")
        
        # 检查文件是否存在
        if not os.path.exists(temp_video_path):
            print(f"合并后的临时文件不存在: {temp_video_path}")
            return False
            
        # 检查合并后的视频时长
        total_duration = self.get_video_duration(temp_video_path)
        if total_duration <= 0:
            print("合并后的视频时长为0或无法获取，可能合并失败")
            if os.path.exists(temp_video_path):
                os.remove(temp_video_path)
            return False
        
        # 如果启用自动分割且时长超过120分钟，则将视频分割成两部分
        if auto_split and total_duration > 7200:  # 120分钟 = 7200秒
            print("\n合并后视频总时长超过120分钟，将生成完整版和两个分割版本...")
            
            # 首先将临时文件重命名为完整版
            full_output = os.path.join(self.output_dir, f"{output_name}_full.mp4")
            os.rename(temp_video_path, full_output)
            print(f"\n完整版已保存：{os.path.basename(full_output)} ({total_duration/60:.2f}分钟)")
            
            # 计算分割点（视频总时长的一半）
            split_point = total_duration / 2
            
            # 使用ffmpeg分割视频
            first_output = f"{output_name}_part1.mp4"
            second_output = f"{output_name}_part2.mp4"
            
            # 分割第一部分（从开始到中点）
            cmd1 = [
                'ffmpeg',
                '-i', full_output,
                '-t', str(split_point),
                '-c', 'copy',
                os.path.join(self.output_dir, first_output)
            ]
            
            # 分割第二部分（从中点到结束）
            cmd2 = [
                'ffmpeg',
                '-i', full_output,
                '-ss', str(split_point),
                '-c', 'copy',
                os.path.join(self.output_dir, second_output)
            ]
            
            print("\n正在生成第一部分视频...")
            subprocess.run(cmd1, check=True)
            
            print("\n正在生成第二部分视频...")
            subprocess.run(cmd2, check=True)
            
            print(f"\n视频处理完成！生成了以下文件：")
            print(f"完整版：{os.path.basename(full_output)} ({total_duration/60:.2f}分钟)")
            print(f"第一部分：{first_output} ({split_point/60:.2f}分钟)")
            print(f"第二部分：{second_output} ({(total_duration-split_point)/60:.2f}分钟)")

            # 为所有视频生成字幕
            if generate_subtitles:
                print("\n开始生成字幕文件...")
                # 为完整版生成字幕
                subtitle_path = self.generate_subtitle(full_output)
                if subtitle_path:
                    print(f"完整版字幕已生成：{os.path.basename(subtitle_path)}")

                # 为第一部分生成字幕
                first_output_path = os.path.join(self.output_dir, first_output)
                subtitle_path = self.generate_subtitle(first_output_path)
                if subtitle_path:
                    print(f"第一部分字幕已生成：{os.path.basename(subtitle_path)}")

                # 为第二部分生成字幕
                second_output_path = os.path.join(self.output_dir, second_output)
                subtitle_path = self.generate_subtitle(second_output_path)
                if subtitle_path:
                    print(f"第二部分字幕已生成：{os.path.basename(subtitle_path)}")
        else:
            # 如果不需要分割，直接重命名临时文件为最终文件名
            final_output = os.path.join(self.output_dir, f"{output_name}.mp4")
            os.rename(temp_video_path, final_output)
            print(f"\n视频合并完成！总时长：{total_duration/60:.2f}分钟")

            # 为合并后的视频生成字幕
            if generate_subtitles:
                print("\n开始生成字幕文件...")
                subtitle_path = self.generate_subtitle(final_output)
                if subtitle_path:
                    print(f"字幕已生成：{os.path.basename(subtitle_path)}")

    def _merge_video_group(self, output_name: str, video_files: List[str], force_encode: bool, encode_preset: str = 'faster'):
        """合并一组视频文件

        Args:
            output_name (str): 输出文件名（不包含扩展名）
            video_files (List[str]): 要合并的视频文件列表
            force_encode (bool): 是否强制重新编码
            encode_preset (str): FFmpeg编码速度预设，可选值：
                                 ultrafast (最快，质量最低)
                                 superfast (非常快，质量较低)
                                 veryfast (很快，质量较低)
                                 faster (较快，质量适中，默认)
                                 fast (快，质量较好)
                                 medium (中等，平衡速度和质量)
                                 slow (慢，质量好)
                                 slower (较慢，质量很好)
                                 veryslow (非常慢，质量最高)
        """
        print(f"找到 {len(video_files)} 个视频文件，准备合并...")
        for i, video in enumerate(video_files, 1):
            print(f"{i}. {video}")

        # 检查视频信息
        video_info = self.check_video_info(video_files)
        expected_duration = sum(duration for _, duration in video_info)

        # 创建合并列表文件
        list_file = self.create_merge_list(video_files)
        output_path = os.path.join(self.output_dir, f"{output_name}.mp4")

        # 检查编码格式兼容性
        codecs_compatible = self.check_codecs_compatibility(video_files)

        # 构建FFmpeg命令
        if force_encode or not codecs_compatible:
            # 使用重编码模式，确保时间同步
            cmd = [
                'ffmpeg',
                '-nostats',  # 添加此参数
                '-f', 'concat',
                '-safe', '0',
                '-i', list_file,
                '-c:v', 'libx264',  # 视频编码器
                '-c:a', 'aac',      # 音频编码器
                '-preset', encode_preset, # 编码速度预设
                '-crf', '23',        # 视频质量
                '-progress', '-', # 输出进度信息
                output_path
            ]
            print(f"使用编码预设: {encode_preset}")

            if not force_encode:
                print("\n检测到视频编码格式不一致，将使用重编码模式...")
        else:
            # 使用直接拷贝模式
            cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', list_file,
                '-c', 'copy',
                '-progress', '-', # 输出进度信息
                output_path
            ]
            print("\n检测到视频编码格式一致，将使用快速合并模式...")

        merge_success = False
        try:
            print("\n开始合并视频...")
            # 将stderr重定向到STDOUT统一处理
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # 合并错误输出到标准输出
                universal_newlines=True
            )

            # 优化输出读取逻辑
            while process.poll() is None:
                output = process.stdout.readline()
                if not output:
                    continue
                
                line = output.strip()
                if line.startswith('out_time_ms='):
                    time_value = line.split('=')[1]
                    if time_value != 'N/A':
                        try:
                            time = int(time_value) / 1000000
                            progress = (time / expected_duration) * 100 if expected_duration > 0 else 0
                            print(f"\r合并进度: {progress:.1f}% ({time/60:.1f}/{expected_duration/60:.1f}分钟)", end='')
                        except ValueError:
                            print(f"\r合并进度: 处理中...", end='')
                    else:
                        print(f"\r合并进度: 初始化中...", end='')
                elif line.startswith('speed='):
                    speed = line.split('=')[1].strip()
                    print(f" 速度: {speed}", end='')
                elif line and not line.startswith('frame='):
                    print(f"\n{line}")

            # 读取剩余输出
            remaining_output = process.stdout.read()
            for line in remaining_output.splitlines():
                print(line.strip())
                
            # 检查进程退出状态
            if process.returncode == 0:
                merge_success = True
                print("\n视频合并成功完成！")
            else:
                print(f"\n视频合并失败，FFmpeg返回错误码: {process.returncode}")

        except Exception as e:
            print(f"合并过程出错：{str(e)}")
        finally:
            # 清理临时文件
            if os.path.exists(list_file):
                os.remove(list_file)
                
            # 检查输出文件是否存在且大小不为0
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0 and merge_success:
                print(f"已生成合并视频: {os.path.basename(output_path)}")
                return True
            elif os.path.exists(output_path) and os.path.getsize(output_path) == 0:
                print(f"合并失败: 输出文件大小为0，删除无效文件")
                os.remove(output_path)
                return False
            else:
                print(f"合并失败: 未生成有效的输出文件")
                return False

def main():
    # 使用示例
    merger = VideoMerger(
        input_dir="/Users/jonathan/Movies/87.有眼不识真锦鲤（35集）刘凯&尹玲",  # 输入视频所在文件夹
        output_dir="/Users/jonathan/Movies/87.有眼不识真锦鲤（35集）刘凯&尹玲"  # 输出文件夹
    )
    
    # 合并视频，根据编码兼容性自动选择是否重编码
    # 如果视频编码格式一致，将使用快速合并模式（不重编码，速度更快）
    # 如果视频编码格式不一致，则会自动使用重编码模式
    # 编码预设选项:
    # - 追求速度: 'ultrafast', 'superfast', 'veryfast'
    # - 平衡速度和质量: 'faster', 'fast', 'medium'
    # - 追求质量: 'slow', 'slower', 'veryslow'
    merger.merge_videos(
        "merged_video", 
        force_encode=False,  # 设为False以允许在编码兼容时使用更快的直接拷贝模式
        encode_preset='faster'  # 较快的编码速度，质量适中
    )

if __name__ == "__main__":
    main()