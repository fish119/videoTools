from PyQt6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget, QApplication
from PyQt6.QtGui import QFont
from video_tools.ui.trim_tab import TrimTab
from video_tools.ui.compress_tab import CompressTab
from video_tools.ui.merge_tab import MergeTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VideoTools - 视频处理工具")
        self.setWindowTitle("VideoTools - 视频处理工具")
        self.resize(500, 600)  # 调小默认宽高，尤其是宽度
        self.apply_styles()
        self.init_ui()

    def apply_styles(self):
        # 设置全局字体
        font = QFont("Microsoft YaHei UI", 10)
        font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        QApplication.setFont(font)
        
        # 简单的 Win11 风格 QSS 模拟
        # 1. 颜色: 背景 #f3f3f3, 控件白底圆角
        # 2. 交互: 悬停变色
        qss = """
        QMainWindow {
            background-color: #f0f3f9;
        }
        QWidget {
            color: #1a1a1a;
        }
        QTabWidget::pane {
            border: 1px solid #e0e0e0;
            background: #ffffff;
            border-radius: 8px;
            top: -1px; 
        }
        QTabBar::tab {
            background: #f0f3f9;
            border: none;
            padding: 8px 20px;
            margin-right: 4px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            color: #5d5d5d;
        }
        QTabBar::tab:selected {
            background: #ffffff;
            color: #0078d4;
            border-bottom: 2px solid #0078d4;
            font-weight: bold;
        }
        QTabBar::tab:hover {
            background: #e5e9f2;
        }
        QGroupBox {
            font-weight: bold;
            border: 1px solid #e5e5e5;
            border-radius: 6px;
            margin-top: 10px;
            padding-top: 15px;
            background-color: #ffffff;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 5px;
            left: 10px;
            color: #0078d4;
        }
        QPushButton {
            background-color: #ffffff;
            border: 1px solid #d1d1d1;
            border-radius: 4px;
            padding: 6px 12px;
            color: #1f1f1f;
        }
        QPushButton:hover {
            background-color: #f5f5f5;
            border-color: #0078d4;
        }
        QPushButton:pressed {
            background-color: #e0e0e0;
        }
        /* 主操作按钮特殊样式 */
        QPushButton[text^="开始"] {
            background-color: #0078d4;
            color: white;
            border: none;
        }
        QPushButton[text^="开始"]:hover {
            background-color: #1084d9;
        }
        QPushButton[text^="开始"]:pressed {
            background-color: #006cc1;
        }
        QLineEdit, QTextEdit, QListWidget {
            background-color: #ffffff;
            border: 1px solid #d1d1d1;
            border-radius: 4px;
            padding: 4px;
            selection-background-color: #0078d4;
        }
        QLineEdit:focus, QTextEdit:focus, QListWidget:focus {
            border: 1px solid #0078d4;
        }
        /* 滚动条美化 */
        QScrollBar:vertical {
            border: none;
            background: #f0f0f0;
            width: 8px;
            border-radius: 4px;
        }
        QScrollBar::handle:vertical {
            background: #c1c1c1;
            border-radius: 4px;
        }
        QScrollBar::handle:vertical:hover {
            background: #a8a8a8;
        }
        """
        self.setStyleSheet(qss)


    def init_ui(self):
        # 创建主部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 创建布局
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        
        # 创建Tab控件
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # 添加各个Tab
        self.trim_tab = TrimTab()
        self.compress_tab = CompressTab()
        self.merge_tab = MergeTab()
        
        self.tabs.addTab(self.trim_tab, "区间剪裁")
        self.tabs.addTab(self.compress_tab, "视频压缩")
        self.tabs.addTab(self.merge_tab, "视频合并")
        
        # 默认选中第一个Tab
        self.tabs.setCurrentIndex(0)
