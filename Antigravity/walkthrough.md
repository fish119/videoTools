# VideoTools 应用交付文档

## 项目概述
VideoTools 是一个专门用于处理视频的Windows桌面应用程序，集成了以下三大功能：
1. **区间剪裁**：精准剪裁视频的多个时间段。
2. **视频压缩**：将视频压缩为H.265格式，节省存储空间。
3. **视频合并**：将多个视频可以按文件名顺序合并。

## 生成产物
- **可执行程序**: [dist/videoTools.exe](file:///e:/Code/Antigravity/vidwoTools/dist/videoTools.exe)
- **源代码**: `src/` 目录

## 安装与运行

### 1. 前置条件 (重要)
本应用依赖 **FFmpeg** 进行视频处理。在运行之前，请确保您的电脑上已安装 FFmpeg 并将其添加到了系统环境变量 PATH 中。

> [!IMPORTANT]
> 如果您未安装 FFmpeg，请访问 [FFmpeg官网](https://ffmpeg.org/download.html) 下载并安装，或者使用包管理器（如 `winget install ffmpeg`）进行安装。

### 2. 运行程序
直接双击 [dist/videoTools.exe](file:///e:/Code/Antigravity/vidwoTools/dist/videoTools.exe) 即可启动应用。

## 功能指南

### 区间剪裁
1. 点击 **"选择视频"** 导入需要处理的视频。
2. 在文本框中输入时间段：
   - 格式：两行为一组，第一行开始时间，第二行结束时间 (HH:MM:SS)。
   - 多组时间段之间用空行分隔。
3. 选择输出目录（默认 `D:\Download`）。
4. 点击 **"开始剪裁"**，生成的片段将自动命名为 `01.mp4`, `02.mp4` 等。

### 视频压缩
1. 点击 **"添加视频"** 选择一个或多个视频文件。
2. 确认输出目录。
3. 点击 **"开始压缩"**。程序将把视频转换为 H.265 编码 (CRF 30)。

### 视频合并
1. 点击 **"添加视频"** 选择多个视频。
2. 程序会自动按照文件名的升序排列视频。
3. 点击 **"开始合并"**，生成的新视频名为 `marg_YYYYMMDDhhmmss.mp4`。
