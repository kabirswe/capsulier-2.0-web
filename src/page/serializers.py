""" API serializers for the page app """

from rest_framework import serializers

from .models import Shop, Schedule

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Serializers
class ScheduleSerializers(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = (
            'id',
            'afternoon_end_time',
            'afternoon_start_time',
            'close',
            'day',
            'get_day_display',
            'morning_end_time',
            'morning_start_time',
            'shop',
        )


class ShopSerializers(serializers.ModelSerializer):
    schedule_set = ScheduleSerializers(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = (
            'id',
            'sites',
            'active',
            'address',
            'address2',
            'email',
            'get_image_mq',
            'logo',
            'name',
            'phone',
            'slug',
            'schedule_set',
            'website',
        )
