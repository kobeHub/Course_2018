from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import  HttpResponse
from django.core.mail import send_mail
from django.template import loader

from django.urls import reverse
from django.views import generic, View

from django.utils import timezone
from django import forms
from django.contrib.auth.hashers import check_password, make_password

from . models import Client, TrainNumber, PassStations, Carriage, Seat, Current, Ticket, Order
from . forms import SignUpForm
import re



class Result:
    def __init__(self, train_name, start_station, end_station, start_time, end_time, swz, ydz, edz, rz, yz, rw, yw):
        self.train_name = train_name
        self.start_station = start_station
        self.start_time = start_time
        self.end_time = end_time
        self.end_station = end_station
        self.swz = swz
        self.ydz = ydz
        self.edz =edz
        self.rz = rz
        self.yz = yz
        self.rw=  rw
        self.yw = yw



def make_query(start_point, end_point, date):
    """
    进行单次车辆信息的查询:
        return 可用车次信息的dict
    """
    start_available = list(PassStations.objects.filter(date=date).filter(station_id__contains=start_point))
    end_available = list(PassStations.objects.filter(date=date).filter(station_id__contains=end_point))

    # 对数据集进行预处理，出发地不可以是终点站，目的地不可以是起点站
    for item in start_available:
        if item.arrival_time == item.depart_time and item.station_num > 0:
            start_available.remove(item)
    for item in end_available:
        if item.arrival_time is None:
            end_available.remove(item)
        elif item.arrival_time == item.depart_time:
            end_available.remove(item)

    # 找出车次id 做交集
    train_num_end = []
    train_num_start = []
    for end in end_available:
        train_num_end.append(end.train_num_id)
    for item in start_available:
        train_num_start.append(item.train_num_id)
    train_num_start = set(train_num_start)
    train_num_end = set(train_num_end)
    target_set = train_num_end & train_num_start

    target_set = list(target_set)
    results_dict = {}
    for proble in target_set:
        proble_pass_start = PassStations.objects.filter(date=date).filter(train_num_id=proble).filter(station_id__contains=start_point)
        proble_pass_end = PassStations.objects.filter(date=date).filter(train_num_id=proble).filter(station_id__contains=end_point)
        if proble_pass_end[0].arrival_time < proble_pass_start[0].depart_time:
            target_set.remove(proble)
    for item in target_set:
        print(item)#.train_num_id, item.station_id, item.arrival_time, item.depart_time, item.seat_type, item.remine_seats_num)
        train_name = item[12:-8]  #  根据编码规则，得到车次名称
        target_train_item_start = PassStations.objects.filter(date=date).filter(train_num_id=item).filter(station_id__contains=start_point)
        target_train_item_end = PassStations.objects.filter(date=date).filter(train_num_id=item).filter(station_id__contains=end_point)[0]
        target_start_station = target_train_item_start[0].station_id
        target_end_station = target_train_item_end.station_id
        target_arrival_time = target_train_item_end.arrival_time
        target_depart_time = target_train_item_start[0].depart_time

        # result_train = TrainNumber.objects.get(train_num_id=item)

        yz = target_train_item_start.filter(seat_type='YZ')[0].remine_seats_num
        yw = target_train_item_start.filter(seat_type='YW')[0].remine_seats_num
        rz = target_train_item_start.filter(seat_type='YZ')[0].remine_seats_num
        rw = target_train_item_start.filter(seat_type='RW')[0].remine_seats_num
        ydz = target_train_item_start.filter(seat_type='YDZ')[0].remine_seats_num
        edz = target_train_item_start.filter(seat_type='EDZ')[0].remine_seats_num
        swz = target_train_item_start.filter(seat_type='SWZ')[0].remine_seats_num
        result = Result(
            train_name,
            target_start_station,
            target_end_station,
            target_depart_time,
            target_arrival_time,
            swz,
            ydz,
            edz,
            rz,
            yz,
            rw,
            yw)
        results_dict[item] = result

    return results_dict



def query_train(request):
    """
    进行余票查询：
    kwargs:
        start_point
        end_point
        date
        back_date
        is_single
    """
    start_point = request.GET.get('start_point')
    end_point = request.GET.get('end_point')
    date = request.GET.get('date')
    back_date =request.GET.get('back_date')
    is_single = request.GET.get('is_single')
    template_name = 'train_ticket/query.html'

    single_set = make_query(start_point, end_point, date)
    if is_single == 'single':
        return render(request, template_name, {'query_set_single':single_set, 'query_set_double':None})
    else:
        back_set = make_query(end_point, start_point, back_date)
        return render(request, template_name, {'query_set_single':single_set, 'query_set_double':back_set})




