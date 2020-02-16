""" Module for admin app settings
"""
from django.contrib import admin
from rss.models import Feed, FeedEntry, FeedImage
from rss.remote import FeedUpdater

class FeedAdmin(admin.ModelAdmin):
    list_display = ['source', 'title', 'home', 'last_synced', ]
    actions = ['sync']

    def sync(self, request, queryset):

        for feed in queryset:
            FeedUpdater.update_from_source(feed)

    sync.short_description = "Manually sync selected feeds with their sources"

admin.site.register(Feed, FeedAdmin)
admin.site.register(FeedEntry)
admin.site.register(FeedImage)
