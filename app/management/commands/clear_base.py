from django.contrib.auth.models import User

from app.models import Tag, BestUser, Profile
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Clear the base'

    def handle(self, *args, **kwargs):
        Tag.objects.all().delete()
        BestUser.objects.all().delete()
        User.objects.exclude(username='vvlad').delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared the base'))