def book_ticket(request, train, seat, board_station, board_time, detrain_time, detrain_station):
    """
    进行车票预订：
    args:
        email
        train_num_id
        seat_type
        board_station
        board_station
        detrain_station
        detrain_time
    """
    template_name = 'train_ticket/buy.html'
    print(train, seat, board_time, board_station)
    client = Current.objects.all()
    if not len(client):
        return render(request, template_name, {'error_msg':'您尚未登录，请登录后购票！'})
    else:
        email = client[0].email

    carriage_sets = Carriage.objects.filter(belong_to_train=train, seat_type=seat)
    def change_ticket(request, order_num, to_train, to_carriage, to_seat):
        """
         进行车票改签,生成相应新的车票，删除旧票，改变订单状态
        """
        template_name = 'train_ticket/change.html'
        order = Order.objects.get(order_num=order_num)
        ticket_num = order.ticket_num
        old_ticket = Ticket.objects.get(ticket_num=ticket_num)
    print('参与筛选的车厢数量：', len(carriage_sets))
    # 获取车票信息，检查坐席是否在其中
    tickets = Ticket.objects.filter(
                train_num_id=train,
                email=email,
                board_time=board_time,
                board_station=board_station,
                detrain_station=detrain_station,
                detrain_time=detrain_time,
                seat_type=seat
            )

    not_valid_seat = []
    if len(tickets):
        for ticket in tickets:
            not_valid_seat.append((ticket.carriage_num, ticket.seat_num))
    for carriage in carriage_sets:
        print('carriage num', carriage.carriage_num)
        if carriage.get_seats_num() == 0:
            continue
        carriage_num = carriage.carriage_num
        seat_sets = carriage.seat_set.all()
        for seat_ in seat_sets:
            seat_num = seat_.seat_num
            print('seat number:', seat_num)
            price = seat_.price
            if not_valid_seat == [] or (carriage_num, seat_num) in not_valid_seat:
                # 该seat可用,生成相应订单
                client = Client.objects.get(email=email)
                phone = client.phone
                now = timezone.localtime()
                # 修改车辆余座信息
                try:
                    pass_train = PassStations.objects.get(train_num_id=train, station_id=board_station, seat_type=seat)
                    pass_train.remine_seats_num -= 1
                    pass_train.save()
                    print('更改车次信息成功!')
                except PassStations.DoesNotExist:
                    print('更改车次余票信息出错')

                #生成订单以及车票
                order_num = 'E'+ str(now.year)+ str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)+str(email)
                create_order = Order(
                    order_num=order_num,
                    ticket_num=None,
                    email=email,
                    phone=phone,
                    order_status='Unpay',
                    pub_date=timezone.localtime(),
                    changed_train_num_id=None,
                    price=price,
                    order_client=client
                )
                create_ticket = Ticket(
                    ticket_num=order_num,
                    train_num_id=train,
                    email=email,
                    carriage_num=carriage_num,
                    seat_num=seat_num,
                    board_time=board_time,
                    board_station=board_station,
                    detrain_station=detrain_station,
                    detrain_time=detrain_time,
                    price=price,
                    seat_type=seat,
                    ticket_client=client
                )
                create_ticket.save()
                create_order.save()
                print(create_ticket.ticket_num, create_ticket.train_num_id[12:-8], create_ticket.email, create_ticket.carriage_num, create_ticket.board_time, create_ticket.price)
                return render(request, 'train_ticket/buy.html', {'order_num':create_order.order_num, 'ticket_num':create_ticket.ticket_num, 'price':str(price)})



def buy(request, order_num, ticket_num):
    template_name = 'train_ticket/buy.html'
    return render(request, template_name, {'success_msg':'订单生成成功,请支付!', 'order_num':order_num, 'ticket':ticket_num})


def pay(request, order_num, ticket_num, payed):
    """
    用户支付：
    args：
        order
    """
    template_name = 'train_ticket/pay.html'
    order = Order.objects.get(order_num=order_num)
    ticket = Ticket.objects.get(ticket_num=ticket_num)
    email = order.email
    client = order.order_client
    train_num_id = ticket.train_num_id
    station = ticket.board_station
    seat_type = ticket.seat_type

    if payed == 1 and order.order_status == 'Unpay':
        order.order_status = 'Changing'
        order.ticket_num = ticket.ticket_num
        msg = '购票成功，可进行改签退票操作'
    elif payed == 0 and order.order_status == 'Unpay':
        order.order_status = 'Cancle'
        try:
            pass_train = PassStations.objects.get(train_num_id=train_num_id, station_id=station, seat_type=seat_type)
            pass_train.remine_seats_num += 1
            pass_train.save()
        except PassStations.DoesNotExist:
            print('取消订单更新失败!')
        ticket.delete()
        msg = '订单已取消'

    order.save()
    return render(request, template_name, {"msg":msg})



