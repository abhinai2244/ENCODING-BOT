FROM python:3.9.2-slim-buster
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ="Asia/Kolkata"

# Install dependencies
RUN apt-get -qq update && \
    apt-get -qq install -y git ffmpeg mediainfo build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY . .

# Install Python dependencies
RUN python3 -m pip install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python3", "-m", "VideoEncoder"]
