import os
import subprocess
from pathlib import Path

class VideoCompressor:
    def __init__(self):
        pass

    def compress_video(self, input_path, output_dir):
        """
        压缩单个视频
        :param input_path: 输入视频路径
        :param output_dir: 输出目录
        :return: (True, output_path) or (False, error_msg)
        """
        if not os.path.exists(input_path):
            return False, f"文件不存在: {input_path}"
        
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                return False, f"无法创建输出目录: {str(e)}"

        filename = Path(input_path).name
        output_path = os.path.join(output_dir, filename)
        
        # 避免输入输出同名覆盖（如果是同一目录）
        if os.path.abspath(input_path) == os.path.abspath(output_path):
            file_stem = Path(input_path).stem
            ext = Path(input_path).suffix
            output_path = os.path.join(output_dir, f"{file_stem}_compressed{ext}")

        # ffmpeg -i input -c:v libx265 -crf 30 -c:a aac output
        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_path),
            "-c:v", "libx265",
            "-crf", "30",
            "-c:a", "aac",
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
            
            if process.returncode != 0:
                return False, f"压缩失败: {process.stderr}"
            
            return True, output_path

        except Exception as e:
            return False, f"异常: {str(e)}"
