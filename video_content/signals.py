import logging
from django_rq import enqueue
import django_rq
from video_content.tasks import convert720p
from video_content.tasks import convert480p

from .models import VideoContent
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

import os
logger = logging.getLogger(__name__)


@receiver(post_save, sender = VideoContent)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        print('New object created')
        queue = django_rq.get_queue('default', autocommit = True)
        queue.enqueue(convert720p, instance.video.path, instance.id)
        queue.enqueue(convert480p, instance.video.path, instance.id)
        # convert720p(instance.video.path)
    else:
        #bei update, funktion muss noch geschrieben werden 
        print('Object updated')
        
        
def auto_file_delete(sender, instance, **kwargs):
    if hasattr(instance, 'video') and instance.video:
        try:
            instance.video.delete(save=False)
            logger.info(f'Video-Datei für {instance} wurde erfolgreich gelöscht.')
        except Exception as e:
            logger.error(f'Fehler beim Löschen der Video-Datei für {instance}: {e}')
                    

