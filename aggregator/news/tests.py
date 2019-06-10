import uuid
from django.test import TestCase
from unittest import mock
from django.urls import reverse
from .models import Article, Feed


def get_entries_mock(url):
    entries = [
        {
            'title': 'Title 1',
            'link': 'test.com/1',
            'description': 'Description 1',
         },

        {
            'title': 'Title 1',
            'link': 'test.com/1',
            'description': 'Description 1',
        }
    ]
    return entries


def get_title_mock(url):

    return "Test Title"


class TestCaseNews(TestCase):

    def setUp(self):
        self.feed = Feed.objects.create(id=uuid.uuid4(), title="Test Blog",
                                        url="test.com",
                                        is_active=True)

    @mock.patch('news.views.get_entries', get_entries_mock)
    @mock.patch('news.views.get_title', get_title_mock)
    def test_article_list(self):
        url = reverse('news:feed_new')
        data = {
            'url': 'http://test.com'
        }

        # Article.refresh_from_db()
        self.client.post(url, data)
        test_feed = Article.objects.count()
        self.assertEqual(test_feed, 2)
        # add assertion in this space and also create more test.
