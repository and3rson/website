# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-27 20:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('bg_color', models.CharField(max_length=32)),
                ('text_color', models.CharField(max_length=32)),
                ('importance', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(to='website.Tag'),
        ),
    ]