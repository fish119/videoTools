# VideoTools Windows桌面应用实施计划

## 项目概述

开发一个Windows桌面应用程序 `videoTools.exe`，提供三个主要功能：
1. **区间剪裁** - 将视频按指定时间段剪裁成多个片段
2. **视频压缩** - 使用H.265编码压缩视频
3. **视频合并** - 将多个视频文件合并为一个

## 技术选型

| 组件 | 技术方案 | 说明 |
|------|----------|------|
| GUI框架 | PyQt6 | 跨平台GUI框架，功能强大，支持Tab控件 |
| 视频处理 | FFmpeg | 业界标准视频处理工具，通过subprocess调用 |
| 打包工具 | PyInstaller | 将Python应用打包为独立exe |
| 依赖管理 | uv | 按用户规则使用uv管理依赖 |

## 用户审核事项

> [!IMPORTANT]
> **FFmpeg依赖**：本应用需要系统安装FFmpeg并添加到PATH环境变量中。请确认您的系统已安装FFmpeg。

> [!NOTE]
> **默认输出目录**：区间剪裁和视频压缩的默认输出目录设置为 `D:\Download`，请确认该目录存在或可创建。

---

## 项目结构

```
vidwoTools/
├── pyproject.toml          # 项目配置和依赖
├── src/
│   └── video_tools/
│       ├── __init__.py
│       ├── main.py         # 程序入口
│       ├── ui/
│       │   ├── __init__.py
│       │   ├── main_window.py      # 主窗口
│       │   ├── trim_tab.py         # 区间剪裁Tab
│       │   ├── compress_tab.py     # 视频压缩Tab
│       │   └── merge_tab.py        # 视频合并Tab
│       └── core/
│           ├── __init__.py
│           ├── video_trimmer.py    # 剪裁逻辑
│           ├── video_compressor.py # 压缩逻辑
│           └── video_merger.py     # 合并逻辑
└── build.py                # 打包脚本
```

---

## 模块设计

### 主窗口 ([NEW] main_window.py)

- 创建带有3个Tab的主界面
- Tab标签：区间剪裁、视频压缩、视频合并
- 默认显示第一个Tab（区间剪裁）
- 窗口标题：VideoTools

### 区间剪裁Tab ([NEW] trim_tab.py)

**界面元素：**
- 视频文件选择按钮 + 显示已选文件路径
- 多行文本输入框（时间段输入）
- 输出目录选择 + 默认值 `D:\Download`
- "打开文件夹"按钮
- "开始剪裁"按钮
- 进度/状态显示

**时间段解析逻辑：**
```
输入格式：
00:02:20    ← 开始时间1
00:03:30    ← 结束时间1
            ← 空行分隔
00:04:20    ← 开始时间2
00:05:10    ← 结束时间2
```

### 视频压缩Tab ([NEW] compress_tab.py)

**界面元素：**
- 视频文件选择按钮（支持多选）+ 显示已选文件列表
- 固定参数显示：H.265编码，CRF=30
- 输出目录选择 + 默认值 `D:\Download`
- "打开文件夹"按钮
- "开始压缩"按钮
- 进度/状态显示

### 视频合并Tab ([NEW] merge_tab.py)

**界面元素：**
- 视频文件选择按钮（支持多选）+ 显示已选文件列表
- 输出目录选择 + 默认值 `D:\Download`
- "打开文件夹"按钮
- "开始合并"按钮
- 进度/状态显示

**输出文件命名：** `merge_YYYYMMDDhhmmss.mp4`

---

## 核心处理逻辑

### 视频剪裁 ([NEW] video_trimmer.py)

使用FFmpeg命令：
```bash
ffmpeg -i input.mp4 -ss 00:02:20 -to 00:03:30 -c copy output_01.mp4
```
- 使用 `-c copy` 避免重新编码，速度快
- 输出文件命名：01.mp4, 02.mp4, 03.mp4...

### 视频压缩 ([NEW] video_compressor.py)

使用FFmpeg命令：
```bash
ffmpeg -i input.mp4 -c:v libx265 -crf 30 -c:a aac output.mp4
```
- H.265编码：`-c:v libx265`
- CRF质量：`-crf 30`
- 音频保持AAC编码

### 视频合并 ([NEW] video_merger.py)

使用FFmpeg concat协议：
```bash
# 先创建文件列表 files.txt
file 'video1.mp4'
file 'video2.mp4'

# 执行合并
ffmpeg -f concat -safe 0 -i files.txt -c copy output.mp4
```
- 按文件名升序排序后合并
- 输出命名：`merge_20260109123745.mp4`

---

## 验证计划

### 功能测试
1. **区间剪裁测试**
   - 选择视频文件
   - 输入多个时间段
   - 验证输出文件数量和命名正确

2. **视频压缩测试**
   - 选择多个视频
   - 验证压缩后文件大小减小
   - 验证使用H.265编码

3. **视频合并测试**
   - 选择多个视频
   - 验证合并后文件正确
   - 验证文件名格式正确

### 打包验证
- 使用PyInstaller打包为单个exe
- 在无Python环境的Windows上测试运行
