""" Module containing utility functions for the RSS app
"""
from datetime import datetime
from time import mktime
from django.utils import timezone

def feed_date_to_datetime(feed_date):
    """ Helper function to convert date time tuple from feed to a datetime object instance

    :param feed_date: Tuple of date time information
    :type feed_date: [type]
    :return: Date time derrived from the input
    :rtype: datetime
    """
    if feed_date:
        return datetime.fromtimestamp(mktime(feed_date), tz=timezone.get_current_timezone())
    
    return None
