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


"""
Signal receiver that triggers after a VideoContent instance is saved.
- If the instance is newly created, it enqueues video conversion tasks for 720p and 480p formats using RQ (Redis Queue).
- If the instance is updated, no conversion is triggered, and a message is printed instead.
:param sender: The model class that triggered the signal (VideoContent).
:param instance: The actual instance of VideoContent that was saved.
:param created: Boolean indicating if the instance was created (True) or updated (False).
:param kwargs: Additional keyword arguments.
"""
@receiver(post_save, sender = VideoContent)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        queue = django_rq.get_queue('default', autocommit = True)
        queue.enqueue(convert720p, instance.video.path, instance.id)
        queue.enqueue(convert480p, instance.video.path, instance.id)
    else:
        print('Object updated')


"""
Automatically deletes the video file associated with a model instance when the instance is deleted.

- If the instance has a video file, the file is deleted from the storage system.
- Logs the success or failure of the file deletion.

:param sender: The model class that triggered the signal.
:param instance: The instance of the model that is being deleted.
:param kwargs: Additional keyword arguments.
"""
def auto_file_delete(sender, instance, **kwargs):
    if hasattr(instance, 'video') and instance.video:
        try:
            instance.video.delete(save=False)
            logger.info(f'Video-Datei für {instance} wurde erfolgreich gelöscht.')
        except Exception as e:
            logger.error(f'Fehler beim Löschen der Video-Datei für {instance}: {e}')