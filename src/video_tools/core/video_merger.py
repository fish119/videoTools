import os
import subprocess
import datetime
from pathlib import Path

class VideoMerger:
    def __init__(self):
        pass

    def merge_videos(self, input_files, output_dir):
        """
        合并视频
        :param input_files: 视频文件路径列表
        :param output_dir: 输出目录
        :return: (True, output_path) or (False, error_msg)
        """
        if not input_files:
            return False, "没有输入文件"
            
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                return False, f"无法创建输出目录: {str(e)}"

        # 1. 按文件名排序
        sorted_files = sorted(input_files, key=lambda p: Path(p).name)

        # 2. 生成文件列表文件 (temp_list.txt)
        # 放在输出目录临时使用
        list_file_path = os.path.join(output_dir, "temp_concat_list.txt")
        try:
            with open(list_file_path, 'w', encoding='utf-8') as f:
                for file_path in sorted_files:
                    # ffmpeg concat 需要 absolute path，并且注意转义
                    # 格式: file 'path'
                    # Windows路径反斜杠需要处理，替换为斜杠兼容性更好，或转义
                    abs_path = os.path.abspath(file_path).replace('\\', '/')
                    f.write(f"file '{abs_path}'\n")
        except Exception as e:
            return False, f"无法创建临时列表文件: {str(e)}"

        # 3. 生成输出文件名 marg_YYYYMMDDhhmmss.mp4
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        output_filename = f"marg_{timestamp}.mp4"
        output_path = os.path.join(output_dir, output_filename)

        # 4. 执行 ffmpeg 合并
        # ffmpeg -f concat -safe 0 -i list.txt -c copy output
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file_path,
            "-c", "copy",
            str(output_path)
        ]
        
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
        try:
            process = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                startupinfo=startupinfo,
                encoding='utf-8'
            )
            
            # 清理临时文件
            if os.path.exists(list_file_path):
                os.remove(list_file_path)
                
            if process.returncode != 0:
                return False, f"合并失败: {process.stderr}"
            
            return True, output_path

        except Exception as e:
            # 清理临时文件
            if os.path.exists(list_file_path):
                os.remove(list_file_path)
            return False, f"异常: {str(e)}"
