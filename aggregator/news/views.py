from django.shortcuts import render
from .models import Article, Feed
from .forms import FeedForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

import feedparser
import datetime

# Create your views here.


def articles_list(request):
    """Get the list of the article"""
    articles = Article.objects.all()

    rows = [articles[x:x+1] for x in range(0, len(articles), 1)]

    return render(request, 'news/articles_list.html', {'rows': rows})


def feeds_list(request):
    feeds = Feed.objects.all()
    return render(request, 'news/feeds_list.html', {'feeds': feeds})


def get_entries(url):
    feed_data = feedparser.parse(url)

    if feed_data.get("entries"):
        return feed_data.get("entries")
    return []


def get_title(url):
    feed_data = feedparser.parse(url)

    return feed_data.get("title")


def create_new_entry(feed, url):
    entries = get_entries(url)
    for entry in entries:
        date_string = timezone.now()  # init the time to now in case published_parse=False
        if entry.get('published_parse'):
            d = datetime.datetime(*(entry.published_parsed[0:6]))
            date_string = d.strftime('%Y-%m-%d %H:%M:%S')

        Article.objects.create(title=entry.get('title'),
                               url=entry.get('link'),
                               description=entry.get('description'),
                               publication_date=date_string,
                               feed=feed)
    return True


def new_feed(request):
    if request.method == "POST":
        form = FeedForm(request.POST)
        if form.is_valid():
            # get the url from the form
            feed = form.save(commit=False)

            # check if there is an existing feed with this url
            existing_feed = Feed.objects.filter(url=feed.url)
            if len(existing_feed) > 0:
                existing_feed_entries = Article.objects.filter(feed=existing_feed[0])
                if len(existing_feed_entries) == 0:
                    create_new_entry(existing_feed[0], existing_feed[0].url)
                return HttpResponseRedirect(reverse('news:feeds_list'))

            if len(existing_feed) == 0:

                # return to the form if there is an error
                get_tit = get_title(feed.url)
                if not get_tit:
                    form = FeedForm()
                    return render(request, 'news/new_feed.html', {'form': form})

                feed.title = get_tit
                feed.save()
                create_new_entry(feed, feed.url)

            return HttpResponseRedirect(reverse('news:feeds_list'))
    else:
        form = FeedForm()
    return render(request, 'news/new_feed.html', {'form': form})
