# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('sent_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.TextField()),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='sent_messages')),
            ],
            options={
                'ordering': ('sent_at',),
            },
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('subject', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='UserThread',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('unread', models.BooleanField()),
                ('deleted', models.BooleanField()),
                ('thread', models.ForeignKey(to='pinax_messages.Thread')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='thread',
            name='users',
            field=models.ManyToManyField(through='pinax_messages.UserThread', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='thread',
            field=models.ForeignKey(to='pinax_messages.Thread', related_name='messages'),
        ),
    ]
