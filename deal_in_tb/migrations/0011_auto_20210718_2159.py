# Generated by Django 3.1.7 on 2021-07-18 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deal_in_tb', '0010_auto_20210718_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbltransaction',
            name='token',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='tbluser',
            name='api_key',
            field=models.CharField(default='iA9sPgI4p2qJDTyKYPDxmowBx7c9IuYedpgrHQkIgrmQ2BhLv2', max_length=50),
        ),
    ]
