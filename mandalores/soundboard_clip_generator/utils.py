import os
import subprocess
import requests

from background_task import background
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from mandalores.soundboard_clip_generator.models import SoundClip

def verifyURL(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ValueError("Invalid URL {e}")


@background(schedule=10)
def downloadClip(clip_id: int):
    clip = SoundClip.objects.get(id=clip_id)
    verifyURL(clip.url)

    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    file_path = os.path.join(settings.MEDIA_ROOT, f"soundclip_{clip.id}.mp3")

    command = [
        "yt-dlp", "-v", "-x", "--audio-format", "mp3",
        "--postprocessor-args", f"-ss {clip.start_time} -to {clip.stop_time}",
        "-o", file_path, clip.url
    ]
    # Create the temp file but close it so yt-dlp can write to it
    try:
        subprocess.run(command, capture_output=True, text=True, check=True)

        with NamedTemporaryFile(dir=settings.MEDIA_ROOT) as temp_file:
            with open(file_path, 'rb') as output_file:
                temp_file.write(output_file.read())

            clip.status = SoundClip.COMPLETED_STATUS
            clip.file.save(f"soundclip_{clip.id}.mp3", File(temp_file))
            clip.save()
    except subprocess.CalledProcessError as e:
        print(e)
        print(e.stdout)
        print(e.stderr)
        clip.status = SoundClip.FAILED_STATUS
        clip.save()
        raise e
    finally:
            os.unlink(file_path)


def generate_clip(clip_id):
    clip = SoundClip.query.get(id=clip_id)

    try:
        downloadClip(clip)
    except Exception as e:
        clip.status = SoundClip.FAILED_STATUS
        clip.save()
