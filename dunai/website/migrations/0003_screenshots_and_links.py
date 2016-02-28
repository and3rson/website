# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-28 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20160227_2024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='project',
        ),
        migrations.RemoveField(
            model_name='screenshot',
            name='project',
        ),
        migrations.AddField(
            model_name='project',
            name='links',
            field=models.ManyToManyField(to='website.Link'),
        ),
        migrations.AddField(
            model_name='project',
            name='screenshots',
            field=models.ManyToManyField(to='website.Screenshot'),
        ),
    ]