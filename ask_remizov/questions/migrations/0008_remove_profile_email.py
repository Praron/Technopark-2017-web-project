# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-20 07:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0007_auto_20170517_1750'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
    ]