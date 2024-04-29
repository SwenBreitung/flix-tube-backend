from rest_framework import viewsets, serializers
from .models import VideoContent

class Video_contentSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = VideoContent
        fields = ['title', 'description', 'video','video_image' ]
        read_only_fields = ['created_at'] 

    def create(self, validated_data):
        print('serilazer',self,validated_data)
        # Erstellt eine neue VideoContent-Instanz mit den validierten Daten
        video_content = VideoContent.objects.create(
            title=validated_data['title'],
            description=validated_data.get('description', ''),  # Optional mit Standardwert ''
            video = validated_data.get('video', None),
            video_image = validated_data.get('video_image', None)
        )
        video_content.save()
        
        return video_content