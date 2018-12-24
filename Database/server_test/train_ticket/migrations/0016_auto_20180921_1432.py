# Generated by Django 2.1 on 2018-09-21 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('train_ticket', '0015_auto_20180920_1719'),
    ]

    operations = [
        migrations.CreateModel(
            name='Current',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='train_ticket.Client')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='current',
            unique_together={('email', 'client')},
        ),
    ]