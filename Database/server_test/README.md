# A simple django app to simulate 12306.cn

![GCC](https://img.shields.io/badge/Build-pass-brightgreen.svg)  ![gdb](https://img.shields.io/badge/django-2.1-brightgreen.svg)  ![Hex.pm](https://img.shields.io/hexpm/l/plug.svg?style=flat-square)  

##Introduction

**The program is a database course design in software college, ShanDong University.** 

**The course  aims to identify the ability to design database pattern and implement  basic functions.**

**Based on django frame and python 3.6, it's a web-application to simulate the basic functions of [12306.com](https://www.12306.cn), such as query train, issue ticket, pay on-line (simulation), bounce a check, change tickets**

 ## Install

```
pip install django_train_ticket-0.1-py3-none-any.whl
```



Quick start
-----------

**1. Add "train_ticket" to your INSTALLED_APPS setting like this::***

```python
INSTALLED_APPS = [
    ...
    'train_ticket',
]
```

**2. Include the polls URLconf in your project urls.py like this::**

```python
path('train_ticket/', include('train_ticket.urls')),
```

**3. Run `python manage.py migrate` to create the polls models.**

**4. Start the development server and visit http://127.0.0.1:8000/admin/**
   **to create a user or manage the train, station, seat message (you'll need the Admin app enabled).**

**5. Visit http://127.0.0.1:8000/train_ticket/ to order the ticket.**



## All details

**All the details are in the [PRD.pdf](https://github.com/kobeHub/Course_2018/blob/master/Database/server_test/PRD.pdf), the product requirement document.**