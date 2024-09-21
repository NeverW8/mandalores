FROM ubuntu:latest

ENV PYTHONUNBUFFERED=1 \
    APP_HOME=/app

# Update package list and install required packages
RUN apt-get update && apt-get install -y \
    python3-full \
    python3-pip \
    python3-dev \
    libpq-dev \
    build-essential \
    wget \
    ffmpeg \
    && apt-get clean

# Install the latest yt-dlp binary
RUN wget -O /usr/local/bin/yt-dlp https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp \
    && chmod a+rx /usr/local/bin/yt-dlp

# Create application directory
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt $APP_HOME/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . $APP_HOME/

ENV FLASK_APP=app/app.py \
    FLASK_ENV=production

EXPOSE 5000
ENV PATH="/opt/venv/bin:$PATH"
CMD ["run_django.sh"]
