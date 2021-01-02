from django.http import StreamingHttpResponse, HttpResponse
from django.template.loader import render_to_string
from django.db import models
import feedparser
from newspaper import Article
from urllib.parse import urlsplit

from .models import RssItem

def get_feed(request, feed):
    url_without_target = f'{request.scheme}://{request.get_host()}/feed/'
    feed = request.build_absolute_uri()[len(url_without_target):]
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
            "title": get_dict_item_safe(data.feed,'title'),
            "url": link,
            "description": get_dict_item_safe(data.feed,'description'),
        }
        yield render_to_string('betterRss/rss_header.html', context)
        
        for entry in entries:
            item_link = get_dict_item_safe(entry,'link')
            rss_item = RssItem.objects.filter(link=item_link).first()
            if rss_item == None:
                # Save new rss item to db
                try:
                    article = Article(item_link)
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
                        title=get_dict_item_safe(entry,'title'),
                        link=item_link,
                        published=get_dict_item_safe(entry,'published'),
                        image=image,
                        summary=get_dict_item_safe(entry,'summary'),
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

def get_dict_item_safe(dict, attr):
    try:
        return dict[attr]
    except KeyError:
        return ""