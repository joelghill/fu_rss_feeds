""" Module for admin app settings
"""
from django.contrib import admin
from rss.models import Feed


admin.site.register(Feed)
