# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-12-17 21:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20181217_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(default='', upload_to='teachers/%Y/%m', verbose_name='\u5934\u50cf'),
        ),
    ]
