import subprocess
from video_content.models import VideoContent
from django.conf import settings


# def convert_480p(source):
#     target = source + '480p.mp4'
    

def convert720p(source):
    new_file_name = source + '_720p.mp4'
    ffmpeg_path = settings.FFMPEG_PATH
    cmd = f'"{ffmpeg_path}" -i "{source}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{new_file_name}"'
    run = subprocess.run(cmd, capture_output=True)

    if run.returncode != 0:
        print("Fehler beim Konvertieren des Videos: ", run.stderr)
    else:
        print("Video erfolgreich konvertiert: ", new_file_name)


def convert480p(source):
    new_file_name = source + '_480p.mp4'
    ffmpeg_path = settings.FFMPEG_PATH
    # Ändern der Auflösungseinstellung von 'hd720' zu '852x480' für 480p
    cmd = f'"{ffmpeg_path}" -i "{source}" -s 852x480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{new_file_name}"'
    run = subprocess.run(cmd, capture_output=True)

    if run.returncode != 0:
        print("Fehler beim Konvertieren des Videos: ", run.stderr)
    else:
        print("Video erfolgreich konvertiert: ", new_file_name)