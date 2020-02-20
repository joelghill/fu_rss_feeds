""" Module for admin app settings
"""
from django.contrib import admin
from rss.models import Feed, FeedEntry, FeedImage, PenName
from rss.remote import FeedUpdater

class FeedAdmin(admin.ModelAdmin):
    """ Admin class for feed model
    """
    list_display = ['source', 'title', 'home', 'last_synced', ]
    actions = ['sync']

    def sync(self, request, queryset):
        """ Action used to manually sync all selected feeds
        """
        for feed in queryset:
            FeedUpdater.update_from_source(feed)

    sync.short_description = "Manual Sync Feeds"


class FeedEntryAdmin(admin.ModelAdmin):
    """ Admin class for Feed Entry model
    """
    list_display = ['source', 'title', 'published', 'author']


class PenNameAdmin(admin.ModelAdmin):
    """ Admin class for Pen Name model
    """
    list_display = ['name', 'email']


admin.site.register(Feed, FeedAdmin)
admin.site.register(FeedEntry, FeedEntryAdmin)
admin.site.register(FeedImage)
admin.site.register(PenName, PenNameAdmin)
