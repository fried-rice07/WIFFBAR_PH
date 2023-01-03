import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        print('Cart:',cart)

    item = []
    order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
    cartItems = order['get_cart_items']

    for i in cart:
        cartItems += cart[i]["quantity"]
        product = Product.objects.get(id=i)
        total = (product.price * cart[i]["quantity"])
        order['get_cart_total'] += total
        order['get_cart_items'] += cart[i]["quantity"]
        
        
        

        item_cart = {
            'product':{
                
                'id':product.id,
                'name_prod':product.name_prod,
                'price':product.price,
                'imageURL':product.imageURL,
                
                },
            'quantity':cart[i]['quantity'],
            'total':total,  
  
        }
        item.append(item_cart)
    return {'cartItems':cartItems,'order':order,'item':item}