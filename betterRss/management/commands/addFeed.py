from django.core.management.base import BaseCommand
from betterRss.tasks import addFeed

class Command(BaseCommand):
    help = 'Add new RSS Feed'

    def handle(self, *args, **options):
        try:
            addFeed()
        except Exception as e:
            print(e)