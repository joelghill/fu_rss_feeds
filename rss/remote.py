""" Module containing classes used to update app feed records
"""
import feedparser
from rss.models import Feed


class FeedUpdater:
    """ Class used to update feeds
    """

    @staticmethod
    def update_from_source(feed: Feed) -> None:
        """ Updates a feed and its entries from the feed source
        
        :param feed: The feed to update from source
        :type feed: Feed
        """
        response = feedparser.parse(feed.source, etag=feed.etag, modified=feed.last_modified)

        if response.status == 304:
            return

        feed.update(response.feed, response.entries, response.get('etag', None), response.get('modified', None))
