from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import ListView, DetailView, View,ArchiveIndexView
from django.utils import timezone
from fasteat.models import FoodItem,Restaurant,FoodCategory,Order,OrderDetail,UserProfile
from django.contrib import messages
from django.http import JsonResponse
import json
import datetime
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm
# from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


def register(request):
    if request.user.is_authenticated:
        return redirect('fasteat:venuesgrid')
    else:
        #Register form: using Django defalut user creation form
        context = {}
        regForm = UserForm()
        if request.method == 'POST':
            regForm = UserForm(request.POST)
            if regForm.is_valid():
                user = regForm.save()
                print(user)
                user_name = regForm.cleaned_data['username']
                UserProfile.objects.create(user=user,name=user_name)
                messages.success(request,'Account is successfully created for' + user_name)
                return redirect('fasteat:login')
            else:
                print('Invalid form')
        context['regForm'] = regForm
        return render(request,'fasteat/register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        messages.success(request,'You have already loged in.')
        return redirect('fasteat:venuesgrid')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            print('username:',username)
            print('password:',password)

            user = authenticate(request,username=username,password=password)
            print(user)

            if user is not None:
                login(request,user)
                return redirect('fasteat:venuesgrid')
            else:
                messages.info(request,'Username or Password is wrong')
                # return render(request,'fasteat/login.html',context)

        context = {}
        return render(request,'fasteat/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('fasteat:login')

#show the venues list in grid format
def venuesGrid(request):
    context = {}
    context['restaurants'] = Restaurant.objects.all()
    return render(request,'fasteat/venues_grid.html',context)

def venuesList(request):
    context = {}
    context['restaurants'] = Restaurant.objects.all()
    return render(request,'fasteat/venues_list.html',context)

# @csrf_protect
def menuView(request):
    resInfo = json.loads(request.COOKIES['ResInfo'])
    print('resId from ResInfo',resInfo)
    resId = resInfo['resId']
    print('VenueID',resId)
    context = {}
    restaurant,created = Restaurant.objects.get_or_create(id=resId)
    context['restaurant'] = restaurant
    foods = FoodItem.objects.filter(venue=restaurant)
    context['foods'] = foods
    context['categories'] = []
    for food in foods:
        if(food.itemCategory not in context['categories']):
            context['categories'].append(food.itemCategory)
    print('categories:',context['categories'])
    print('foods got:',context['foods'])
    # context['categories'] = FoodCategory.objects.order_by('name')
    if request.user.is_authenticated:
        customer = request.user.userprofile
        restaurant = Restaurant.objects.get(id=resId)
        order, created = Order.objects.get_or_create(user=customer,restaurant=restaurant, ordered='F')
        print('MenuView order:',order)
        items = order.orderdetail_set.all()
        itemQuantity = order.getTotalQuantity
    else:
        guestData = guestCart(request)
        items = guestData['items']
        order = guestData['order']
        itemQuantity = guestData['itemQuantity']
    context['items'] = items
    context['order'] = order

    #Register form: using Django defalut user creation form
    regForm = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
    context['regForm'] = regForm

    return render(request,"fasteat/menu.html",context)


# @login_required(login_url='fasteat:login')
def checkout(request):
    resInfo = json.loads(request.COOKIES['ResInfo'])
    resId = resInfo['resId']
    restaurant = Restaurant.objects.get(id=resId)
    if request.user.is_authenticated:
        customer = request.user.userprofile
        order, created = Order.objects.get_or_create(user=customer,restaurant=restaurant,ordered='F')
        print('Checkout order:',order)
        items = order.orderdetail_set.all()
        itemQuantity = order.getTotalQuantity
    else:
        guestData = guestCart(request)
        items = guestData['items']
        order = guestData['order']
        itemQuantity = guestData['itemQuantity']

    context = {'items':items,'order':order,'itemQuantity':itemQuantity,'restaurant':restaurant}
    return render(request,'fasteat/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    foodId = data['foodId']
    action = data['action']
    print('Action',action)
    print('food',foodId)

    resInfo = json.loads(request.COOKIES['ResInfo'])
    resId = resInfo['resId']
    customer = request.user.userprofile
    food = FoodItem.objects.get(id=foodId)
    restaurant = Restaurant.objects.get(id=resId)
    order, created = Order.objects.get_or_create(user=customer,restaurant=restaurant,ordered='F')
    print('updateItem order:',order)
    orderitem,created = OrderDetail.objects.get_or_create(order=order,foodItem=food)

    if action == 'add':
        orderitem.quantity += 1
    if action == 'remove':
        orderitem.quantity -= 1

    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()

    return JsonResponse('Item was added',safe=False)

def enterVenue(request):
    data = json.loads(request.body)
    print(request)
    resId = data['resId']
    # resName = data['resName']
    print('VenueID',resId)
    resInfo = {'resId':resId}

    # print('Venue',resName)
    return JsonResponse(safe=False)

def processOrder(request):
    refCode= datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    resInfo = json.loads(request.COOKIES['ResInfo'])
    resId = resInfo['resId']
    restaurant = Restaurant.objects.get(id=resId)

    #Check if the user is logged in
    if request.user.is_authenticated:
        customer = request.user.userprofile
        order, created = Order.objects.get_or_create(user=customer,restaurant=restaurant,ordered='F')
        print('processOrder order:',order)
        totalPrice = float(data['form']['totalPrice'])
        order.refCode = refCode
        print('totoalPrice',totalPrice)
        print('Actual',order.getTotalPrice)
        print('Qty',order.getTotalQuantity)

        #Prevent user manipulate the price data in the front end.
        # Ensure that the front-end data is the same with that of the backend
        if totalPrice == float(order.getTotalPrice):
            order.ordered = 'P'
            print('match',order.ordered)
        else:
            print('No match')
        order.save()
    else:
        print('User is not logged in')
        name = data['form']['name']
        email = data['form']['email']
        phone = data['form']['phone']

        guestData = guestCart(request)
        items = guestData['items']
        customer,create = UserProfile.objects.get_or_create(email=email)
        customer.name = name
        customer.phone = phone
        customer.save()
        order = Order.objects.create(user=customer,restaurant=restaurant,ordered='F')
        order.save()
        print('This is order for Anonymous user:',order)
        for item in items:
            foodItem = FoodItem.objects.get(id=item['foodItem']['id'])
            orderItem = OrderDetail.objects.create(
                foodItem = foodItem,
                order = order,
                quantity = item['quantity']
            )
        print("Cookie:",request.COOKIES)

    totalPrice = float(data['form']['totalPrice'])
    order.refCode = refCode
    if totalPrice == float(order.getTotalPrice):
        order.ordered = 'P'
        order.restaurant.id = resId
    order.save()
    print(order)

    return JsonResponse('Payment complete',safe=False)

# @login_required(login_url='fasteat:login')
def orderConfirm(request):
    resInfo = json.loads(request.COOKIES['ResInfo'])
    resId = resInfo['resId']
    if request.user.is_authenticated:
        customer = request.user.userprofile
        restaurant = Restaurant.objects.get(id=resId)
        try:
            order= Order.objects.get(user=customer,restaurant=restaurant,ordered='P')
            print('There is pending order')
            print('orderConfirm order:',order)
            items = order.orderdetail_set.all()
        except:
            # order = Order.objects.get_or_create(user=customer,ordered='F')
            order = {'id':0,'refCode':None,'ordered':None}
            items = []
            print('There is no pending order')
            print('restaurant ID:',restaurant.id)
    else:
        print('User is not logged in')
        guestData = guestCart(request)
        items = guestData['items']
        # order = []
        order = guestData['order']
        order['ordered'] = 'P'
        # order,created = Order.objects.create()
        restaurant = Restaurant.objects.get(id=resId)
        # order= Order.objects.get(user=customer,restaurant=restaurant,ordered='P')
        # order = {'getTotalPrice':0, 'getTotalQuantity':0,'ordered':'P'}
    context = {'items':items,'order':order}

#Email module
    # template = render_to_string('fasteat/confirm_email.html',{'name':request.user.userprofile.name})
    # email = EmailMessage(
    #     'subject',
    #     'body', #template
    #     settings.EMAIL_HOST_USER, #Email host that sends email
    #     [request.user.userprofile.email], #recipents(logged in user)
    # )
    # email.fail_silently = False
    # email.send()
    # print('email:',email)

    return render(request,'fasteat/confirm.html',context)

@login_required(login_url='fasteat:login')
def historyOrder(request):
    if request.user.is_authenticated:
        customer = request.user.userprofile
        pastOrders = Order.objects.filter(user=customer,ordered='C')  #completed oreders
        # items = pastOrders.orderdetail_set.all()
        items = OrderDetail.objects.all()
    else:
        pastOrders = []
        items = []
    context = {'pastorders':pastOrders,'items':items}

    return render(request,'fasteat/history_order.html',context)


###########################
def guestCart(request):
    try:
        cart = json.loads(request.COOKIES['cart']) #load the cart info from the cookie
    except:
        cart = {}  #create dummy value to prevent the case there is no cart in cookie

    print('GuestCart',cart)
    items = []
    order = {'getTotalPrice':0, 'getTotalQuantity':0,'ordered':'F'}
    itemQuantity = order['getTotalQuantity']

    for i in cart:
        try:
            itemQuantity += cart[i]['quantity']
            item = FoodItem.objects.get(id=i)
            totalPrice = cart[i]['quantity'] * item.price

            order['getTotalPrice'] += totalPrice
            order['getTotalQuantity'] = cart[i]['quantity']

            item = {
                'foodItem':{
                    'id':item.id,
                    'name':item.name,
                    'price':item.price,
                    'imageURL':item.image_url,
                },
                'quantity':cart[i]['quantity'],
                'getItemsPrice':totalPrice
            }
            # print('itemname',item['FoodItem']['name'])
            items.append(item)
        except:
            pass
    return {'items':items,'order':order,'itemQuantity':itemQuantity}


def sbmVenue(request):
    context = {}
    return render(request,'fasteat/submit_restaurant.html',context)

def index(request):
    context = {}
    context['restaurants'] = Restaurant.objects.all()
    return render(request,'fasteat/index.html',context)

@allowed_users(allowed_roles=['staff','admin'])
def resMng(request):
    context = {}
    # context['restaurants'] =
    order = Order.objects.all()
    # print(order)
    context['orders'] = order
    context['items'] = OrderDetail.objects.all()


    return render(request,'fasteat/dashboard.html',context)


def updataOrderStatus(request):
    data = json.loads(request.body)
    print(data)
    orderId = data['orderId']
    print('orderId',orderId)
    order = Order.objects.get(id=orderId)
    order.ordered = 'C'
    order.save()

    return JsonResponse('Order Status changed',safe=False)