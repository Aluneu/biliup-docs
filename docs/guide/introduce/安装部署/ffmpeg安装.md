# FFmpeg 安装

> [!NOTE]
> 仅在使用 `streamlink` 或 `ffmpeg` 下载器时需要安装 FFmpeg。默认下载器 `stream-gears` 无需 FFmpeg。

---

## 1. 简介

FFmpeg 是一个开源的音视频处理工具集，支持转码、流媒体、滤镜等多媒体操作。

典型用途：视频格式转换、提取音频、录制屏幕、流媒体处理。

---

## 2. 各系统安装方法

### Windows

**方法一：winget（推荐）**

以管理员身份运行 CMD：

```cmd
winget install BtbN.FFmpeg.GPL
```

**方法二：手动安装**

1. 访问 [FFmpeg Builds 页面](https://github.com/BtbN/FFmpeg-Builds/releases)
2. 下载 `ffmpeg-master-latest-win64-gpl.zip` 并解压
3. 将 `bin` 文件夹路径（如 `D:\ffmpeg\bin`）添加到系统 PATH 环境变量

### macOS

```bash
# 安装 Homebrew（如未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 FFmpeg
brew install ffmpeg
```

### Linux

**Debian / Ubuntu：**

```bash
sudo apt update && sudo apt install -y ffmpeg
```

**RHEL / CentOS / Fedora：**

```bash
sudo dnf install -y ffmpeg
```

**Arch / Manjaro：**

```bash
sudo pacman -S ffmpeg
```

### 通用方案：二进制手动安装

```bash
# 下载
wget https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz

# 解压
tar Jxvf ffmpeg-master-latest-linux64-gpl.tar.xz

# 添加到 PATH（编辑 ~/.bashrc，末尾添加）
export PATH="/root/ffmpeg-master-latest-linux64-gpl/bin:$PATH"

# 重新加载
source ~/.bashrc
```

---

## 3. 验证安装

```bash
ffmpeg -version
```

输出应显示版本号及编解码器支持列表。

---

## 4. 常见问题

**"Command not found" 错误：** 检查环境变量配置是否正确。

**Windows PATH 不生效：** 重启终端或注销重新登录。
