from rest_framework import viewsets, serializers
from .models import VideoContent
import os
from moviepy.editor import VideoFileClip
import tempfile
import shutil
from PIL import Image
import subprocess
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import datetime
class Video_contentSerializer(serializers.ModelSerializer):


    def create_thumbnail(video_file):
        # thumb_dir = 'media/video_imgs'  # Stelle sicher, dass dieser Ordner existiert
        # if not os.path.exists(thumb_dir):
        #     os.makedirs(thumb_dir)
        # clip = VideoFileClip(video_path)
        # frame = clip.get_frame(clip.duration / 2)
        # image = Image.fromarray(frame)
        # thumb_path = os.path.join(thumb_dir, os.path.basename(video_path) + '_video_imgs.jpg')
        # image.save(thumb_path)
        # return thumb_path 
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
            for chunk in video_file.chunks():
                temp_video.write(chunk)
        temp_video_path = temp_video.name  # Speichere den Pfad der temporären Datei

    # Benutze diesen temporären Pfad, um das Thumbnail zu erstellen
        try:
            # thumb_dir = 'media/video_imgs'  # Stelle sicher, dass dieser Ordner existiert
            # if not os.path.exists(thumb_dir):
            #     os.makedirs(thumb_dir)
        
            clip = VideoFileClip(temp_video_path)
            frame = clip.get_frame(clip.duration / 2)
            clip.close()  
            thumb_dir = 'media/video_imgs'
            if not os.path.exists(thumb_dir):
                os.makedirs(thumb_dir)
            image = Image.fromarray(frame)
            thumb_path = os.path.join(thumb_dir, os.path.basename(temp_video_path) + '_thumbnail.jpg')
            image.save(thumb_path)
            return thumb_path
        finally:
            os.unlink(temp_video_path) 

    def create_gif(self, video_path, output_gif_path):
        cmd = [
            'ffmpeg',
            '-ss', '10',  # Start 10 Sekunden ins Video
            '-t', '5',    # Dauer: 5 Sekunden (für 5 Frames bei 1 fps)
            '-i', video_path,
            '-vf', 'fps=1,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse',
            '-loop', '0',
        output_gif_path
        ]
        subprocess.run(cmd, text=True)

# Beispielaufruf der Funktion
# 
        
    class Meta:
        model = VideoContent
        fields = ['title', 'description', 'video','video_image' ]
        read_only_fields = ['created_at'] 

    def create(self, validated_data):
        video_file = validated_data.get('video')
        print('video_file.path',video_file)
        print("vor erste 1 if abfrage!!!!!!!!!!!",validated_data)
        # Temporären Pfad für das hochgeladene Video generieren
        temp_path = default_storage.save('tmp/some_prefix_' + video_file.name, ContentFile(video_file.read()))
        full_temp_path = os.path.join(default_storage.location, temp_path)
        print('full_temp_path',full_temp_path)
        # Erstelle einen einzigartigen Dateinamen basierend auf der aktuellen Zeit
        # Beispielname des Videos: "example_video.mp4"
        base_name = os.path.splitext(video_file.name)[0]  # Entfernt die Dateierweiterung
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  
        output_gif_path = os.path.join('media/video_gifs', f'{timestamp}_{base_name}.gif')
        
        print('output_gif_path',output_gif_path)
        # Hier würdest du deine Funktionen aufrufen, um das GIF zu erstellen
        
        if not validated_data.get('video_image'):
                print("zweite 2 if abfrage")
                thumbnail_path = self.__class__.create_thumbnail(video_file)
                print("zweite 2 if abfrage",thumbnail_path)
                validated_data['video_image'] = thumbnail_path
        # self.create_gif_directly('path/to/your/video.mp4', 'path/to/your/output.gif')
        self.create_gif(full_temp_path, output_gif_path)
        video_content = VideoContent.objects.create(
            title=validated_data['title'],
            description=validated_data.get('description', ''),  # Optional mit Standardwert ''
            video = validated_data.get('video', None),
            video_image = validated_data.get('video_image', None)
        )
        
        # Temporäre Datei löschen
        os.remove(full_temp_path)
        default_storage.delete(temp_path)
        
        video_content.save()
        
        return video_content
    
    