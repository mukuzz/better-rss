from django.core.management.base import BaseCommand
from betterRss.tasks import removeFeed

class Command(BaseCommand):
    help = 'Add new RSS Feed'

    def handle(self, *args, **options):
        try:
            removeFeed()
        except Exception as e:
            print(e)