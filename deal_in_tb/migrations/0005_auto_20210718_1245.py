# Generated by Django 3.1.7 on 2021-07-18 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deal_in_tb', '0004_auto_20210718_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblcart',
            name='deleted',
            field=models.CharField(default=0, max_length=1),
        ),
        migrations.AlterField(
            model_name='tbluser',
            name='api_key',
            field=models.CharField(default='iiZTtpQgncY0XpSu4FYlK8UB4sbyCgDmopgpXR4C31iv9z0ByL', max_length=50),
        ),
    ]
