from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTextEdit, QFileDialog, QMessageBox, QGroupBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from video_tools.core.video_trimmer import VideoTrimmer
import os
import subprocess

class TrimWorker(QThread):
    finished = pyqtSignal(bool, str)

    def __init__(self, input_path, segments, output_dir):
        super().__init__()
        self.input_path = input_path
        self.segments = segments
        self.output_dir = output_dir
        self.trimmer = VideoTrimmer()

    def run(self):
        success, msg = self.trimmer.trim_video(self.input_path, self.segments, self.output_dir)
        self.finished.emit(success, msg)

class TrimTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # 1. 视频选择区域
        video_group = QGroupBox("1. 选择视频")
        video_layout = QHBoxLayout()
        video_group.setLayout(video_layout)
        
        self.video_path_edit = QLineEdit()
        self.video_path_edit.setPlaceholderText("请选择要剪裁的视频文件...")
        self.video_path_edit.setReadOnly(True)
        video_layout.addWidget(self.video_path_edit)
        
        btn_select_video = QPushButton("选择视频")
        btn_select_video.clicked.connect(self.select_video)
        video_layout.addWidget(btn_select_video)
        
        main_layout.addWidget(video_group)
        
        # 2. 时间段输入区域
        time_group = QGroupBox("2. 输入剪裁时间段")
        time_layout = QVBoxLayout()
        time_group.setLayout(time_layout)
        
        tip_label = QLabel("格式说明：第一行为开始时间，第二行为结束时间。\n不同时间段之间可用空行分隔。")
        tip_label.setStyleSheet("color: gray;")
        time_layout.addWidget(tip_label)
        
        self.time_edit = QTextEdit()
        self.time_edit.setPlaceholderText("00:02:20\n00:03:30\n\n00:04:20\n00:05:10\n\n00:20:21\n00:28:27")
        time_layout.addWidget(self.time_edit)
        
        main_layout.addWidget(time_group)
        
        # 3. 输出目录区域
        out_group = QGroupBox("3. 输出设置")
        out_layout = QHBoxLayout()
        out_group.setLayout(out_layout)
        
        self.out_dir_edit = QLineEdit()
        self.out_dir_edit.setText(r"D:\Download")
        out_layout.addWidget(self.out_dir_edit)
        
        btn_select_out = QPushButton("选择目录")
        btn_select_out.clicked.connect(self.select_output_dir)
        out_layout.addWidget(btn_select_out)
        
        btn_open_out = QPushButton("📂 打开文件夹")
        btn_open_out.clicked.connect(self.open_output_dir)
        out_layout.addWidget(btn_open_out)
        
        main_layout.addWidget(out_group)
        
        # 4. 操作区域
        action_layout = QHBoxLayout()
        self.btn_start = QPushButton("开始剪裁")
        self.btn_start.setMinimumHeight(40)
        self.btn_start.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.btn_start.clicked.connect(self.start_trimming)
        action_layout.addWidget(self.btn_start)
        
        main_layout.addLayout(action_layout)
        
        # 状态标
        self.status_label = QLabel("准备就绪")
        main_layout.addWidget(self.status_label)
        
    def select_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择视频文件", "", "Video Files (*.mp4 *.mkv *.avi *.mov);;All Files (*)"
        )
        if file_path:
            self.video_path_edit.setText(file_path)
            
    def select_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择保存目录", self.out_dir_edit.text())
        if dir_path:
            self.out_dir_edit.setText(dir_path)
            
    def open_output_dir(self):
        path = self.out_dir_edit.text()
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except:
                QMessageBox.warning(self, "错误", f"目录不存在且无法创建: {path}")
                return
        os.startfile(path)
        
    def parse_time_segments(self):
        text = self.time_edit.toPlainText().strip()
        if not text:
            return []
            
        segments = []
        # 获取所有非空行
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        
        # 每两行为一组
        for i in range(0, len(lines), 2):
            if i + 1 < len(lines):
                start = lines[i]
                end = lines[i+1]
                # 简单校验
                if ':' in start and ':' in end:
                    segments.append((start, end))
                    
        return segments

    def start_trimming(self):
        video_path = self.video_path_edit.text()
        output_dir = self.out_dir_edit.text()
        
        if not video_path:
            QMessageBox.warning(self, "提示", "请先选择视频文件")
            return
            
        segments = self.parse_time_segments()
        if not segments:
            QMessageBox.warning(self, "提示", "请按正确格式输入时间段")
            return
            
        self.btn_start.setEnabled(False)
        self.status_label.setText("正在剪裁中...")
        
        self.worker = TrimWorker(video_path, segments, output_dir)
        self.worker.finished.connect(self.on_trim_finished)
        self.worker.start()
        
    def on_trim_finished(self, success, msg):
        self.btn_start.setEnabled(True)
        self.status_label.setText(msg)
        if success:
            QMessageBox.information(self, "完成", msg)
        else:
            QMessageBox.critical(self, "错误", msg)
