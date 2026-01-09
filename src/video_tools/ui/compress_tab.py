from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QListWidget, QFileDialog, 
                             QMessageBox, QLineEdit, QGroupBox, QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from video_tools.core.video_compressor import VideoCompressor
import os

class CompressWorker(QThread):
    progress = pyqtSignal(str) # 实时日志
    finished = pyqtSignal(bool, str) # 任务结束 (is_success, summary_msg)

    def __init__(self, file_list, output_dir):
        super().__init__()
        self.file_list = file_list
        self.output_dir = output_dir
        self.compressor = VideoCompressor()
        self.is_running = True

    def run(self):
        success_count = 0
        fail_count = 0
        total = len(self.file_list)
        
        for idx, file_path in enumerate(self.file_list, 1):
            if not self.is_running:
                break
                
            self.progress.emit(f"[{idx}/{total}] 正在压缩: {os.path.basename(file_path)} ...")
            
            ok, msg = self.compressor.compress_video(file_path, self.output_dir)
            if ok:
                success_count += 1
                self.progress.emit(f"√ 完成: {os.path.basename(file_path)}")
            else:
                fail_count += 1
                self.progress.emit(f"× 失败: {os.path.basename(file_path)} -> {msg}")
                
        self.finished.emit(True, f"处理完成。成功: {success_count}, 失败: {fail_count}")

    def stop(self):
        self.is_running = False

class CompressTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.files = []
        
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 1. 视频选择列表
        file_group = QGroupBox("1. 选择视频 (支持多选)")
        file_layout = QVBoxLayout()
        file_group.setLayout(file_layout)
        
        btn_layout = QHBoxLayout()
        btn_add = QPushButton("添加视频")
        btn_add.clicked.connect(self.add_files)
        btn_clear = QPushButton("清空列表")
        btn_clear.clicked.connect(self.clear_files)
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_clear)
        btn_layout.addStretch()
        file_layout.addLayout(btn_layout)
        
        self.file_list_widget = QListWidget()
        file_layout.addWidget(self.file_list_widget)
        
        layout.addWidget(file_group)
        
        # 2. 参数说明
        info_label = QLabel("压缩参数：编码 H.265, CRF 30 (固定)")
        info_label.setStyleSheet("color: blue;")
        layout.addWidget(info_label)
        
        # 3. 输出设置
        out_group = QGroupBox("2. 输出设置")
        out_layout = QHBoxLayout()
        out_group.setLayout(out_layout)
        
        self.out_dir_edit = QLineEdit(r"D:\Download")
        out_layout.addWidget(self.out_dir_edit)
        
        btn_select_out = QPushButton("选择目录")
        btn_select_out.clicked.connect(self.select_output_dir)
        out_layout.addWidget(btn_select_out)
        
        btn_open_out = QPushButton("📂 打开文件夹")
        btn_open_out.clicked.connect(self.open_output_dir)
        out_layout.addWidget(btn_open_out)
        
        layout.addWidget(out_group)
        
        # 4. 操作与状态
        action_layout = QHBoxLayout()
        self.btn_start = QPushButton("开始压缩")
        self.btn_start.setMinimumHeight(40)
        self.btn_start.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.btn_start.clicked.connect(self.start_compression)
        action_layout.addWidget(self.btn_start)
        
        layout.addLayout(action_layout)
        
        self.status_label = QLabel("准备就绪")
        layout.addWidget(self.status_label)
        
    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "选择视频", "", "Video Files (*.mp4 *.mkv *.avi *.mov);;All Files (*)"
        )
        if files:
            self.files.extend(files)
            # 去重
            self.files = list(set(self.files))
            self.refresh_list()
            
    def clear_files(self):
        self.files = []
        self.refresh_list()
        
    def refresh_list(self):
        self.file_list_widget.clear()
        for f in self.files:
            self.file_list_widget.addItem(f)
            
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
                return
        os.startfile(path)

    def start_compression(self):
        if not self.files:
            QMessageBox.warning(self, "提示", "请先添加视频文件")
            return
            
        output_dir = self.out_dir_edit.text()
        
        self.btn_start.setEnabled(False)
        self.status_label.setText("正在压缩...")
        
        self.worker = CompressWorker(self.files, output_dir)
        self.worker.progress.connect(self.update_status)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()
        
    def update_status(self, msg):
        self.status_label.setText(msg)
        
    def on_finished(self, success, summary):
        self.btn_start.setEnabled(True)
        self.status_label.setText(summary)
        QMessageBox.information(self, "完成", summary)
