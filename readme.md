Certainly! Below is a modern and stylish `README.md` for the `FFmpegWrapper` Python module with updated formatting, additional clarity, and enhanced aesthetics for an improved developer experience.

---

# FFmpegWrapper Python Module

![FFmpegWrapper](https://img.shields.io/badge/FFmpegWrapper-Python-blue)  
A simple and easy-to-use Python wrapper for **local `ffmpeg` binaries**, enabling seamless multimedia processing in your Python projects. Perform tasks like video conversion, audio extraction, video trimming, and more, all from within Python without the need to install `ffmpeg` globally.

---

## 🚀 Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
  - [Initialize the Wrapper](#initialize-the-wrapper)
  - [Common Operations](#common-operations)
    - [Convert Video](#convert-video)
    - [Extract Audio](#extract-audio)
    - [Get Video Info](#get-video-info)
    - [Trim Video](#trim-video)
    - [Change Video Resolution](#change-video-resolution)
    - [Add Watermark](#add-watermark)
- [Testing the Wrapper](#testing-the-wrapper)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 📚 Overview

`FFmpegWrapper` is a clean, lightweight Python module designed to interact with **local `ffmpeg` binaries**. It simplifies video and audio processing tasks with just a few lines of code. Unlike global `ffmpeg` installations, this wrapper allows you to specify a **local `ffmpeg` binary path**, making it easy to work in isolated environments or with specific `ffmpeg` versions.

**Features**:
- Convert video and audio formats.
- Extract audio from video files.
- Retrieve detailed video metadata.
- Trim and resize videos.
- Apply watermarks to videos.

---

## 💻 Installation

### 1. Install `ffmpeg` Locally

You **do not need to install `ffmpeg` globally** to use this wrapper. Simply download a **local `ffmpeg` binary** and point to it when initializing the wrapper.

- **On Windows**:
  - Download `ffmpeg` from the [FFmpeg Downloads](https://ffmpeg.org/download.html) page.
  - Extract the contents and remember the path to the `bin/ffmpeg.exe` file (e.g., `C:/ffmpeg/bin/ffmpeg.exe`).

- **On macOS**:
  - Install using [Homebrew](https://brew.sh/):
    ```bash
    brew install ffmpeg
    ```
  - Or download the static build from [FFmpeg Downloads](https://ffmpeg.org/download.html).
  
- **On Linux**:
  - Install via your package manager:
    ```bash
    sudo apt install ffmpeg
    ```

### 2. Add `FFmpegWrapper` to Your Project

Simply download or clone the `FFmpegWrapper` Python script (`ffmpeg_wrapper.py`) into your project directory. No pip installation is needed.

---

## ⚡ Usage

### Initialize the Wrapper

The `FFmpegWrapper` class is easy to initialize. While it works with **local `ffmpeg` binaries**, you must specify the path to `ffmpeg` if it's not already in your system’s `PATH`.

#### Example:

```python
from ffmpeg_wrapper import FFmpegWrapper

# Initialize with the path to the ffmpeg binary
ffmpeg = FFmpegWrapper(ffmpeg_path="/path/to/ffmpeg")

# Or use if ffmpeg is already available in your system's PATH
ffmpeg = FFmpegWrapper()
```

Once initialized, you can easily interact with your video and audio files.

---

### Common Operations

#### Convert Video

Convert a video from one format to another. The `convert_video()` function supports setting the video and audio codecs, as well as adjusting the quality.

```python
stdout, stderr, returncode = ffmpeg.convert_video("input.mp4", "output.mkv")
```

#### Parameters:
- `input_file`: Path to the input video file.
- `output_file`: Path to save the converted video.
- `codec` (optional): Video codec (default: `libx264`).
- `crf` (optional): Constant Rate Factor for video quality (default: `23`).
- `audio_codec` (optional): Audio codec (default: `aac`).
- `audio_bitrate` (optional): Audio bitrate (default: `192k`).

#### Extract Audio

Extract audio from a video and save it in your desired format.

```python
stdout, stderr, returncode = ffmpeg.extract_audio("input.mp4", "output_audio.mp3")
```

#### Parameters:
- `input_file`: Path to the input video.
- `output_audio_file`: Path where the audio will be saved.

#### Get Video Info

Retrieve detailed information about a video (e.g., codec, duration, resolution).

```python
stdout, stderr, returncode = ffmpeg.get_video_info("input.mp4")
print(stdout)
```

#### Parameters:
- `input_file`: Path to the input video.

#### Trim Video

Trim a video by specifying the start time and duration.

```python
stdout, stderr, returncode = ffmpeg.trim_video("input.mp4", "output_trimmed.mp4", "00:01:00", "00:00:30")
```

#### Parameters:
- `input_file`: Path to the input video.
- `output_file`: Path to save the trimmed video.
- `start_time`: Start time in `HH:MM:SS` format.
- `duration`: Duration of the trim, also in `HH:MM:SS`.

#### Change Video Resolution

Resize a video to a new resolution.

```python
stdout, stderr, returncode = ffmpeg.change_video_resolution("input.mp4", "output_resized.mp4", "640x360")
```

#### Parameters:
- `input_file`: Path to the input video.
- `output_file`: Path where the resized video will be saved.
- `resolution`: Desired resolution in the format `widthxheight` (e.g., `640x360`).

#### Add Watermark

Overlay an image (watermark) onto a video at a specific position.

```python
stdout, stderr, returncode = ffmpeg.add_watermark("input.mp4", "output_with_watermark.mp4", "watermark.png", "top-left")
```

#### Parameters:
- `input_file`: Path to the input video.
- `output_file`: Path to save the watermarked video.
- `watermark_image`: Path to the watermark image (e.g., `"watermark.png"`).
- `position`: Position of the watermark (e.g., `"top-left"`, `"bottom-right"`).

---

## 🧪 Testing the Wrapper

To test the wrapper, follow these steps:

1. **Download** or **copy** the `FFmpegWrapper` script into your project.
2. **Ensure that `ffmpeg` is installed locally** and that you know the path to the `ffmpeg` binary.
3. Create a test script, for example:

```python
from ffmpeg_wrapper import FFmpegWrapper

# Initialize wrapper with local ffmpeg binary
ffmpeg = FFmpegWrapper(ffmpeg_path="/path/to/ffmpeg")

# Test video conversion
stdout, stderr, returncode = ffmpeg.convert_video("input.mp4", "output.mkv")
print(stdout, stderr, returncode)

# Test audio extraction
stdout, stderr, returncode = ffmpeg.extract_audio("input.mp4", "output_audio.mp3")
print(stdout, stderr, returncode)

# Test getting video info
stdout, stderr, returncode = ffmpeg.get_video_info("input.mp4")
print(stdout)
```

4. Run the script:
   ```bash
   python test_script.py
   ```

The script should output success/failure messages, as well as the standard output and error.

---

## 🔧 Troubleshooting

### **`FileNotFoundError: ffmpeg binary not found`**

- **Cause**: The path to `ffmpeg` is incorrect or not specified.
- **Solution**: Ensure that the `ffmpeg` binary path is correct or that `ffmpeg` is in your system’s `PATH`.

### **`subprocess.CalledProcessError`**

- **Cause**: `ffmpeg` failed to execute the command.
- **Solution**: Check `stderr` for more details. Common causes include incorrect input files, unsupported formats, or invalid parameters.

### **Unsupported File Formats**

- **Cause**: The input or output format is not supported by `ffmpeg`.
- **Solution**: Verify that `ffmpeg` supports the formats you're working with by running:
  ```bash
  ffmpeg -formats
  ```

---

## 🤝 Contributing

We welcome contributions! Here’s how you can help:
1. Fork the repo.
2. Create a new branch.
3. Implement your changes.
4. Submit a pull request.

I'll’ll review your PR and merge if it fits.

---

## 📝 License
None yet, feel free to use this wrapper in your projects.
