# Generated by Django 2.1 on 2018-09-19 17:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('train_ticket', '0012_auto_20180920_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seat',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='trainnumber',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 9, 19, 17, 46, 47, 132409, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
