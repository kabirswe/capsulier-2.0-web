""" Forms for the mycaps app """

from PIL import Image
from django import forms

from . import models

__author__ = 'Aupourbau Koumar, Alamgir Kabir Roni'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Forms
class PackageForm(forms.ModelForm):
    x = forms.FloatField(
        widget=forms.HiddenInput(
            attrs={'required': 'false'}
        )
    )
    y = forms.FloatField(
        widget=forms.HiddenInput(
            attrs={'required': 'false'}
        )
    )
    width = forms.FloatField(
        widget=forms.HiddenInput(
            attrs={'required': 'false'}
        )
    )
    height = forms.FloatField(
        widget=forms.HiddenInput(
            attrs={'required': 'false'}
        )
    )
    x1 = forms.FloatField(
        widget=forms.HiddenInput(
            attrs={'required': 'false'}
        )
    )
    y1 = forms.FloatField(
        widget=forms.HiddenInput(
            attrs={'required': 'false'}
        )
    )
    width1 = forms.FloatField(
        widget=forms.HiddenInput(
            attrs={'required': 'false'}
        )
    )
    height1 = forms.FloatField(
        widget=forms.HiddenInput(
            attrs={'required': 'false'}
        )
    )

    class Meta:
        model = models.Package

        fields = [
            'color',
            'coffee',
            'text1',
            'text2',
            'image',
            'x',
            'y',
            'width',
            'height',
            'image1',
            'x1',
            'y1',
            'width1',
            'height1',
        ]

    def save(self):
        photo = super(PackageForm, self).save()
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')
        image = Image.open(photo.image)
        cropped_image = image.crop((x, y, w + x, h + y))
        resized_image = cropped_image.resize((400, 400), Image.ANTIALIAS)
        resized_image.save(photo.image.path)

        return photo

        photo1 = super(PackageForm, self).save()
        x1 = self.cleaned_data.get('x1')
        y1 = self.cleaned_data.get('y1')
        w1 = self.cleaned_data.get('width1')
        h1 = self.cleaned_data.get('height1')

        # if self.cleaned_data.get('image'):
        image1 = Image.open(photo1.image1)
        cropped_image1 = image1.crop((x1, y1, w1 + x1, h1 + y1))
        resized_image1 = cropped_image1.resize((400, 400), Image.ANTIALIAS)
        resized_image1.save(photo1.image1.path)

        return photo1


# class PackageForm2(forms.ModelForm):
#     x = forms.FloatField(widget=forms.HiddenInput())
#     y = forms.FloatField(widget=forms.HiddenInput())
#     width = forms.FloatField(widget=forms.HiddenInput())
#     height = forms.FloatField(widget=forms.HiddenInput())

#     class Meta:
#         model = Crop

#         fields = [
#             'image',
#             'x',
#             'y',
#             'width',
#             'height',
#         ]
#         widgets = {
#             'image': forms.FileInput(attrs={
#                 'accept': 'image/*',
#                 'required': 'false',
#             })
#         }

#     def save(self):
#         print 'in my caps form'
#         print self
#         photo = super(PackageForm2, self).save()
#         print 'in my caps form photo section'
#         print photo

#         x = self.cleaned_data.get('x')
#         y = self.cleaned_data.get('y')
#         w = self.cleaned_data.get('width')
#         h = self.cleaned_data.get('height')

#         image = Image.open(photo.image)
#         cropped_image = image.crop((x, y, w+x, h+y))
#         resized_image = cropped_image.resize((400, 400), Image.ANTIALIAS)
#         resized_image.save(photo.image.path)

#         return photo
