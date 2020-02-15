""" Module containing the Feed model and supporting classes
"""
from datetime import datetime
from time import mktime
from django.db import models
import feedparser

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

    def update(self) -> None:
        """ Queries the feed source and updates the feed and feed entries
        """

        response = feedparser.parse(self.source, etag=self.etag, modified=self.last_modified)

        if response.status == 304:
            print("No changes")
            return

        if hasattr(response, 'modified') and response.modified:
            self.last_modified = response.modified
        if hasattr(response, 'etag') and response.etag:
            self.etag = response.etag

        self.feed_id = response.feed.get('id', None)
        self.title = response.feed.get('title', None)
        self.subtitle = response.feed.get('subtitle', None)
        self.description = response.feed.get('info', None)
        self.license_link = response.feed.get('license', None)
        self.homepage = response.feed.get('link', None)

        published_data = response.feed.get('published_parsed', None)
        if published_data:
            self.published_date = datetime.fromtimestamp(mktime(published_data))

        self.copyright_raw = response.feed.get('rights', None)

        self.icon = response.feed.get('icon', None)
        self.image = FeedImage.get_or_create(response.feed.get('image', None))
        self.logo = response.feed.get('logo', None)

        author_detail = response.feed.get('author_detail', None)
        if author_detail:
            self.author, _ = PenName.objects.get_or_create(name=author_detail['name'], email=author_detail['email'])

        publisher_detail = response.feed.get('publisher_detail', None)
        if publisher_detail:
            self.publisher, _ = PenName.objects.get_or_create(
                name=publisher_detail['name'],
                email=publisher_detail['email'])

        contributors = response.feed.get('contributors', None)
        if contributors:
            for contributor_detail in contributors:
                contributor, _ = PenName.objects.get_or_create(
                    name=contributor_detail['name'],
                    email=contributor_detail['email'])

                if contributor not in self.contributors:
                    self.contributors.add(contributor)

        self.update_entries(response.entries)


    def update_entries(self, raw_entries):
        for raw_entry in raw_entries:
            entry = FeedEntry.from_parsed(self, raw_entry)
            entry.save()
