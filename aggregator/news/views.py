from django.shortcuts import render
from .models import Article, Feed
from .forms import FeedForm
from django.http import HttpResponseRedirect
from django.urls import reverse

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
                    feed_data = feedparser.parse(feed.url)
                    for entry in feed_data.entries:
                        article = Article()
                        article.title = entry.title
                        article.url = entry.link
                        article.description = entry.description

                        date_string = datetime.datetime.now()  # init the time to now in case published_parse=False
                        if entry.get('published_parse'):
                            d = datetime.datetime(*(entry.published_parsed[0:6]))
                            date_string = d.strftime('%Y-%m-%d %H:%M:%S')

                        article.publication_date = date_string
                        article.feed = existing_feed[0]
                        article.save()

                return HttpResponseRedirect(reverse('news:feeds_list'))

            if len(existing_feed) == 0:
                feed_data = feedparser.parse(feed.url)

                # return to the form if there is no error
                if not feed.get('title') and len(feed.entries) == 0:
                    form = FeedForm()
                    return render(request, 'news/new_feed.html', {'form': form})

                feed.title = feed_data.feed.title
                feed.save()

                for entry in feed_data.entries:
                    article = Article()
                    article.title = entry.title
                    article.url = entry.link
                    article.description = entry.description

                    d = datetime.datetime(*(entry.published_parsed[0:6]))
                    date_string = d.strftime('%Y-%m-%d %H:%M:%S')

                    article.publication_date = date_string
                    article.feed = feed
                    article.save()

            return HttpResponseRedirect(reverse('news:feeds_list'))
    else:
        form = FeedForm()
    return render(request, 'news/new_feed.html', {'form': form})
