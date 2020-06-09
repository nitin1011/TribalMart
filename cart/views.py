from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from account.models import Account
from django.contrib import messages
from product.models import Product
from .models import CartItem, Cart
# Create your views here.


@login_required
def view_cart(request):
    account = Account.objects.get(user=request.user)
    if account.category != 'customer':
        st = 'You are ' + account.category + ". You cannot buy the product"
        messages.error(request, st)
        return redirect('login')
    try:
        new_cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        new_cart = Cart()
        new_cart.user = request.user
        new_cart.save()
    except:
        new_cart = None
    if new_cart:
        if new_cart.cartitem_set.count() == 0:
            context = {'empty': True, 'message': 'Your cart is empty'}
        else:
            context = {'cart': new_cart}
    else:
        context = {'empty': True, 'message': 'Your cart is empty'}
    return render(request, 'cart/view_cart.html', context)


@login_required
def update_cart(request, pk):
    account = Account.objects.get(user=request.user)
    if account.category != 'customer':
        st = 'You are ' + account.category + ". You cannot buy the product"
        messages.error(request, st)
        return redirect('product-detail', pk)
    try:
        qty = request.GET.get('qty')
        if len(qty) == 0:
            qty = 1
        update_qty = True
    except:
        qty = None
        update_qty = False

    try:
        # the_id = request.session['cart_id']
        new_cart = Cart.objects.get(user=request.user)
    except:
        new_cart = Cart()
        new_cart.user = request.user
        new_cart.save()

    product = Product.objects.get(pk=pk)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, cart=new_cart, product=product)
    if created:
        new_cart.item_count = new_cart.cartitem_set.count()
    if update_qty:
        if int(qty) == 0:
            cart_item.delete()
        elif int(qty) < 0:
            messages.error(request, "You can't add negative no. of quantity into the cart ")
            return redirect('product-detail', pk)
        else:
            cart_item.quantity = qty
            price = cart_item.product.product_price-(cart_item.product.product_price*(cart_item.product.product_discount/100))
            cart_item.line_total = price*int(cart_item.quantity)
            cart_item.save()
    else:
        pass

    new_total = 0.00
    request.session['item_count'] = new_cart.cartitem_set.count()
    for i in new_cart.cartitem_set.all():
        sp = i.product.product_price - (i.product.product_price*(i.product.product_discount/100))
        line_total = float(sp) * i.quantity
        new_total += float(line_total)
    new_cart.total = new_total
    new_cart.save()
    return redirect('view-cart')
