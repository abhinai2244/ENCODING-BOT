<div align="center">
  <img src="https://prod.assets.earlygamecdn.com/images/Chisa.jpg?transform=Banner+Webp" alt="VideoEncoder Bot" width="100%">

  # 🎬 VideoEncoder Bot

  <p>
    <b>A powerful Telegram bot for compressing, encoding, and manipulating video files.</b><br>
    <i>Built with Python (Pyrofork) and FFmpeg.</i>
  </p>

  <p>
    <a href="https://t.me/cantarellabots"><img src="https://img.shields.io/badge/Channel-Cantarella%20Bots-blue?style=for-the-badge&logo=telegram"></a>
    <a href="https://t.me/cantarella_wuwa"><img src="https://img.shields.io/badge/Developer-cantarella__wuwa-blue?style=for-the-badge&logo=telegram"></a>
    <a href="https://github.com/abhinai2244/Encoding-Bot"><img src="https://img.shields.io/badge/Language-Python-green?style=for-the-badge&logo=python"></a>
  </p>
</div>

---

## ✨ Features

### 🎥 Video Encoding
* **Formats:** Encodes seamlessly to **MKV**, **MP4**, and **AVI**.
* **Codecs:** Choose between **H.264 (x264)** and **H.265 (HEVC)** for maximum compression.
* **Quality Control:** 
  * Custom **CRF** (Constant Rate Factor) settings.
  * Various **Presets** (UltraFast to VerySlow).
  * True **10-bit** encoding support.
* **Resolution:** Downscale videos to 1080p, 720p, 540p, 480p, 360p, or maintain original scale.
* **Audio:** 
  * Re-encode audio codecs (AAC, AC3, OPUS, MP3, etc.).
  * Custom bitrate and sample rates.
  * Mix/Remix audio channels (Stereo, Mono, 5.1).

### 🎛 Audio Rearrangement (`/af`)
* Interactively **reorder audio streams** within a video file using a smooth inline button menu.
* Set the default audio track easily by pushing it to the top slot.

### 📥 Download Methods
* **Telegram Files (`/dl`)**: Just reply to a video or document to process it natively.
* **Direct Links (`/ddl`)**: Pass direct URLs to download and encode files from the web.
* **Batch Processing (`/batch`)**: Automate your workflow by processing multiple links or files.

### 🛠 Utilities
* **Speedtest (`/speedtest`)**: Test server internet speed with graphical reports.
* **System Status (`/status`)**: Live tracking of CPU, RAM, Disk usage, and task queues.
* **Settings (`/settings`)**: Isolated per-user settings to customize individual encoding preferences.
* **Watermarks & Metadata**: Apply custom static or motion watermarks (with adjustable opacity) and modify metadata fields.
* **Subtitles**: Hardsub subtitles directly or copy soft subtitles.

---

## 🤖 Commands List

| Command | Description |
| :--- | :--- |
| `/start` | Check if the bot is alive. |
| `/help` | Display the interactive help menu. |
| `/settings` | Open personal encoding settings menu. |
| `/reset` | Reset your encoding settings to default. |
| `/vset` | View a summary of your current video settings. |
| `/dl` | Download & process a Telegram file (Reply to message). |
| `/af` | Interactive audio stream rearrangement (Reply to message). |
| `/ddl [url]` | Download & process a file from a direct link. |
| `/speedtest` | Run an internet speed test. |
| `/status` | View server statistics and active queue. |
| `/stats` | View bot statistics (Users, Uptime). |
| `/clean` | **[Sudo]** Clean download & encode directories. |
| `/restart` | **[Sudo]** Restart the bot safely. |
| `/update` | **[Sudo]** Update the bot from git repository. |

---

## ⚙️ Configuration

Configure the bot easily via environment variables or a `config.env` file.

* `API_ID` & `API_HASH` — Telegram API credentials (from my.telegram.org)
* `BOT_TOKEN` — Your Telegram Bot Token (from @BotFather)
* `MONGO_URI` — MongoDB Connection String
* `OWNER_ID` — Your Telegram User ID
* `SUDO_USERS` — Space-separated list of admin User IDs
* `LOG_CHANNEL` — Channel ID for logging tasks
* `DOWNLOAD_DIR` / `ENCODE_DIR` — Temporary paths for working directories

---

## 🚀 Deployment

### 💻 Local / VPS Execution

Ensure you have **Python 3.9+** and **FFmpeg** installed on your system.

1. Install required dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
2. Start the bot:
   ```bash
   python3 -m VideoEncoder
   ```

### 🐳 Docker

Deploy effortlessly using Docker containers:

1. Build the Docker image:
   ```bash
   docker build -t video-encoder .
   ```
2. Run the container:
   ```bash
   docker run -d --env-file config.env video-encoder
   ```

### ☁️ Heroku Deployment

> [!WARNING]
> If you are deploying this bot to Heroku, you **must** add the FFmpeg buildpack alongside the default Python buildpack. Without it, the bot will fail to process videos and throw a `Could not retrieve media streams` error.

1. Deploy the app from your GitHub repository or via Heroku CLI.
2. Navigate to your app's **Settings** tab in the Heroku Dashboard.
3. Scroll down to the **Buildpacks** section and click **Add buildpack**.
4. Paste the following URL and click Save:
   ```text
   https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
   ```
5. Verify that both `heroku/python` and the FFmpeg buildpack are listed.
6. Go to the **Deploy** tab and trigger a **new deployment** to apply the buildpacks.

---

## 📝 Important Notes

* **Task Limiting**: To ensure fair usage and prevent crashes, each user is strictly limited to one active encoding task at a time.
* **Settings Isolation**: User configurations are fully isolated. No one can overwrite another person's settings.

---

## 💼 Custom Modifications & Support

Need custom modifications, private features, or a personalized bot setup? 

💌 **DM the developer on Telegram:** [@cantarella_wuwa](https://t.me/cantarella_wuwa)

_Buy custom bots, advanced features, automation systems, Telegram CDN setups, encoding solutions, and more!_
