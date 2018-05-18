# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-17 18:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_question_tema'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='correct',
        ),
        migrations.AddField(
            model_name='question',
            name='numChoices',
            field=models.IntegerField(default='0'),
        ),
    ]
