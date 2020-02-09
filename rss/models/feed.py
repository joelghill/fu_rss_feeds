""" Module containing the Feed model and supporting classes
"""
from django.db import models
from web_presence.models import WebIdentity

import feedparser

class FeedImage(models.Model):
    """ Model used to describe an image for a feed
    """
    # Alt attribute
    title = models.CharField(max_length=200, blank=True)
    # Title attribute, rare
    description = models.TextField()

    src = models.URLField(name='Source', blank=True)
    link = models.URLField(name='Image Link', blank=True)

    # Image properties
    width = models.IntegerField(editable=False)
    height = models.IntegerField(editable=False)


class Feed(models.Model):
    """ Model representing an RSS feed
    """
    # The location of the feed. Web URL or local filepath
    source = models.CharField(max_length=200, blank=False, null=False)

    feed_id = models.UUIDField(blank=True, null=True)
    title = models.CharField(max_length=100, blank=True)
    subtitle = models.CharField(max_length=200, blank=True)
    display_name = models.CharField(max_length=200, name='Name', blank=True)
    description = models.TextField(name='Description', blank=True)
    license_link = models.URLField(name='License', blank=True)
    homepage = models.URLField(name='Home', blank=True)
    published_date = models.DateTimeField(name='Published')
    copyright_raw = models.TextField(name='Copywrite', blank=True)

    icon = models.URLField(name='Icon', blank=True)
    image = models.ForeignKey(FeedImage, name='Image', related_name='feed', on_delete=models.SET_NULL)
    logo = models.URLField(name='Logo', blank=True)


    author = models.ForeignKey(WebIdentity, related_name='feeds', on_delete=models.SET_NULL)
    publisher = models.ForeignKey(WebIdentity, related_name='publications', on_delete=models.SET_NULL)
    contributors = models.ManyToManyField(WebIdentity, blank=True, null=True, related_name='feed_contributions')

    e_tag = models.CharField(max_length=200, name='ETag', blank=True, null=True, editable=False)
    last_modified = models.DateTimeField(name='Last Modified', blank=True, null=True, editable=False)

    def update_feed(self):
        

