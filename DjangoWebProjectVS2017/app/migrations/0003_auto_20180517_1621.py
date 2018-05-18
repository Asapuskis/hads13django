# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-17 14:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='correct',
            field=models.IntegerField(default='1'),
        ),
    ]
