from django.db import models
from  django.utils import timezone

class RssFeed(models.Model):
    title = models.CharField(max_length=256)
    url = models.CharField(max_length=512)
    description = models.CharField(max_length=512)
    feed_url = models.CharField(max_length=512)
    should_update_summary = models.BooleanField(default=True)
    nick_name = models.CharField(max_length=16)
    refresh_interval_minutes = models.IntegerField(default=60)
    last_update = models.DateTimeField(default=timezone.make_aware(timezone.datetime(1999,12,31)))

    def __str__(self):
        return self.url


class RssItem(models.Model):
    rss_feed = models.ForeignKey(RssFeed, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    link = models.CharField(max_length=512)
    published = models.CharField(max_length=128)
    image = models.CharField(max_length=512)
    summary = models.CharField(max_length=2048)
    nlp_summary = models.CharField(max_length=2048)
    author = models.CharField(max_length=512)
    save_date = models.DateTimeField(default=timezone.now)
        
    def __str__(self):
        return self.link