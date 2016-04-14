# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='task_creationdate',
            new_name='creationdate',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='task_text',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='account',
            new_name='user',
        ),
        migrations.AddField(
            model_name='task',
            name='duedate',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Date Due'),
        ),
    ]
