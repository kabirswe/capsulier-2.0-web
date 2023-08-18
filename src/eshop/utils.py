# -*- coding: utf-8 -*-

""" Utils for the eshop app """

import StringIO
import uuid
import zipfile

from django.http import HttpResponse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

__author__ = 'Olivier Hourcard'
__credits__ = 'Olivier Hourcard, Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Oh! Softwares, Maison Mahdil'


# Admin actions
def cancel(modeladmin, request, queryset):
    queryset = queryset.exclude(status='x')
    for order in queryset:
        order.cancel()


def invoice(modeladmin, request, queryset):
    queryset = queryset.exclude(status='c').exclude(status='i')
    for order in queryset:
        order.invoice()


def print_invoice(modeladmin, request, queryset):
    queryset = queryset.filter(status='i')

    # Open StringIO to grab in-memory ZIP contents
    str_buffer = StringIO.StringIO()

    # The zip compressor
    zip_file = zipfile.ZipFile(str_buffer, "w")

    for header in queryset:
        # Generate the PDF & Add it to the ZIP file
        zip_file.writestr(
            "%s.pdf" % (header.invoice_number,),
            header.to_pdf()
        )

    # Must close zip for all contents to be written
    zip_file.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    response = HttpResponse(
        str_buffer.getvalue(),
        content_type='application/x-zip-compressed'
    )
    response['Content-Disposition'] = 'attachment; filename="pdfs.zip"'
    return response


# Admin actions description
cancel.short_description = _('Cancel selected sales header(s)')
invoice.short_description = _('Invoice selected sales header(s)')
print_invoice.short_description = _('Print invoice(s) of selected sales header(s)')


# Admin box
def get_total(self):
    return self.get_total


# Admin box description
get_total.short_description = _('Total')


# Methods
def file_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return "eshop/%s/%s" % (
        timezone.now().strftime('%Y/%m/%d'),
        filename
    )
