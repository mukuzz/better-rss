from django.core.management.base import BaseCommand
from betterRss.tasks import listFeeds

class Command(BaseCommand):
    help = 'Add new RSS Feed'

    def handle(self, *args, **options):
        try:
            listFeeds()
        except Exception as e:
            print(e)