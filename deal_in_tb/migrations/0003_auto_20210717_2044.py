# Generated by Django 3.1.7 on 2021-07-17 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deal_in_tb', '0002_auto_20210717_0010'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbluser',
            name='api_key',
            field=models.CharField(default='moMNUtWbiueJbG6xo7bZsK9MNLszwL0ZBNtItpe7jYrG6yGXBw', max_length=50),
        ),
        migrations.AddField(
            model_name='tbluser',
            name='limited',
            field=models.IntegerField(default=0),
        ),
    ]
