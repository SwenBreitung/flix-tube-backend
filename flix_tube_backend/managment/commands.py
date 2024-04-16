from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Deletes guest users that are older than a specified age'

    def handle(self, *args, **options):
        expiration_days = 7  
        threshold_date = timezone.now() - timedelta(days=expiration_days)

        
        old_guest_users = User.objects.filter(username__startswith='guest_', date_joined__lt=threshold_date)
        count = old_guest_users.count()
        old_guest_users.delete()

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} old guest user(s).'))