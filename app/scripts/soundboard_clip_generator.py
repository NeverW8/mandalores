import requests
import subprocess
from app.models import SoundClip
from app import db
import os


def verifyURL(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Invalid URL: {e}")
        raise ValueError("Invalid URL")


def verifyTimeRange(startTime, stopTime):
    if len(startTime) != 8 or len(stopTime) != 8:
        print("Invalid time range")
        raise ValueError("Invalid time range")

    for i in range(0, 8):
        if i == 2 or i == 5:
            if startTime[i] != ":" or stopTime[i] != ":":
                print("Invalid time range")
                raise ValueError("Invalid time range")
        else:
            if not startTime[i].isdigit() or not stopTime[i].isdigit():
                print("Invalid time range")
                raise ValueError("Invalid time range")


def downloadClip(url, startTime, stopTime, clip_id):
    verifyURL(url)
    verifyTimeRange(startTime, stopTime)

    media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'media')
    os.makedirs(media_dir, exist_ok=True)

    file_path = os.path.join(media_dir, f"soundclip_{clip_id}.mp3")
    command = [
        "yt-dlp", "-x", "--audio-format", "mp3",
        "--postprocessor-args", f"-ss {startTime} -to {stopTime}",
        "-o", file_path, url
    ]

    try:
        subprocess.run(command, capture_output=True, text=True, check=True)
        clip = SoundClip.query.get(clip_id)
        if clip is None:
            print(f"No clip found with ID: {clip_id}")
            return

        clip.status = 'Completed'
        clip.file_path = file_path
        db.session.commit()
    except subprocess.CalledProcessError as e:
        clip = SoundClip.query.get(clip_id)
        if clip is None:
            print(f"No clip found with ID: {clip_id}")
            return

        clip.status = 'Failed'
        db.session.commit()
        print(f"Error downloading clip: {e.stderr}")
        raise e
