from django.db import models
from django.utils.translation import gettext_lazy as _

class Client(models.Model):
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=60)
    name  = models.CharField(max_length=80, blank=False)
    card_num = models.CharField(max_length=120, blank=False)
    CARD_TYPE_LIST = (
        ('EDJ','二代居民身份证'),
        ('LSS', '临时身份证'),
        ('HKB', '户口簿'),
        ('JRB', '中国人民解放军军人保障卡'),
        ('JGZ', '军官证'),
        ('WJJ','武警警官证'),
        ('SBZ','士兵证'),
        ('JDX','军队学员证'),
        ('JDW','军队文职干部证'),
        ('JDL','军队离休干部证'),
        ('HZ','护照'),
        ('GAJ','港澳居民来往内地通行证'),
        ('GAT','中华人民共和国来往港澳通行证'),
        ('TWJ','台湾居民来往大陆通行证'),
        ('DLJ', '大陆居民来往台湾通行证'),
        ('WJL','外国人居留证'),
        ('RJZ','外国人出入境证'),
        ('WJG','外交官证'),
        ('LSG','领事馆证'),
        ('HYZ','海员证'),
        ('WGR','外交部开具的外国人身份证明'),
        ('DFG','地方公安机关出入境管理部门开具的护照报失证明'),
        ('TLG', '铁路公安部门填发的乘坐旅客列车临时身份证明'),
        ('XSZ','身高不足1.5m的未成年人学生证')
    )
    card_type = models.CharField(max_length=3, choices=CARD_TYPE_LIST, blank=False)
    SEX_LIST = (
        ('M', '男'),
        ('F', '女'),
    )
    sex = models.CharField(max_length = 1, choices=SEX_LIST)
    passwd = models.CharField(_('password'), max_length=128)


    class Meta:
        # 设置联合主码
        unique_together = ('email', 'phone')



class Ticket(models.Model):
    ticket_num = models.CharField(max_length=100, primary_key=True)
    train_num_id = models.CharField(max_length=80)
    email = models.CharField(max_length=100)
    carriage_num = models.CharField(max_length=20)
    seat_num = models.CharField(max_length=20)
    board_time = models.DateTimeField('board time')
    board_station = models.CharField(max_length=20)
    detrain_time = models.DateTimeField('detrain time')
    detrain_station = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seat_type = models.CharField(max_length=20)

    # 多对一关系
    ticket_client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('train_num_id', 'email', 'carriage_num', 'seat_num')



