# Generated by Django 2.1 on 2018-09-19 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('train_ticket', '0008_auto_20180919_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='passstations',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='passstations',
            name='station_id',
            field=models.CharField(max_length=80),
        ),
    ]