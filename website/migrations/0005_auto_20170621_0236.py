# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 02:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20170621_0231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gerenciardoenca',
            name='id',
        ),
        migrations.AlterField(
            model_name='gerenciardoenca',
            name='codigo',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
