# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-26 19:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poetry_generator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poem',
            name='poem_text',
            field=models.TextField(max_length=1000),
        ),
    ]
