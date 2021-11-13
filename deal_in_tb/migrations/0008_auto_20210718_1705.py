# Generated by Django 3.1.7 on 2021-07-18 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deal_in_tb', '0007_auto_20210718_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbltransaction',
            name='username',
            field=models.ForeignKey(blank=True, db_column='username', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='deal_in_tb.tbluser'),
        ),
        migrations.AlterField(
            model_name='tbluser',
            name='api_key',
            field=models.CharField(default='I4bpW01ltZ6s3RxW8TRDAgZx6nHSr7copRxegaN63VSf1FWi1Y', max_length=50),
        ),
    ]
