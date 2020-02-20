""" Module containing the Pen Name model and supporting code
"""
from django.db import models

class PenName(models.Model):
    """ A pen name potentially used by an author, publisher, or contributor for a feed
    """
    name = models.CharField(name="name", max_length=100, blank=False)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        if self.name:
            return self.name
        return self.email