class Order(models.Model):
    order_num = models.CharField(max_length=80, primary_key=True)
    ticket_num = models.CharField(max_length=80, null=True, blank=True)
    phone = models.CharField(max_length=60)
    email = models.CharField(max_length=100)
    ORDER_STATUS_LIST = (
        ('Done', '完成'),
        ('Cancle', '取消'),
        ('Unpay', '待付款'),
        ('Changing', '可改签,可退款'),
        ('Payback', '仅可退款'),
    )
    order_status = models.CharField(max_length=8, choices=ORDER_STATUS_LIST)
    pub_date = models.DateTimeField('创建时间')
    changed_train_num_id = models.CharField(max_length=80, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # 多对一关系
    order_client = models.ForeignKey(Client, on_delete=models.CASCADE)



class TrainNumber(models.Model):
    train_num_id = models.CharField(max_length=80, primary_key=True)
    train_name = models.CharField(max_length=20)
    start_station = models.CharField(max_length=20)
    end_station = models.CharField(max_length=20)
    date = models.DateField()

    def get_carriages_num(self):
        return self.carriage_set.count()

    def get_seat_type_num(self):
        yz, rz, yw, rw, edz, ydz, swz = 0, 0, 0, 0, 0, 0, 0
        if self.get_carriages_num() == 0:
            return {'YZ':0, 'YW':0, 'RZ':0, 'RW':0, 'YDZ':0, 'EDZ':0, 'SWZ':0}
        else:
            for carriage in self.carriage_set.all():
                if carriage.seat_type == 'YZ':
                    yz += carriage.get_seats_num()
                elif carriage.seat_type == 'RZ':
                    rz += carriage.get_seats_num()
                elif carriage.seat_type == 'YW':
                    yw += carriage.get_seats_num()
                elif carriage.seat_type == 'RW':
                    rw += carriage.get_seats_num()
                elif carriage.seat_type == 'EDZ':
                    edz += carriage.get_seats_num()
                elif carriage.seat_type == 'YDZ':
                    ydz += carriage.get_seats_num()
                elif carriage.seat_type == 'SWZ':
                    swz += carriage.get_seats_num()
            return {'YZ':yz, 'RZ':rz, 'YW':yw, 'EDZ':edz, 'YDZ':ydz, 'SWZ':swz, 'RW':rw}


class Carriage(models.Model):
   # id = models.AutoField(primary_key=True)
    belong_to_train = models.ForeignKey(TrainNumber, on_delete=models.CASCADE)
    carriage_num = models.CharField(max_length=20)
    SEAT_TYEP_LIST = (
        ('YZ', '硬座'),
        ('RZ', '软座'),
        ('YW', '硬卧'),
        ('RW', '软卧'),
        ('YDZ', '一等座'),
        ('EDZ', '二等座'),
        ('SWZ', '商务座'),
    )
    seat_type = models.CharField(max_length=3, choices=SEAT_TYEP_LIST)

    def get_seats_num(self):
        return self.seat_set.count()

    class Meta:
        unique_together = ('belong_to_train', 'carriage_num')



class Seat(models.Model):
    belong_to_carriage = models.ForeignKey(Carriage, on_delete=models.CASCADE)
    seat_num = models.CharField(max_length=20, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_carriage(self):
        return self.belong_to_carriage.carriage_num

    def get_train(self):
        return self.belong_to_carriage.belong_to_train.train_num_id

    class Meta:
        unique_together = ('belong_to_carriage', 'seat_num')


class Stations(models.Model):
    #station_id = models.CharField(max_length=50, primary_key=True)
    station_name = models.CharField(max_length=50, primary_key=True)
    station_code = models.CharField(max_length=3, blank=True)


class PassStations(models.Model):
    train_num_id = models.CharField(max_length=80)
    station_id = models.CharField(max_length=80)
    arrival_time = models.DateTimeField('arrival time')
    depart_time = models.DateTimeField('depart time')
    station_num = models.IntegerField(default=-1)
    SEAT_TYEP_LIST = (
        ('YZ', '硬座'),
        ('RZ', '软座'),
        ('YW', '硬卧'),
        ('RW', '软卧'),
        ('YDZ', '一等座'),
        ('EDZ', '二等座'),
        ('SWZ', '商务座'),
    )
    seat_type = models.CharField(max_length=3, choices=SEAT_TYEP_LIST)
    remine_seats_num = models.IntegerField()
    date = models.DateField(blank=True, null=True)



    class Meta:
        unique_together = ('train_num_id', 'station_id', 'seat_type')


class Current(models.Model):
    email = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('email', 'client')



"""
class RemineSeatsNums(models.Model):
    train_num_id = models.CharField(max_length=80)
    station_id = models.CharField(max_length=50)
    SEAT_TYEP_LIST = (
        ('YZ', '硬座'),
        ('RZ', '软座'),
        ('YW', '硬卧'),
        ('RW', '软卧'),
        ('YDZ', '一等座'),
        ('EDZ', '二等座'),
        ('SWZ', '商务座'),
    )
    seat_type = models.CharField(max_length=3, choices=SEAT_TYEP_LIST)
    total_num = models.IntegerField()
    remine_num = models.IntegerField()


    class Meta:
        unique_together = ('train_num_id', 'station_id')
        """

