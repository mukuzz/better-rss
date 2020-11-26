from django.core.management.base import BaseCommand
from betterRss.tasks import refresh_feeds

class Command(BaseCommand):
    help = 'Refresh all feeds'

    def handle(self, *args, **options):
        try:
            refresh_feeds()
        except Exception as e:
            print(e)