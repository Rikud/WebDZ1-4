# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-14 13:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IvanAsk', '0002_auto_20171114_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
    ]
