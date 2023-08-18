""" Utils for the blog app """

import uuid

from django.utils import timezone

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Upload to
def blog_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return "blog/%s/%s" % (
        timezone.now().strftime('%Y/%m/%d'),
        filename
    )
