from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from account.models import Account
from django.contrib import messages
from .models import Product, Review
from order.models import OrderItem, Order
# Create your views here.


@login_required
def add_product(request):
    account = Account.objects.get(user=request.user)
    if account.address == '' or account.area == '' or account.city == '' or account.state == '' or account.pincode == '':
        messages.error(request, 'Complete Your profile')
        return redirect('edit-profile')
    if account.category != 'shopkeeper':
        messages.error(request, 'You can not add product')
        return redirect('home')
    else:
        if request.method == 'POST':
            product_name = request.POST['name']
            product_category = request.POST['category']
            product_price = request.POST['price']
            product_discount = request.POST['discount']
            product_image = request.FILES['image']
            product_disc = request.POST['disc']

            product = Product(user=request.user, product_name=product_name, product_category=product_category,
                              product_price=product_price,product_discount=product_discount,
                              product_image=product_image, product_disc=product_disc)
            product.save()
            return redirect('view-profile')
        else:
            return render(request, 'product/add_product.html')


@login_required
def all_product(request):
    account = Account.objects.get(user=request.user)
    if account.category == 'shopkeeper':
        user = request.user
        context = {'products': user.product_set.all()}
        return render(request, 'product/all_product.html', context)
    else:
        return redirect('home')


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    try:
        account = Account.objects.get(user=request.user)
    except:
        account = None
    try:
        review = Review.objects.filter(product=product)
    except:
        review = None
    if request.method == 'POST':
        product.product_image = request.FILES['image']
        product.save()
    context = {'product': product, 'account': account, 'review': review}
    return render(request, 'product/product_detail.html', context)


@login_required
def edit_product(request, pk):
    product = Product.objects.get(pk=pk)
    context = {'product': product}
    account = Account.objects.get(user=request.user)
    if account.category != 'shopkeeper':
        messages.error(request, 'your are not shopkeeper')
        return redirect('home')
    if request.method == 'POST':
        product.product_name = request.POST['name']
        product.product_category = request.POST['category']
        product.product_price = request.POST['price']
        product.product_discount = request.POST['discount']
        product.product_disc = request.POST['discription']
        product.save()
        return redirect('product-detail', product.id)
    else:
        return render(request, 'product/edit_product.html', context)


@login_required
def delete_product(request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return redirect('home')


@login_required
def review(request,pk):
    product = Product.objects.get(pk=pk)
    orderitem = OrderItem.objects.filter(product=product)
    flag = False
    for i in orderitem:
        if i.order.customer == request.user:
            flag = True
            break
    if flag:
        if request.method == 'POST':
            rating = request.POST['rating']
            comment = request.POST['comment']
            review = Review(user=request.user, product=product, rating=rating, comment=comment)
            review.save()
            return redirect('product-detail', pk)
        else:
            return render(request, 'product/review.html')
    else:
        messages.error(request, 'you cannot give review')
        return redirect('product-detail', pk)

