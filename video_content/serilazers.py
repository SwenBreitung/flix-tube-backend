from rest_framework import viewsets, serializers
from .models import VideoContent

class Video_contentSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = VideoContent
        fields = ['title', 'description', 'created_at', 'video', 'updated_at']
        extra_kwargs = {'password': {'write_only': True}}
        

    def create(self, validated_data):
        # Erstellt eine neue VideoContent-Instanz mit den validierten Daten
        video_content = VideoContent.objects.create(
            title=validated_data['title'],
            description=validated_data.get('description', ''),  # Optional mit Standardwert ''
            video=validated_data['video']
        )
        video_content.save()
        
        return video_content