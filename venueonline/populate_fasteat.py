import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'venueonline.settings')

import django
django.setup()
from fasteat.models import Restaurant, FoodItem, Menu, Order, OrderDetail, Payment, FoodCategory

from django.contrib.auth.models import User,UserManager
from django.db import IntegrityError
from django.core.files import File



def populate():

    ## making a superuser
    username = 'wenjing'
    email = '1359832701@qq.com'
    password = 'Gauss5050'

    super = UserManager.create_superuser(username, email, password)
    #
    #
    # restaurants = {'Happy Lunch':{'address':'South Kensington Campus London, SW7 2AZ'},
    #                'KFC': {'address':'173-175 Earls Court Road, SW5 9RF'},
    #                'Domino\'s':{'address':'West Kensington 13 To 15 Northend Parade Fulham, W14 0SJ'}
    #                }
    #
    #
    # for
    # def add_res():

    # fooditems = {}






