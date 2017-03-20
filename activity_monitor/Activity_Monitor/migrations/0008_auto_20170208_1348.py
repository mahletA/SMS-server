# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-08 13:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Activity_Monitor', '0007_auto_20170208_1343'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('hospitalID', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30, null=True, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('salt', models.CharField(max_length=10)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('employee_agreement_file', models.FileField(blank=True, upload_to='agreement_files')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('update_date', models.DateField(auto_now_add=True)),
                ('SystemUser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Activity_Monitor.SystemUser')),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='SystemUser',
        ),
        migrations.AlterField(
            model_name='practitioner',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Activity_Monitor.Users'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
