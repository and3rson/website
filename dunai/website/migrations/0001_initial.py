# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-27 19:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('title', models.TextField(max_length=128)),
                ('icon', models.CharField(max_length=128)),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('url', models.URLField()),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('title', models.CharField(max_length=128)),
                ('cover', models.ImageField(upload_to='covers')),
                ('description', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='website.Category')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=128)),
                ('icon', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('title', models.CharField(blank=True, max_length=128, null=True)),
                ('file', models.ImageField(upload_to='screenshots')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='screenshots', to='website.Project')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='link',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='website.Project'),
        ),
        migrations.AddField(
            model_name='link',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Provider'),
        ),
    ]
