""" Module containing models representing a person's erb presence
"""
from django.db import models


class SocialMediaType(models.Model):
    """ Class representing a type of social media
    """
    code = models.CharField(max_length=150, primary_key=True, unique=True, blank=False, null=False)
    domain = models.URLField(name='Website', blank=False, null=False)
    # font awesome icon name. Ex: twitter
    icon = models.CharField(max_length=100, blank=True)


class SocialMediaEndpoint(models.Model):
    """ A Class representing a social media link as part of a person's web presence
    """
    type = models.ForeignKey(SocialMediaType, on_delete=models.CASCADE, related_name='endpoints')
    url = models.URLField(name='url', blank=False)

class WebIdentity(models.Model):
    """ A model representing the web identity of a person
    """
    public_name = models.CharField(name="Name", max_length=200, blank=False, null=False)
    about = models.TextField(name="About", blank=True)
    email = models.EmailField(blank=True)
    homepage = models.URLField(name="Homepage", blank=True, null=True)
    social = models.ManyToManyField(SocialMediaEndpoint, related_name="identities")
