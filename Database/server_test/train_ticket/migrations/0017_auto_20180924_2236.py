# Generated by Django 2.1 on 2018-09-24 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('train_ticket', '0016_auto_20180921_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ticket_num',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]