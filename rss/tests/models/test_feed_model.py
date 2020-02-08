""" Module containing tests for the feed model
"""
from django.test import TestCase
from rss.models.feed import Feed


class InitFeedTestCase(TestCase):
    """ Basic initialization test case
    """

    def test_init_feed(self):
        """ Create a feed instance and verify correct initialization
        """
        feed = Feed.objects.create(url='https://www.xkcd.com/rss.xml')
        self.assertIsNotNone(feed)
