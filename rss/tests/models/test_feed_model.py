""" Module containing tests for the feed model
"""
from django.test import TestCase
from rss.models.feed import Feed
from rss.remote import FeedUpdater


class InitFeedTestCase(TestCase):
    """ Basic initialization test case
    """

    def test_init_feed(self):
        """ Create a feed instance and verify correct initialization
        """
        feed = Feed.objects.create(source='rss/tests/fixtures/xkcd_feed.xml')
        self.assertIsNotNone(feed)

    def test_first_time_update_feed(self):
        """ Create a feed instance and verify correct initialization
        """
        feed = Feed.objects.create(source='https://www.penny-arcade.com/feed')
        self.assertIsNotNone(feed)

    def test_fu_politics_update_feed(self):
        """ Create a feed instance and verify correct initialization
        """
        feed = Feed.objects.create(source='https://feed.podbean.com/fupolitics/feed.xml')
        FeedUpdater.update_from_source(feed)

        count = feed.entries.count()
        FeedUpdater.update_from_source(feed)
        self.assertEqual(count, feed.entries.count())
