from django.test import TestCase

from rss.models.feed import Feed


class InitFeedTestCase(TestCase):

    def test_init_feed(self):
        feed = Feed.objects.create()