from django.shortcuts import render
from django.http import HttpResponseServerError, HttpResponseNotFound
from django.template.loader import render_to_string
from django.db import models

from .models import RssFeed, RssItem

def get_feed(request, feed):
    try:
        feedObj = RssFeed.objects.get(nick_name=feed)
    except RssFeed.DoesNotExist:
        return HttpResponseNotFound()
    except Exception as e:
        print(e)
        return HttpResponseServerError()
    try:
        feedItems = RssItem.objects.filter(rss_feed__feed_url=feedObj.feed_url)
        context = {
            "title": feedObj.title,
            "url": feedObj.url,
            "description": feedObj.description,
            "items": feedItems
        }
        return render(request, 'betterRss/rss.html', context, content_type="application/rss+xml; charset=utf-8")
    except Exception as e:
        print(e)
        return HttpResponseServerError()