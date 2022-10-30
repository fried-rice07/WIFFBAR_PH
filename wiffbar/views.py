from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from .models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
import json
import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, View
# Create your views here.
def base(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        item = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        item = None
        cartItems = None
    context = {
        'item':item,
        'cartItems':cartItems,
        'order':order,
    }
    return render(request,'base.html', context)
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        item = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        order = None
        item = None
        cartItems = None
    product = Product.objects.all()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,f' Welcome {username}')
            return redirect('home')
        else:
            messages.info(request, 'Credentials Not Valid')
            return redirect(request.META['HTTP_REFERER'])
    context = {
        'product':product,
        'item':item,
        'cartItems':cartItems,
        'order':order,
    }
    return render(request, 'home.html',context)

def collection(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        item = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        item = None
        order = None
        cartItems = None
    product = Product.objects.all()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,f' Welcome {username}')
            return redirect('home')
        else:
            messages.error(request, 'Credentials Not Valid')
    context = {
        'product':product,
        'order':order,
        'item':item,

    }
    return render(request, 'collections.html', context)

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Exists')
                return redirect(request.META['HTTP_REFERER'])
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username exists')
                return redirect(request.META['HTTP_REFERER'])
            else:
                user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name ,password=password)  
                user.save()
            

                #for login authentication
                # user_login = auth.authenticate(username=username, password=password)
                # auth.login(request, user_login)
                messages.success(request,'Create Account Successfully!')
                return redirect('login')
        else:
            messages.error(request,'Password not match')
            return redirect(request.META['HTTP_REFERER'])
        
    return render(request,'sign-up.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,f' Welcome {username}')
            return redirect('home')
        else:
            messages.error(request, 'Credentials Not Valid')

    return render(request, 'login.html',)
def log_out(request):
    logout(request)
    messages.info(request,'Thankyou for visiting')
    return redirect('home')



class ItemDetailView(DetailView):
    model = Product
    template_name = 'product-page.html'
def add_to_cart(request,pk):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        item = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        item = None
        cartItems = None
        order = None
    product = Product.objects.filter(select="display")
    prod = Product.objects.get(id=pk)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,f' Welcome {username}')
            return redirect('home')
        else:
            messages.error(request, 'Credentials Not Valid')
    context = {
        'prod':prod,
        'product':product,
        'item':item,
        'cartItems':cartItems,
        'order':order,
    }
    return render(request,'add_to_cart.html', context)
def updateItem(request):
    #force the data into template
    data = json.loads(request.body)
    productId = data ['productId']
    action  = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)
def delete_product(request,pk):
    product = OrderItem.objects.get(id=pk)
    product.delete()
    return redirect('home')

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        item = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        item = None
        order = None
        cartItems = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,f' Welcome {username}')
            return redirect('home')
        else:
            messages.error(request, 'Credentials Not Valid')

    context = {
        "order":order,
    }
    return render(request,'checkout.html',context)

def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'your password has changed!')
            return redirect('home')
    form = SetPasswordForm(user)
    context = {
        'form':form
    }
    return render(request,'password_reset.html',context )


def profile(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        item = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        item = None
        order = None
        cartItems = None

    context = {
        'order':order,
        'item':item,
        'cartItems':cartItems,  
    }
    return render(request, 'profile.html',context)
def edit_profile(request, pk):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        item = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        item = None
        order = None
        cartItems = None
    user_id = User.objects.get(id=pk)
    user = UserForm(request.POST or None, request.FILES or None,instance=user_id)
    if user.is_valid():
        user.save()
        messages.success(request,'Profile Updated!')
        return redirect('profile')
    context = {
        'user':user,
        'order':order,
        'item':item,
    }
    return render(request,'edit_profile.html', context)