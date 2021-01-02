from django.http import StreamingHttpResponse, HttpResponse
from django.template.loader import render_to_string
from django.db import models
import feedparser
from newspaper import Article
from urllib.parse import urlsplit

from .models import RssItem

def get_feed(request):
    feed = request.GET.get('feedUrl', None)
    return StreamingHttpResponse(
        stream_feed(feed),
        content_type="application/rss+xml; charset=utf-8",
    )

def stream_feed(feed):
    try:
        data = feedparser.parse(feed)
        entries = data.entries

        # Stream the feed header
        split_url = urlsplit(feed)
        link = f'{split_url.scheme}://{split_url.netloc}'
        context = {
            "title": data.feed.title,
            "url": link,
            "description": data.feed.description
        }
        yield render_to_string('betterRss/rss_header.html', context)
        
        for entry in entries:
            rss_item = RssItem.objects.filter(link=entry.link).first()
            if rss_item == None:
                # Save new rss item to db
                article = Article(entry.link)
                try:
                    article.download()
                    article.parse()
                    image = article.top_image
                    authors = article.authors
                except Exception as e:
                    print(e)
                finally:
                    try:
                        authors = [entry.author]
                    except AttributeError:
                        pass
                    rss_item = RssItem(
                        title=entry.title,
                        link=entry.link,
                        published=entry.published,
                        image=image,
                        summary=entry.summary,
                        author=', '.join([a.strip() for a in authors]),
                    )
                    rss_item.save()
            # stream the rss item
            yield render_to_string('betterRss/rss_item.html', {'item': rss_item})
        # Stream the rss feed footer
        yield render_to_string('betterRss/rss_footer.html')
    except Exception as e:
        print(e)
        yield ""

def clear_saved_rss_items(request):
    RssItem.objects.all().delete()
    return HttpResponse()