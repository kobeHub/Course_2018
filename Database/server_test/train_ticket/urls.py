from django.urls import path

from . import views


app_name = 'train_ticket'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('test/', views.mail_test, name='test'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('query/', views.query_train, name='query'),
    path('book_ticket/<str:train>/<str:seat>/<str:board_station>/<str:board_time>/<str:detrain_station>/<str:detrain_time>/', views.book_ticket, name='book_ticket'),
    path('pay/<str:order_num>/<str:ticket_num>/<int:payed>/', views.pay, name='pay'),
    path('buy/<str:order_num>/<str:ticket_num>/<str:price>/', views.buy, name='buy'),
    path('ticket/', views.TicketView.as_view(), name='ticket'),
    path('delete/<str:order_num>', views.delete_order, name='delete'),
    path('payback/<str:order_num>/', views.pay_back, name='payback'),
    path('change/<str:order_num>/', views.change_ticket, name='change'),
]
