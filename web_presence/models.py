""" Module containing models representing a person's erb presence
"""
from django.db import models


class WebIdentity(models.Model):
    """ A model representing the web identity of a person
    """
    first_name = models.CharField(name="first_name", max_length=100, blank=True)
    last_name = models.CharField(name="last_name", max_length=100, blank=True)
    about = models.TextField(name="about", blank=True)
    homepage = models.URLField(name="homepage", blank=True, null=True)


class SocialMediaType(models.Model):
    """ Class representing a type of social media
    """
    code = models.CharField(max_length=150, primary_key=True)
    domain = models.URLField(name='domain', blank=False, null=False)
    # font awesome icon name. Ex: twitter
    icon = models.CharField(max_length=100, blank=True)


class SocialMediaEndpoint(models.Model):
    """ A Class representing a social media link as part of a person's web presence
    """
    url = models.URLField(name='url', primary_key=True)
    type = models.ForeignKey(SocialMediaType, on_delete=models.CASCADE, related_name='endpoints')
    identity = models.ForeignKey(WebIdentity, on_delete=models.CASCADE, related_name='social_networks')
