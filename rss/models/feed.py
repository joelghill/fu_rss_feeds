""" Module containing the Feed model and supporting classes
"""
from django.db import models

import feedparser

class Feed(models.Model):
    """ Model representing an RSS feed
    """
    url = models.URLField(max_length=200, blank=False, null=False)
    display_name = models.CharField(max_length=200, name='Name', blank=True)
    description = models.TextField(name='Description', blank=True)
    e_tag = models.CharField(max_length=200, name='ETag', blank=True, null=True)
    last_modified = models.DateTimeField(name='Last Modified', blank=True, null=True)

    raw_feed = models.TextField

    def update_feed(self):
        pass