class TicketView(View):
    def get(self, request, *args, **kwargs):
        current = Current.objects.all()
        if not len(current):
            return render(request, 'train_ticket/ticket_result.html', {'msg':'请登录后查看订单信息!'})
        else:
            cur = current[0]
            email = cur.email
            client = Client.objects.get(email=email)
            name = client.name
            orders = Order.objects.filter(email=email)
            return render(request, 'train_ticket/ticket_result.html', {'order_set':orders,'name':name, 'msg':'订单信息'})



def change_ticket(request, order_num):
    """
     进行车票改签,生成相应新的车票，删除旧票，改变订单状态
    """
    ticket = Ticket.objects.get(ticket_num=order_num)
    order = Order.objects.get(order_num=order_num)
    if order.order_status == 'Changing':
        ticket.delete()
        order.order_status = 'Done'
    order.save()
    return render(request, 'train_ticket/index.html', {'test':None})

def pay_back(request, order_num):
    order = Order.objects.get(order_num=order_num)
    ticket = Ticket.objects.get(ticket_num=order_num)
    if order.order_status == 'Payback' or order.order_status == 'Changing':
        ticket.delete()
        order.order_status = 'Cancle'
        order.save()
        return render(request, 'train_ticket/ticket_result.html', {'msg':'退票成功!'})

def delete_order(request, order_num):
    order = Order.objects.get(order_num=order_num)
    if order.order_status == 'Cancle':
        order.delete()
        return render(request, 'train_ticket/ticket_result.html', {'msg':'订单已删除!'})


class IndexView(View):
    template_name = 'train_ticket/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'test':None})




class LoginView(View):
    template_name = 'train_ticket/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'test':None})

    def post(self, request, *args, **kwargs):
        current = Current.objects.all()
        if len(current) > 0:
            current[0].delete()
        username = request.POST.get('username')
        pwd = request.POST.get('passwd')
        pattern = re.compile(r'^[0-9]+')
        try:
            if pattern.match(username):
                client = Client.objects.get(phone=username)
            else:
                client = Client.objects.get(email=username)
        except Client.DoesNotExist:
            return render(request, self.template_name, {'error_msg':'请先注册'})
        if check_password(pwd, client.passwd):
            cur = Current(email=client.email, client=client)
            cur.save()
            print('email:{} login sucessfully!'.format(username))
            return redirect(reverse('train_ticket:index'))
        else:
            return render(request, self.template_name, {'error_msg':'密码错误'})



class RegisterView(View):
    template_name = 'train_ticket/register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'test':None})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            print(request.POST)
            print(request.POST.get('email'))
            print(request.POST.get('name'))
            print(request.POST.get('passwd'))


            name = request.POST.get('name')
            email= request.POST.get('email')
            phone = request.POST.get('phone')
            card_num = request.POST.get('card_num')
            card_type = request.POST.get('card_type')
            sex = request.POST.get('sex')
            pwd = request.POST.get('passwd')
            pwd = make_password(pwd)

            if not name:
                return(request, self.template_name, {'error_msg':'姓名不可为空!'})
            if not email:
                return(request, self.template_name, {'error_msg':'邮箱不可为空!'})
            if not phone:
                return(request, self.template_name, {'error_msg':'手机号不可为空!'})
            if not sex:
                return(request, self.template_name, {'error_msg':'性别不可为空!'})
            if not card_type:
                return(request, self.template_name, {'error_msg':'证件类型不可为空!'})
            if not name:
                return(request, self.template_name, {'error_msg':'证件号码不可为空!'})


            try:
                if Client.objects.get(email=email):
                    return render(request, self.template_name, {'error_msg':'用户已注册！'},)
            except Client.DoesNotExist:
                client = Client(email=email, phone=phone, name=name, sex=sex, card_type=card_type, card_num=card_num, passwd=pwd)
                client.save()
                return redirect(reverse('train_ticket:login'), {'success_msg':'注册成功！'})





def mail_test(request):
    send_mail(
            'Subject here',
            'Here is the message.',
            'train@innohub.top',
            ['jdgets111@gmail.com'],
            fail_silently=False,
    )
    return HttpResponse('mail sent')




