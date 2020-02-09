""" Module for admin settings
"""
from django.contrib import admin
from web_presence.models import SocialMediaType, SocialMediaEndpoint, WebIdentity

# Register your models here.
admin.site.register(SocialMediaEndpoint)
admin.site.register(SocialMediaType)
admin.site.register(WebIdentity)
