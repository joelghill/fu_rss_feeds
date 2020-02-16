""" Module containing the Feed model and supporting classes
"""
from datetime import datetime
from time import mktime
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from .entry import FeedEntry
from .pen_name import PenName


class FeedImage(models.Model):
    """ Model used to describe an image for a feed
    """
    # Alt attribute
    title = models.CharField(max_length=200, blank=True)
    # Title attribute, rare
    description = models.TextField(blank=True, null=True)

    src = models.URLField(name='src', blank=True)
    link = models.URLField(name='image_link', blank=True)

    # Image properties
    width = models.IntegerField(editable=False)
    height = models.IntegerField(editable=False)

    @staticmethod
    def get_or_create(feed_image):
        """ Gets or creates a feed image instance
        :param feed_image: Object containing parameters for a feed image
        :type feed_image: dict
        :return: A new or found instance of a feed image
        :rtype: FeedImage
        """
        if feed_image is None:
            return None

        image, _ = FeedImage.objects.get_or_create(
            title=feed_image.get('title', None),
            description=feed_image.get('description', None),
            src=feed_image.get('link', None),
            width=feed_image.get('width', None),
            height=feed_image.get('height', None))

        return image


class Feed(models.Model):
    """ Model representing an RSS feed
    """
    # The location of the feed. Web URL or local filepath
    source = models.TextField(blank=False, null=False)

    feed_id = models.UUIDField(blank=True, null=True)
    title = models.TextField(blank=True)
    subtitle = models.TextField(blank=True)
    description = models.TextField(name='description', blank=True)
    license_link = models.URLField(name='license', blank=True)
    homepage = models.URLField(name='home', blank=True)
    published_date = models.DateTimeField(name='published', null=True)
    copyright_raw = models.TextField(name='copywrite', blank=True)

    icon = models.URLField(name='icon', blank=True)
    image = models.ForeignKey(FeedImage, name='Image', related_name='feed', null=True, on_delete=models.SET_NULL)
    logo = models.URLField(name='logo', blank=True)

    author = models.ForeignKey(PenName, related_name='feeds', null=True, on_delete=models.SET_NULL)
    publisher = models.ForeignKey(PenName, related_name='publications', null=True, on_delete=models.SET_NULL)
    contributors = models.ManyToManyField(PenName, blank=True, related_name='feed_contributions')

    etag = models.CharField(max_length=200, name='etag', blank=True, null=True, editable=False)
    last_modified = models.DateTimeField(blank=True, null=True, editable=False)

    def update(self, feed: dict, entries: list, modified=None, etag=None) -> None:
        """ Updates the feed with feed data, entries, last modified date, and etag

        :param feed: The feed data to apply to the feed
        :type feed: dict
        :param entries: List of entries to add to the feed
        :type entries: list
        :param modified: Last modified date string, defaults to None
        :type modified: str, optional
        :param etag: Most recent eTag of the feed, defaults to None
        :type etag: str, optional
        """

        if modified and self.last_modified != modified:
            self.last_modified = modified
        if etag and self.etag != etag:
            self.etag = etag

        self.update_feed(feed)
        self.update_entries(entries)

    def update_feed(self, raw_feed: dict):
        """ Updates the feed entry from raw feed data
        :param raw_feed: Raw feed data
        :type raw_feed: dict
        """
        self.feed_id = raw_feed.get('id', None)
        self.title = raw_feed.get('title', None)
        self.subtitle = raw_feed.get('subtitle', None)
        self.description = raw_feed.get('info', None)
        self.license_link = raw_feed.get('license', None)
        self.homepage = raw_feed.get('link', None)

        published_data = raw_feed.get('published_parsed', None)
        if published_data:
            self.published_date = datetime.fromtimestamp(mktime(published_data))

        self.copyright_raw = raw_feed.get('rights', None)

        self.icon = raw_feed.get('icon', None)
        self.image = FeedImage.get_or_create(raw_feed.get('image', None))
        self.logo = raw_feed.get('logo', None)

        author_detail = raw_feed.get('author_detail', None)
        if author_detail:
            self.author, _ = PenName.objects.get_or_create(name=author_detail['name'], email=author_detail['email'])

        publisher_detail = raw_feed.get('publisher_detail', None)
        if publisher_detail:
            self.publisher, _ = PenName.objects.get_or_create(
                name=publisher_detail['name'],
                email=publisher_detail['email'])

        contributors = raw_feed.get('contributors', None)
        if contributors:
            for contributor_detail in contributors:
                contributor, _ = PenName.objects.get_or_create(
                    name=contributor_detail['name'],
                    email=contributor_detail['email'])

                if contributor not in self.contributors:
                    self.contributors.add(contributor)

    def update_entries(self, raw_entries: list) -> None:
        """ Adds entries that have not yet been associated with this feed

        :param raw_entries: A list of entries to add to the feed
        :type raw_entries: list
        """
        latest_entry = self.entries.order_by('-published').first()
        latest_published_date = latest_entry.published if latest_entry else None
        for raw_entry in raw_entries:

            published_data = raw_entry.get('published_parsed', None)
            published_datetime = datetime.fromtimestamp(mktime(published_data), tz=timezone.get_current_timezone())

            # If the latest entry exists and has a greater published date then stop adding entries
            if latest_entry and published_datetime and published_datetime <= latest_published_date:
                break

            raw_title = raw_entry.get('title', None)
            try:
                FeedEntry.objects.get(source=self, title=raw_title)
                break
            except ObjectDoesNotExist:
                FeedEntry.from_parsed(self, raw_entry)
