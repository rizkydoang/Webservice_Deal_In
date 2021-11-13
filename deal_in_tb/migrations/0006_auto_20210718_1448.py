# Generated by Django 3.1.7 on 2021-07-18 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deal_in_tb', '0005_auto_20210718_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbltransaction',
            name='id_cart',
            field=models.ForeignKey(blank=True, db_column='id_cart', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='deal_in_tb.tblcart'),
        ),
        migrations.AddField(
            model_name='tbltransaction',
            name='qty',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tbltransaction',
            name='status',
            field=models.CharField(choices=[('0', 'Belum Transfer'), ('1', 'Sedang di kirim'), ('2', 'Sukses')], default=0, max_length=1),
        ),
        migrations.AlterField(
            model_name='tbltransaction',
            name='total',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tbluser',
            name='api_key',
            field=models.CharField(default='0PHANgyCeUXgeTuubDmggzip7XEhN85sAUC59kkwsYzwcdJ5gB', max_length=50),
        ),
        migrations.DeleteModel(
            name='TblDataTrans',
        ),
    ]
