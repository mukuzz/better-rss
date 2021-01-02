from django.db import models
from  django.utils import timezone

class RssItem(models.Model):
    title = models.CharField(max_length=256)
    link = models.CharField(db_index=True, max_length=512)
    published = models.CharField(max_length=128)
    image = models.CharField(max_length=512)
    summary = models.CharField(max_length=2048)
    author = models.CharField(max_length=512)
    
    def __str__(self):
        return self.link