from django.db import models
from .models import RssFeed, RssItem
import feedparser
from newspaper import Article
from  django.utils import timezone
from urllib.parse import urlsplit


def addFeed():
    try:
        url = str(input("Enter feed url: "))
        nick_name = str(input("Enter short name: "))
        refresh_interval = int(input("Enter the refresh interval in minutes: "))
        should_update_summary = bool(input("Should update summary(Leave empty for yes): "))
        if not should_update_summary:
            should_update_summary = True
            print("Summary will be appended to feed articles")
        else:
            should_update_summary = False
            print("Summary will NOT be appended to feed articles")
        data = feedparser.parse(url)
        split_url = urlsplit(data.feed.link)
        link = f'{split_url.scheme}://{split_url.netloc}'
        rss_feed = RssFeed()
        rss_feed.title = data.feed.title
        rss_feed.url = link
        rss_feed.feed_url = url
        rss_feed.description = data.feed.description
        rss_feed.should_update_summary = should_update_summary
        rss_feed.nick_name = nick_name
        rss_feed.refresh_interval_minutes = refresh_interval
        rss_feed.save()
    except Exception as e:
        print(e)


def removeFeed():
    try:
        nick_name = str(input("Enter short name of feed to delete: "))
        print(RssFeed.objects.filter(nick_name=nick_name).delete())
    except Exception as e:
        print(e)


def listFeeds():
    try:
        feeds = RssFeed.objects.all()
        for i, feed in enumerate(feeds):
            print(f'{i+1}. {feed.url} ({feed.nick_name})')
    except Exception as e:
        print(e)


def refresh_feeds():
    feeds = RssFeed.objects.all()
    for feed in feeds:
        if timezone.timedelta(minutes=feed.refresh_interval_minutes) + feed.last_update > timezone.now():
            print(f'Refresh interval({feed.refresh_interval_minutes} min) not reached:', feed.feed_url, "| Last refresh:", feed.last_update)
            continue
        
        print("Refreshing:", feed.feed_url)
        url = feed.feed_url
        should_update_summary = feed.should_update_summary
        try:
            savedRssItemUrls = [item.link for item in RssItem.objects.filter(rss_feed__feed_url=url)]
            data = feedparser.parse(url)
            entries = data.entries
            for entry in entries:
                try:
                    if entry.link in savedRssItemUrls:
                        continue
                    article = Article(entry.link)
                    image = ""
                    nlp_summary = ""
                    authors = []
                    try:
                        article.download()
                        article.parse()
                        image = article.top_image
                        if should_update_summary:
                            article.nlp()
                            nlp_summary = article.summary
                        if feed.nick_name != "hn":
                            authors = article.authors
                    except Exception as e:
                        print(e)
                    finally:
                        try:
                            authors = [entry.author]
                        except AttributeError:
                            pass
                        rss_item = RssItem(
                            rss_feed=feed,
                            title=entry.title,
                            link=entry.link,
                            published=entry.published,
                            image=image,
                            summary=entry.summary,
                            nlp_summary=nlp_summary,
                            author=', '.join([a.strip() for a in authors]),
                        )
                        rss_item.save()
                        print("Added:", entry.link)
                except Exception as e:
                    print(e)
            feed.last_update = timezone.now()
            feed.save()
        except Exception as e:
            print(e)
    clear_old_feed_items()


# Remove articles older than 48 hours
def clear_old_feed_items():
    try:
        expiry = timezone.now() - timezone.timedelta(hours=48)
        deleted_items = RssItem.objects.filter(save_date__lt=expiry).delete()
        print(f'{deleted_items[0]} articles older than 48 hours purged')
    except Exception as e:
        print(e)
