import os
import subprocess
from pathlib import Path

class VideoTrimmer:
    def __init__(self):
        pass

    def trim_video(self, input_path, time_segments, output_dir):
        """
        剪裁视频
        :param input_path: 输入视频路径
        :param time_segments: 时间段列表，格式 [(start, end), (start, end), ...]
        :param output_dir: 输出目录
        :return: (True, minsg) or (False, error_msg)
        """
        if not os.path.exists(input_path):
            return False, "输入文件不存在"
        
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                return False, f"无法创建输出目录: {str(e)}"

        input_filename = Path(input_path).name
        input_ext = Path(input_path).suffix

        results = []
        
        try:
            for idx, (start, end) in enumerate(time_segments, 1):
                # 格式化输出文件名: 01.mp4, 02.mp4...
                output_filename = f"{idx:02d}{input_ext}"
                output_path = os.path.join(output_dir, output_filename)
                
                # 构建 ffmpeg 命令
                # ffmpeg -y -i input -ss start -to end -c copy output
                # 注意：将 -ss 放在 -i 之前可以加快定位速度，但可能导致开始时刻不精准关键帧问题。
                # 放在 -i 之后更精准。这里选择放在 -i 后，或者 -ss before -i and -to after.
                # 简单起见： -i input -ss start -to end -c copy output
                cmd = [
                    "ffmpeg", "-y",
                    "-i", str(input_path),
                    "-ss", start.strip(),
                    "-to", end.strip(),
                    "-c", "copy",
                    str(output_path)
                ]
                
                # 执行命令
                # startupinfo用于隐藏控制台窗口 (Windows)
                startupinfo = None
                if os.name == 'nt':
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                
                process = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    startupinfo=startupinfo,
                    encoding='utf-8'
                )
                
                if process.returncode != 0:
                    return False, f"剪裁片段 {idx} 失败: {process.stderr}"
                
                results.append(output_path)
                
            return True, f"成功剪裁 {len(results)} 个片段"

        except Exception as e:
            return False, f"发生错误: {str(e)}"
