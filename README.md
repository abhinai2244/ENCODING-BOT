# VideoEncoder Bot

A powerful Telegram bot for compressing, encoding, and manipulating video files. Built with Python (Pyrofork) and FFmpeg.

## 🚀 Features

### 🎥 Video Encoding
- **Formats**: Supports encoding to **MKV**, **MP4**, **AVI**.
- **Codecs**: Choose between **H264** (x264) and **H265** (HEVC).
- **Quality Control**: 
  - Custom **CRF** (Constant Rate Factor).
  - **Presets** (UltraFast to VerySlow).
  - **10-bit** encoding support.
- **Resolution**: Downscale videos to 1080p, 720p, 540p, 480p, 360p, or keep original.
- **Audio**: 
  - Change audio codecs (AAC, AC3, OPUS, MP3, etc.).
  - Custom bitrate and sample rates.
  - Mix/Remix audio channels (Stereo, Mono, 5.1).

### 🎛 Audio Rearrangement (`/af`)
- Interactively **reorder audio streams** in a video file using an inline button menu.
- Set the default audio track by moving it to the top.

### 📥 Download Methods
- **Telegram Files** (`/dl`): Reply to a video or document to process it.
- **Direct Links** (`/ddl`): Download files from direct URLs.
- **Batch Processing** (`/batch`): Process multiple links or files.

### 🛠 Utilities
- **Speedtest** (`/speedtest`): Check the server's internet speed and view a graphical report.
- **System Status** (`/status`): View real-time CPU, RAM, Disk usage, and active tasks queue.
- **Settings**: Per-user settings menu (`/settings`) to customize encoding preferences.
- **Watermark**: Add custom hardsub watermarks or metadata.
- **Subtitles**: Hardsub or copy soft subtitles.

## 🤖 Commands

| Command | Description |
| :--- | :--- |
| `/start` | Check if the bot is online. |
| `/help` | Show help message. |
| `/settings` | Open personal encoding settings menu. |
| `/reset` | Reset your settings to default. |
| `/vset` | View current video settings summary. |
| `/dl` | Download and process a Telegram file (Reply to message). |
| `/af` | Interactive audio stream rearrangement (Reply to message). |
| `/ddl [url]` | Download and process a file from a direct link. |
| `/speedtest` | Run an internet speed test. |
| `/status` | Show server stats and active queue. |
| `/stats` | Show bot statistics (Users, Uptime). |
| `/clean` | (Sudo) Clean download/encode directories. |
| `/restart` | (Sudo) Restart the bot. |
| `/update` | (Sudo) Update the bot from git. |

## ⚙️ Configuration

The bot is configured via environment variables (or `config.env`).

- `API_ID`, `API_HASH`: Telegram API credentials.
- `BOT_TOKEN`: Telegram Bot Token.
- `MONGO_URI`: MongoDB connection string.
- `OWNER_ID`: Your Telegram User ID.
- `SUDO_USERS`: List of admin user IDs.
- `LOG_CHANNEL`: Channel ID for logging tasks.
- `DOWNLOAD_DIR`, `ENCODE_DIR`: Paths for working directories.

## 🏃 How to Run

### Normal Execution

To run the bot normally, ensure you have Python 3.9+ and FFmpeg installed.

1. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
2. Start the bot:
   ```bash
   python3 -m VideoEncoder
   ```

### Docker

To run the bot using Docker:

1. Build the image:
   ```bash
   docker build -t video-encoder .
   ```
2. Run the container:
   ```bash
   docker run -d --env-file config.env video-encoder
   ```

## 📝 Notes

- **Task Limit**: Each user is limited to one active task at a time to ensure fair usage.
- **Settings Isolation**: Users cannot modify each other's settings via the interactive menu.
