from django.contrib import admin
from .models import *
from django.utils.html import format_html

# Register your models here.
admin.site.register(Profile)
admin.site.register(User)

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(CustomerReview)
class ProductAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.image.url))

    list_display = ('image_tag','name_prod','price')
    
   
admin.site.register(Product,ProductAdmin)