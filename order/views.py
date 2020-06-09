from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from datetime import datetime
import string
from account.models import Account
import random
from decimal import Decimal
# Create your views here.


@login_required
def checkout(request):
    account = Account.objects.get(user=request.user)
    if account.address == '' or account.area == '' or account.city == '' or account.state == '' or account.pincode == '':
        messages.error(request, 'Complete Your profile')
        return redirect('edit-profile')
    cart = Cart.objects.get(user=request.user)
    cartitem = CartItem.objects.filter(cart=cart)
    now = datetime.now()
    d = now.strftime("%Y-%m-%d %H:%M")
    order = Order(customer=request.user, shop_user=cartitem[0].product.user.username, orderid=id_generator(), date=d)
    order.save()
    order.subtotal = cart.total
    order.save()
    for i in range(len(cartitem)):
        order_item = OrderItem(order=order, product=cartitem[i].product, quantity=cartitem[i].quantity, price=cartitem[i].line_total)
        order_item.save()
    cart.delete()
    return redirect('order-view', order.id)


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    the_id = "".join(random.choice(chars) for x in range(size))
    try:
        order = Order.objects.get(order_id=the_id)
        id_generator()
    except:
        return the_id

@login_required
def order_list(request):
    account = Account.objects.get(user=request.user)
    if account.category == 'customer':
        order = Order.objects.filter(customer=request.user)
    elif account.category == 'shopkeeper':
        order = Order.objects.filter(shop_user=request.user.username)
    elif request.user.is_superuser:
        order = Order.objects.all()
    else:
        messages.error(request, 'You cannot perform this operation')
        return redirect('home')
    if len(order) == 0:
        data = {'empty': True}
    else:
        data = {'empty': False}
    data['order'] = order
    return render(request, 'order/order_list.html', data)


@login_required
def order_view(request, pk):
    order = Order.objects.get(pk=pk)
    if request.method == 'POST':
        shipping = request.POST['delivery']
        order.shipping = Decimal(shipping)
        order.finaltotal = order.shipping+order.subtotal
        order.status = 'started'
        order.save()
    account = Account.objects.get(user=request.user)
    customer = Account.objects.get(user=order.customer)
    shopkeeper = Account.objects.get(username=order.shop_user)
    context = {'order': order, 'account': account, 'customer': customer, 'shopkeeper': shopkeeper}
    return render(request, 'order/order_view.html', context)


@login_required
def canceled(request,pk):
    order = Order.objects.get(pk=pk)
    order.status = 'canceled'
    order.save()
    return redirect('order-view', pk)


@login_required
def finished(request, pk):
    order = Order.objects.get(pk=pk)
    order.status = 'finished'
    order.save()
    return redirect('order-view', pk)
