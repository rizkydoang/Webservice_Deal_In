# Generated by Django 3.1.7 on 2021-11-20 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deal_in_tb', '0012_auto_20211114_1750'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tbluser',
            name='api_key',
        ),
        migrations.AddField(
            model_name='tblstore',
            name='api_key',
            field=models.CharField(default='th5zvp2k8JVLknIiWHB9c9ge7fa7jisIqcZrgYAOhBwbixtsF7', max_length=50),
        ),
    ]
