from django.contrib import admin

from . models import TrainNumber, Carriage, Seat, Stations, PassStations, Client, Order, Ticket



class SeatInline(admin.TabularInline):
    model = Seat
    extra = 3



class CarriageInline(admin.StackedInline):
    model = Carriage
    extra = 3
    #inlines = [SeatInline]


@admin.register(TrainNumber)
class TrainNumberAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['train_num_id']}),
        ('编号', {'fields':['train_name']}),
        ('始发站', {'fields':['start_station']}),
        ('终点站', {'fields':['end_station']}),
        ('日期', {'fields':['date']}),
    ]
    inlines = [CarriageInline]

    list_display = ('train_num_id', 'train_name', 'start_station', 'end_station', 'get_carriages_num')
    list_fliter = ['train_name']
    search_fields = ['train_num_id']



@admin.register(Carriage)
class CarriageAdmin(admin.ModelAdmin):
    """
    fieldsets = [
       #('所属列车', {'readonly_fields':['belong_to_train_id']}),
        ('车厢号', {'fields':['carriage_num']}),
        ('坐席类型', {'fields':['seat_type']}),
    ]"""
    inlines = [SeatInline]

    list_display = ('belong_to_train_id', 'carriage_num', 'seat_type', 'get_seats_num')
    list_fliter = ['seat_type']
    search_fields = ['seat_type']



@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    readonly_fields = ('get_train', 'get_carriage')
    #fields = ('seat_num',)

    list_display = ('get_train', 'get_carriage','seat_num', )
    list_fliter = ['get_train']
    search_fields = ['get_train']



@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    fieldsets = [
        ('个人信息', {'fields':['name', 'sex', 'card_num', 'card_type']}),
        ('账号以及联系方式', {'fields':['email', 'phone']}),
        ('密码', {'fields':['passwd']}),
    ]

    list_display = ('name', 'email', 'phone', 'card_num')
    list_fliter = ['phone']
    search_fields = ['name']

@admin.register(Stations)
class StationsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('站点信息', {'fields':['station_name', 'station_code']})
    ]
    list_display = ('station_name', 'station_code')
    search_fields = ['Station_name']



@admin.register(PassStations)
class PassStationsAdmin(admin.ModelAdmin):
    list_display = ('train_num_id', 'station_id', 'arrival_time', 'depart_time', 'station_num', 'seat_type', 'remine_seats_num', 'date')
    search_fields = ['train_num_id']
    list_fliter = ['station_id']



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_num', 'email', 'order_status', 'pub_date', 'price']
    search_fields = ['email']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_num', 'email', 'price', 'board_time', 'board_station']
    search_fields = ['ticket_num']
#admin.site.register(TrainNumber, TrainNumberAdmin)
#admin.site.register(Carriage, CarriageAdmin)
#admin.site.register(Seat, SeatAdmin)
#admin.site.register(Stations)
#admin.site.register(Client)
#admin.site.register(PassStations)



