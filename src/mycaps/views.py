""" Views for the mycaps app """

import json

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

from product import models as product_models

from . import forms
from . import models

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Views
def mycaps(request):
    color = models.Color.objects.all()
    coffee = models.Coffee.objects.all()
    mycaps_product_instance = product_models.Product.objects.get(id=310)
    if request.method == 'POST':
        form = forms.PackageForm(request.POST or None, request.FILES or None)
        # print(form.data)

        if not form.data['x']:
            form.data['x'] = 0
        if not form.data['y']:
            form.data['y'] = 0
        if not form.data['height']:
            form.data['height'] = 0
        if not form.data['width']:
            form.data['width'] = 0

        if form.is_valid():
            instance = form.save()
            instance.save()
            ajaxData = {}
            ajaxData['msg'] = 'Thank you <br>Your package was created'
            ajaxData['package_id'] = instance.id
            ajaxData['title'] = 'My caps'
            # ajaxData['price'] = str(instance.price)
            ajaxData['dataSave'] = True
            return HttpResponse(json.dumps(ajaxData))
        else:
            # print(form.errors)
            ajaxData = {}
            ajaxData['msg'] = 'Sorry no data saved!'
            return HttpResponse(json.dumps(ajaxData))
    else:
        form = forms.PackageForm()
    context = {
        'form': form,
        'color': color,
        'coffee': coffee,
        'mycaps_product_instance': mycaps_product_instance,
    }
    return render(request, 'package/mycaps.html', context)


def crop(request):
    photo = models.Crop.objects.all()
    if request.method == 'POST':
        form = forms.PackageForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save()
            instance.save()
            return redirect('mycaps:crop')
    else:
        form = forms.PackageForm()
    context = {
        'form': form,
        'photo': photo,
    }
    return render(request, 'package/crop.html', context)
