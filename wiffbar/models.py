
from email.policy import default
from enum import unique
from math import prod
from random import choices
from tkinter import N
from tokenize import blank_re
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
# Create your models here.
choice_gender = [
    ('Male','Male'),
    ('Female','Female'),
]
class User(AbstractUser):
    first_name = models.CharField(max_length= 50, null=True)
    last_name = models.CharField(max_length= 50, null=True)
    username = models.CharField(max_length= 50,null=True, unique=True)
    email = models.EmailField(unique=True, null=True)
    photo = models.ImageField(upload_to='static/images' , blank=True)
    address = models.CharField(max_length = 50, blank=True)
    phone_no = models.IntegerField(null=True)
    form_submitted = models.BooleanField(default=True)
    gender = models.CharField(max_length=10, choices=choice_gender, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    def __str__(self):
        return "{}".format(self.username)
    @property
    def image(self):
        try:
            url = self.photo.url
        except:
            url = ""
        
        return url

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
  

    def __str__(self):
        return str(self.user.username)

@receiver(post_save, sender = User)
def create_user_profile(sender,instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender,instance, **kwargs):
    instance.profile.save()

choice_select = [
    ('new_product','new_product'),
    ('exclusive','exclusive_prod'),
    ('display','display'),
]

class Product(models.Model):
    name_prod = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    discount_price = models.DecimalField(max_digits=7 , decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True,blank=True)
    select = models.CharField(max_length=100, choices=choice_select, blank=True)

    def __str__(self):
        return self.name_prod

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length= 100, null=True)
    def __str__(self):
        return str(self.id) 
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    @property
    def cart_total(self):
        try:
            url = self.get_cart_total
        except:
            url = ""
        return url
    #shipping property 
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        
        return shipping




class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete= models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    def __str__(self):
        return str(self.product)
    @property 
    def get_total(self):
        total= self.product.price * self.quantity
        return total

    @property
    def total(self):
        try:
            url = self.get_total
        except:
            url = ""
        return url

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode= models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address

class CustomerReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=1000, blank=True)
    rating = models.CharField(max_length=1,blank=True)
    prod = models.CharField(max_length=100, null=True)
    date = models.TimeField(auto_now=False,auto_now_add=False)
    def __str__(self):
        return self.user.username
    