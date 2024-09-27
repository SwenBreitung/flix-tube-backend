import subprocess
from video_content.models import VideoContent
from django.conf import settings


"""
Converts a video to 720p resolution using FFmpeg.

- The function processes the given video file with FFmpeg to convert it to 720p resolution
    and saves the output as a new file with the suffix '_720p.mp4'.
- If the conversion is successful, a success message is printed. If it fails, an error message is printed.

:param source: The file path of the video to be converted.
:return: None. The function prints the success or failure of the video conversion.
"""
def convert720p(source):
    new_file_name = source + '_720p.mp4'
    ffmpeg_path = settings.FFMPEG_PATH
    cmd = f'"{ffmpeg_path}" -i "{source}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{new_file_name}"'
    run = subprocess.run(cmd, capture_output=True)

    if run.returncode != 0:
        print("Fehler beim Konvertieren des Videos: ", run.stderr)
    else:
        print("Video erfolgreich konvertiert: ", new_file_name)


"""
Converts a video to 480p resolution using FFmpeg.

- The function takes a video file, processes it with FFmpeg to convert it to 480p resolution,
    and saves the output as a new file with the suffix '_480p.mp4'.
- If the conversion is successful, it prints a success message. If it fails, an error message is printed.

:param source: The file path of the video to be converted.
:return: None. The function prints the success or failure of the video conversion.
"""
def convert480p(source):
    new_file_name = source + '_480p.mp4'
    ffmpeg_path = settings.FFMPEG_PATH
    cmd = f'"{ffmpeg_path}" -i "{source}" -s 852x480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{new_file_name}"'
    run = subprocess.run(cmd, capture_output=True)

    if run.returncode != 0:
        print("Fehler beim Konvertieren des Videos: ", run.stderr)
    else:
        print("Video erfolgreich konvertiert: ", new_file_name)