# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-21 22:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20170321_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalog',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 21, 22, 45, 30, 241405, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, upload_to='/static/app/images/product_photo'),
        ),
    ]