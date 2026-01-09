# VideoTools - 简易视频处理工具箱

这是一个完全使用Google Antigravity开发的视频处理工具。所有内容均由Antigravity提供，包括代码、界面、文档等。

VideoTools 是一个基于 Python (PyQt6) 开发的 Windows 桌面视频处理工具。它提供了一个现代化的图形界面，集成了视频剪裁、压缩和合并三大常用功能，操作简单高效。

## ✨ 主要功能

### 1. ✂️ 区间剪裁 (Trim)
- **精准剪辑**：支持对单个视频进行多段剪辑。
- **批量处理**：一次性输出多个剪辑片段。
- **智能解析**：支持通过文本快速输入时间段（如 `00:02:20`），自动解析开始与结束时间。

### 2. 📉 视频压缩 (Compress)
- **高效压缩**：使用先进的 **H.265 (HEVC)** 编码格式。
- **批量操作**：支持一次性添加并压缩多个视频文件。
- **画质平衡**：默认采用 CRF 30 参数，在显著减小体积的同时保持良好的视觉质量。

### 3. 🔗 视频合并 (Merge)
- **无损合并**：快速将多个视频文件拼接为一个。
- **自动排序**：自动根据文件名进行升序排列，确保合并顺序正确。
- **自动命名**：生成的文件自动包含时间戳，避免重名。

---

## 🛠️ 安装与运行

### 前置要求
⚠️ **重要**：本程序底层依赖 **FFmpeg** 工具。在运行之前，请务必确保您的电脑已安装 FFmpeg 并配置了系统环境变量 `PATH`。

### 方式一：直接运行 (推荐)
生成的最终可执行文件位于 `dist` 目录下：
1. 进入 `dist/` 文件夹。
2. 双击 `videoTools.exe` 即可启动。

### 方式二：源码开发与运行

**1. 环境配置**
本项目使用 `uv` 进行现代化的 Python 依赖管理。

```bash
# 初始化环境并安装依赖
uv sync
```

**2. 运行源代码**
```bash
uv run python src/video_tools/main.py
```

**3. 打包为 EXE**
如果您修改了代码并希望重新打包：
```bash
uv run pyinstaller --name videoTools --onefile --noconsole --clean --paths=src src/video_tools/main.py
```

---

## 📂 项目结构

```
vidwoTools/
├── src/
│   └── video_tools/
│       ├── core/               # 核心逻辑层
│       │   ├── video_trimmer.py    # 剪裁逻辑 (ffmpeg -ss -to)
│       │   ├── video_compressor.py # 压缩逻辑 (ffmpeg -c:v libx265)
│       │   └── video_merger.py     # 合并逻辑 (ffmpeg concat)
│       ├── ui/                 # 界面层 (PyQt6)
│       │   ├── main_window.py      # 主窗口框架
│       │   └── ...                 # 各功能Tab页
│       └── main.py             # 程序入口
├── dist/                   # 构建产物目录
├── pyproject.toml          # 依赖配置文件
└── README.md               # 项目说明文档
```

## 🎨 界面风格
项目采用了 Windows 11 风格的现代化 UI 设计，支持高 DPI 屏幕显示，字体清晰锐利。

---
*Created by Antigravity*
