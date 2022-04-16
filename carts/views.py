from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponse

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    # current_user = request.user
    product = Product.objects.get(id=product_id) #get the product
    # If the user is authenticated
    # if current_user.is_authenticated:
    #     product_variation = []
    #     if request.method == 'POST':
    #         for item in request.POST:
    #             key = item
    #             value = request.POST[key]

    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        # variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
        # product_variation.append(variation)
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    try:
        cart_item=CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity+=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
             )
        cart_item.save()
  
    return redirect('cart')



def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,

    }
        
    return render(request,'store/cart.html',context)


