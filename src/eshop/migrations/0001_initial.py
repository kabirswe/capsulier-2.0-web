# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-31 02:02
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_total', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='discount total')),
                ('shipping_total', models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='shipping total')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='subtotal')),
                ('tax_total', models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='tax total')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='total')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='updated on')),
            ],
            options={
                'ordering': ['-created_on'],
                'verbose_name': 'cart',
                'verbose_name_plural': 'carts',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_item_total', models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=10, null=True, verbose_name='total')),
                ('line_item_subtotal', models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=10, null=True, verbose_name='subtotal')),
                ('line_item_tax_percentage', models.DecimalField(decimal_places=3, default=0, editable=False, max_digits=5, verbose_name='vat percentage')),
                ('line_item_tax_total', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=7, verbose_name='vat total')),
                ('unit_price', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10, verbose_name='unit gross price')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='quantity')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, null=True, verbose_name='updated on')),
            ],
            options={
                'ordering': ['-updated_on'],
                'verbose_name': 'cart item',
                'verbose_name_plural': 'cart items',
            },
        ),
        migrations.CreateModel(
            name='InvoiceNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ending_date', models.DateField(default=django.utils.timezone.now, verbose_name='ending date')),
                ('last_used_number', models.CharField(editable=False, max_length=20, null=True, verbose_name='last used number')),
                ('number_places', models.PositiveSmallIntegerField(default=2, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(2)], verbose_name='number places')),
                ('prefix', models.CharField(max_length=10, verbose_name='prefix')),
                ('starting_date', models.DateField(default=django.utils.timezone.now, verbose_name='starting date')),
                ('created_on', models.DateTimeField(auto_now_add=True, help_text="The object's creation date/time", null=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, help_text="The object's last update date/time", null=True, verbose_name='updated on')),
            ],
            options={
                'verbose_name': 'invoice number',
                'verbose_name_plural': 'invoice numbers',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('canceled_on', models.DateTimeField(blank=True, editable=False, help_text='The order cancel date', null=True, verbose_name='canceled on')),
                ('invoice_number', models.CharField(blank=True, editable=False, max_length=20, verbose_name='invoice number')),
                ('invoiced_on', models.DateTimeField(blank=True, editable=False, help_text='The order posting date', null=True, verbose_name='invoiced on')),
                ('order_id', models.CharField(blank=True, max_length=20, null=True, verbose_name='order id')),
                ('order_total', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='order total')),
                ('shipping_number', models.CharField(blank=True, max_length=20, verbose_name='shipping number')),
                ('shipped_on', models.DateTimeField(blank=True, help_text='The order shipping date', null=True, verbose_name='shipped on')),
                ('status', models.CharField(choices=[('c', 'Created'), ('x', 'Cancel'), ('i', 'Invoiced'), ('p', 'Paid'), ('s', 'Shipped')], default='c', max_length=1, verbose_name='status')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
            ],
            options={
                'ordering': ['-created_on', '-id'],
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('c_type', models.CharField(choices=[('a', 'Percentage on Cart Total'), ('b', 'Percentage on Product Variant'), ('c', 'Free Product Variant')], max_length=1, verbose_name='type')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('description_fr', models.TextField(blank=True, null=True, verbose_name='description')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='description')),
                ('description_es', models.TextField(blank=True, null=True, verbose_name='description')),
                ('name', models.CharField(max_length=40, verbose_name='name')),
                ('name_fr', models.CharField(max_length=40, null=True, verbose_name='name')),
                ('name_en', models.CharField(max_length=40, null=True, verbose_name='name')),
                ('name_es', models.CharField(max_length=40, null=True, verbose_name='name')),
                ('code', models.CharField(max_length=40, unique=True, verbose_name='code')),
                ('percentage', models.DecimalField(blank=True, decimal_places=2, help_text='in %', max_digits=5, null=True, verbose_name='discount percentage')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, null=True, verbose_name='updated on')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='updated by')),
            ],
            options={
                'verbose_name': 'Promo Code',
                'verbose_name_plural': 'Promo Codes',
            },
        ),
        migrations.CreateModel(
            name='ShippingCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_value', models.DecimalField(decimal_places=2, help_text='Euro TTC', max_digits=10, verbose_name='max cart value')),
                ('min_value', models.DecimalField(decimal_places=2, help_text='Euro TTC', max_digits=10, verbose_name='min cart value')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price')),
                ('price_ve', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price vat excluded')),
                ('tax_percentage', models.DecimalField(decimal_places=3, default=0.2, max_digits=5, verbose_name='vat percentage')),
                ('tax', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=5, verbose_name='vat')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, null=True, verbose_name='updated on')),
            ],
            options={
                'verbose_name': 'Shipping Cost',
                'verbose_name_plural': 'Shipping Costs',
            },
        ),
        migrations.CreateModel(
            name='ShippingService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('name', models.CharField(max_length=40, verbose_name='name')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, null=True, verbose_name='updated on')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Shipping Service',
                'verbose_name_plural': 'Shipping Services',
            },
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=120, verbose_name='city')),
                ('phone_number', models.CharField(blank=True, max_length=80, verbose_name='phone number')),
                ('state', models.CharField(max_length=120, verbose_name='country')),
                ('street', models.CharField(max_length=120, verbose_name='street')),
                ('types', models.CharField(choices=[('b', 'Billing'), ('s', 'Shipping'), ('a', 'Both')], max_length=120, verbose_name='type')),
                ('zipcode', models.CharField(max_length=120, verbose_name='zip code')),
            ],
        ),
        migrations.CreateModel(
            name='UserCheckout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='email')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.AddField(
            model_name='useraddress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eshop.UserCheckout', verbose_name='user'),
        ),
        migrations.AddField(
            model_name='shippingcost',
            name='shipping_service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eshop.ShippingService', verbose_name='shippping service'),
        ),
    ]
