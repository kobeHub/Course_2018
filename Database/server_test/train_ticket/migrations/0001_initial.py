# Generated by Django 2.1 on 2018-09-12 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carriage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carriage_num', models.CharField(default=None, max_length=20)),
                ('seat_type', models.CharField(choices=[('YZ', '硬座'), ('RZ', '软座'), ('YW', '硬卧'), ('RW', '软卧'), ('YDZ', '一等座'), ('EDZ', '二等座'), ('SWZ', '商务座')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=60)),
                ('name', models.CharField(max_length=80)),
                ('card_num', models.CharField(max_length=120)),
                ('card_type', models.CharField(choices=[('EDJ', '二代居民身份证'), ('LSS', '临时身份证'), ('HKB', '户口簿'), ('JRB', '中国人民解放军军人保障卡'), ('WJJ', '武警警官证'), ('SBZ', '士兵证'), ('JDX', '军队学员证'), ('JDW', '军队文职干部证'), ('JDL', '军队离休干部证'), ('HZ', '护照'), ('GAJ', '港澳居民来往内地通行证'), ('GAT', '中华人民共和国来往港澳通行证'), ('TWJ', '台湾居民来往大陆通行证'), ('WJL', '外国人居留证'), ('RJZ', '外国人出入境证'), ('WJG', '外交官证'), ('LSG', '领事馆证'), ('JYZ', '海员证'), ('WGR', '外交部开具的外国人身份证明'), ('DFG', '地方公安机关出入境管理部门开具的护照报失证明'), ('TLG', '铁路公安部门填发的乘坐旅客列车临时身份证明')], max_length=3)),
                ('sex', models.CharField(choices=[('M', '男'), ('F', '女')], max_length=1)),
                ('passwd', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_num', models.CharField(max_length=80, primary_key=True, serialize=False)),
                ('ticket_num', models.CharField(max_length=80)),
                ('phone', models.CharField(max_length=60)),
                ('email', models.CharField(max_length=100)),
                ('order_status', models.CharField(choices=[('Done', '完成'), ('Cancle', '取消'), ('Unpay', '待付款'), ('Changing', '可改签,可退款'), ('Payback', '仅可退款')], max_length=8)),
                ('pub_date', models.DateTimeField(verbose_name='创建时间')),
                ('changed_train_num_id', models.CharField(blank=True, max_length=80)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='train_ticket.Client')),
            ],
        ),
        migrations.CreateModel(
            name='PassStations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('train_num_id', models.CharField(max_length=80)),
                ('station_id', models.CharField(max_length=50)),
                ('arrival_time', models.DateTimeField(verbose_name='arrival time')),
                ('depart_time', models.DateTimeField(verbose_name='depart time')),
                ('seat_type', models.CharField(choices=[('YZ', '硬座'), ('RZ', '软座'), ('YW', '硬卧'), ('RW', '软卧'), ('YDZ', '一等座'), ('EDZ', '二等座'), ('SWZ', '商务座')], max_length=3)),
                ('remine_seats_num', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_num', models.CharField(default=None, max_length=20)),
                ('belong_to_carriage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='train_ticket.Carriage')),
            ],
        ),
        migrations.CreateModel(
            name='Stations',
            fields=[
                ('station_name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket_num', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('train_num_id', models.CharField(max_length=80)),
                ('email', models.CharField(max_length=100)),
                ('carriage_num', models.CharField(max_length=20)),
                ('seat_num', models.CharField(max_length=20)),
                ('board_time', models.DateTimeField(verbose_name='board time')),
                ('board_station', models.CharField(max_length=20)),
                ('detrain_time', models.DateTimeField(verbose_name='detrain time')),
                ('detrain_station', models.CharField(max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('seat_type', models.CharField(max_length=20)),
                ('ticket_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='train_ticket.Client')),
            ],
        ),
        migrations.CreateModel(
            name='TrainNumber',
            fields=[
                ('train_num_id', models.CharField(max_length=80, primary_key=True, serialize=False)),
                ('train_name', models.CharField(max_length=20)),
                ('start_station', models.CharField(max_length=20)),
                ('end_station', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='passstations',
            unique_together={('train_num_id', 'station_id')},
        ),
        migrations.AlterUniqueTogether(
            name='client',
            unique_together={('email', 'phone')},
        ),
        migrations.AddField(
            model_name='carriage',
            name='belong_to_train',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='train_ticket.TrainNumber'),
        ),
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together={('train_num_id', 'email', 'carriage_num', 'seat_num')},
        ),
        migrations.AlterUniqueTogether(
            name='seat',
            unique_together={('belong_to_carriage', 'seat_num')},
        ),
        migrations.AlterUniqueTogether(
            name='carriage',
            unique_together={('belong_to_train', 'carriage_num')},
        ),
    ]
