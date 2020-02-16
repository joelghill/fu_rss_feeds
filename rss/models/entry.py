""" Module containing the Pen Name model and supporting code
"""
from datetime import datetime
from time import mktime

from django.db import models

from .pen_name import PenName


class FeedEntry(models.Model):
    """ A model represeting an individual entry to a feed
    """
    # The location of the feed. Web URL or local filepath
    source = models.ForeignKey('Feed', on_delete=models.CASCADE, related_name='entries')
    title = models.TextField(blank=True)
    entry_id = models.TextField(blank=True, null=True)

    author = models.ForeignKey(PenName, related_name='entries', null=True, on_delete=models.SET_NULL)
    publisher = models.ForeignKey(PenName, related_name='entry_publications', null=True, on_delete=models.SET_NULL)
    contributors = models.ManyToManyField(PenName, blank=True, related_name='entry_contributions')

    link = models.URLField(name='link', blank=True)
    license = models.URLField(name='license', blank=True, null=True)

    published = models.DateTimeField(name='published', null=True)
    created = models.DateTimeField(name='created', null=True)
    updated = models.DateTimeField(name='updated', null=True)

    comments = models.URLField(name='comments', blank=True)

    class Meta:
        unique_together = [['title', 'source']]

    @staticmethod
    def from_parsed(parsed_entry: dict):
        """ Generates a feed entry with the provided data

        :param parsed_entry: Parsed entry data
        :type parsed_entry: dict
        :return: A newly instantiated instance of a FeedEntry
        :rtype: FeedEntry
        """
        title = parsed_entry.get('title', None)
        entry = FeedEntry(title=title)

        entry.entry_id = parsed_entry.get('id', None)

        author_detail = parsed_entry.get('author_detail', None)
        if author_detail:
            entry.author, _ = PenName.objects.get_or_create(
                name=author_detail.get('name', None),
                email=author_detail.get('email', None))

        publisher_detail = parsed_entry.get('publisher_detail', None)
        if publisher_detail:
            entry.publisher, _ = PenName.objects.get_or_create(
                name=publisher_detail.get('name', None),
                email=publisher_detail.get('email', None))

        contributors = parsed_entry.get('contributors', None)
        if contributors:
            for contributor_detail in contributors:
                contributor, _ = PenName.objects.get_or_create(
                    name=contributor_detail.get('name', None),
                    email=contributor_detail.get('email', None))

                if contributor not in entry.contributors:
                    entry.contributors.add(contributor)

        entry.link = parsed_entry.get('link', None)
        entry.license = parsed_entry.get('license', None)

        contents = parsed_entry.get('content', None)
        if contents:
            for content_data in contents:
                EntryContent.objects.get_or_create(
                    base=content_data.get('base', None),
                    language=content_data.get('language', None),
                    value=content_data.get('value', None),
                    type=content_data.get('content_type', None),
                    entry=entry)

        published_data = parsed_entry.get('published_parsed', None)
        if published_data:
            entry.published = datetime.fromtimestamp(mktime(published_data))

        created_data = parsed_entry.get('created_parsed', None)
        if created_data:
            entry.created = datetime.fromtimestamp(mktime(created_data))

        updated_data = parsed_entry.get('updated_parsed', None)
        if updated_data:
            entry.updated = datetime.fromtimestamp(mktime(updated_data))

        entry.save()
        return entry


class EntryContent(models.Model):
    """ Content associated with a feed entry
    """
    base = models.URLField(name='base', blank=True, null=True)
    language = models.TextField(name='language', blank=True, null=True)
    value = models.TextField(name='value', blank=True, null=True)
    content_type = models.TextField(name='type', blank=True, null=True)
    entry = models.ForeignKey(FeedEntry, on_delete=models.CASCADE, related_name='content')
