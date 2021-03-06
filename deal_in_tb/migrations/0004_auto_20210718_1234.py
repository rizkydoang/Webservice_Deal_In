# Generated by Django 3.1.7 on 2021-07-18 05:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deal_in_tb', '0003_auto_20210717_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbluser',
            name='api_key',
            field=models.CharField(default='tl0955zvOKHpjKUHoy3pJSxgNlsYILoKnFowVZ5S5LT24oOGwK', max_length=50),
        ),
        migrations.CreateModel(
            name='TblCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_item', models.ForeignKey(blank=True, db_column='id_item', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='deal_in_tb.tblitem')),
                ('username', models.ForeignKey(blank=True, db_column='username', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='deal_in_tb.tbluser')),
            ],
            options={
                'db_table': 'tbl_cart',
            },
        ),
    ]
