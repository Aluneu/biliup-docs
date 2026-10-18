# FFmpeg 安装

::: info
仅在使用 `streamlink` 或 `ffmpeg` 下载器时需要安装 FFmpeg。默认下载器 `mesio` 无需 FFmpeg。

但 **v1.3.0 的画面遮挡、录后合成与精确剪** 依赖 FFmpeg：建议使用带 `libx264` 与 `libass` 的完整构建。

> Docker 镜像与 Windows 桌面版安装包**已经内置 FFmpeg**（同一份 BtbN 构建），这两种方式不用另外安装。
:::


---

## 1. 各系统安装方法

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

# 添加到 PATH（编辑 ~/.bashrc，末尾添加；路径换成你实际解压出来的目录）
export PATH="$HOME/ffmpeg-master-latest-linux64-gpl/bin:$PATH"

# 重新加载
source ~/.bashrc
```

---

## 2. 验证安装

```bash
ffmpeg -version
```

输出应显示版本号及编解码器支持列表。

---

## 3. 常见问题

**"Command not found" 错误：** 检查环境变量配置是否正确。

**Windows PATH 不生效：** 重启终端或注销重新登录。
