from itertools import product
from multiprocessing.sharedctypes import Value
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
from django.utils.datastructures import MultiValueDictKeyError
from .utils import cookieCart
from django.core.mail import send_mail, EmailMessage
# Create your views here.
def base(request):
    product = Product.objects.all()
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        item = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems  = cookieData['cartItems']
        order = cookieData['order']
        item = cookieData['item']

    context = {
        'item':item,
        'cartItems':cartItems,
        'order':order,
        'product':product,
    }
    return render(request,'base.html', context)

def search(request):
    if request.method == "GET":
        searched = request.GET.get('searched')
        product = Product.objects.all().filter(name_prod__icontains=searched)

    
        return render(request,'search_product.html',{'product':product})



def home(request):
    if request.user.is_authenticated:
        
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        item = order.orderitem_set.all()
        cartItems = order.get_cart_items
        
    else:
        cookieData = cookieCart(request)
        cartItems  = cookieData['cartItems']
        order = cookieData['order']
        item = cookieData['item']
    product = Product.objects.all()
    if 'Send' in request.POST:
        if request.method == "POST":
            email = request.POST['email']
            send_mail(
                'WIFFBAR PH',
                'Thanks for subscribing!',
                'settings.EMAIL_HOST_USER',
                [email], fail_silently=False
            )
    elif 'login' in request.POST:

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
    try:
        customer_review = CustomerReview.objects.all()
    except CustomerReview.DoesNotExist:
        customer_review = ""
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        item = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems  = cookieData['cartItems']
        order = cookieData['order']
        item = cookieData['item']
    product = Product.objects.all()
    
    if 'Send' in request.POST:
            if request.method == "POST":
                email = request.POST['email']
                send_mail(
                    'WIFFBAR PH',
                    'Thanks for subscribing!',
                    'settings.EMAIL_HOST_USER',
                    [email], fail_silently=False
                )
    elif 'login' in request.POST:

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
        'order':order,
        'item':item,
        'customer_review':customer_review,

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
    user_customer = request.user
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        item = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems  = cookieData['cartItems']
        order = cookieData['order']
        item = cookieData['item']
    if request.method == "POST":
        if request.user.is_authenticated:
            prod = str(Product.objects.get(id=pk))
            user = request.user
            rating = request.POST['rating']
            message = request.POST['message']
            now = datetime.datetime.now()
            date = now.time()
            customer_review = CustomerReview.objects.create(rating=rating, message=message, user=user, prod=prod, date=date)
            customer_review.save()
            messages.success(request,'Thanks for rating!')
            return redirect(request.META['HTTP_REFERER'])
        else:
            rating = None

    
    product = Product.objects.filter(select="display")
    prod = Product.objects.get(id=pk)
    product_all = Product.objects.all()
    try:
        customer_review = CustomerReview.objects.all()
    except CustomerReview.DoesNotExist:
        customer_review = ""
    if 'Send' in request.POST:
        if request.method == "POST":
            email = request.POST['email']
            send_mail(
                'WIFFBAR PH',
                'Thanks for subscribing!',
                'settings.EMAIL_HOST_USER',
                [email], fail_silently=False
            )
    elif 'login' in request.POST:

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
        'prod':prod,
        'product':product,
        'item':item,
        'cartItems':cartItems,
        'order':order,
        'user':user_customer,
        'customer_review':customer_review,
        'product_all':product_all,
    }
    return render(request,'add_to_cart.html', context)
def updateItem(request):
    #force the data into template
    data = json.loads(request.body)
    productId = data['id']
    action  = data['action']
    print('Action:', action)
    print('Product:', productId)
    if request.user.is_authenticated:
        customer = request.user
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        if action == "add":
            orderItem.quantity += 1
            messages.add_message(request,messages.SUCCESS,'ADD ITEM SUCCESSFUL', fail_silently=True)
        orderItem.save()


    msg = {
        'quantity':order.cart_total,
    }   
        

    return JsonResponse(msg, safe=False)

def delete_product(request,pk):
    product = OrderItem.objects.get(id=pk)
    product.delete()
    return redirect(request.META['HTTP_REFERER'])

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        item = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems  = cookieData['cartItems']
        order = cookieData['order']
        item = cookieData['item']
    if 'Send' in request.POST:
        if request.method == "POST":
            email = request.POST['email']
            send_mail(
                'WIFFBAR PH',
                'Thanks for subscribing!',
                'settings.EMAIL_HOST_USER',
                [email], fail_silently=False
            )
    elif 'login' in request.POST:

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
        cookieData = cookieCart(request)
        cartItems  = cookieData['cartItems']
        order = cookieData['order']
        item = cookieData['item']

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
        cookieData = cookieCart(request)
        cartItems  = cookieData['cartItems']
        order = cookieData['order']
        item = cookieData['item']
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


from django.core.exceptions import MultipleObjectsReturned

def cart(request):
    product = Product.objects.all()
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        item = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems  = cookieData['cartItems']
        order = cookieData['order']
        item = cookieData['item']
    if 'Send' in request.POST:
        if request.method == "POST":
            email = request.POST['email']
            send_mail(
                'WIFFBAR PH',
                'Thanks for subscribing!',
                'settings.EMAIL_HOST_USER',
                [email], fail_silently=False
            )
    elif 'login' in request.POST:

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
        'item':item,
        'cartItems':cartItems,
        'order':order,
        'product':product,
    }
    return render(request,'cart.html',context)

def updateQuantity(request):
    data = json.loads(request.body)
    inputval = int(data['in_val'])
    product_id = data['p_id']
    if request.user.is_authenticated:
        customer = request.user
        product = Product.objects.get(id=product_id)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        orderItem.quantity = inputval
        orderItem.save()

        msg = {
            'total': order.cart_total,
            'subtotal':orderItem.total,
            'total2': order.cart_total,

        }
    return JsonResponse(msg,safe=False)

def deletecart(request):

    return JsonResponse(safe=False)