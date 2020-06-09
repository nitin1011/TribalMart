from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Account, TempAccount, Token
import base64
from datetime import datetime, timedelta, timezone
import string
import random as random12
from random import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import auth
from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.auth.decorators import login_required
from product.models import Product
from .models import Account
# Create your views here.


def home(request):
    product = Product.objects.all()
    context = {'product': product[:6]}
    try:
        account = Account.objects.get(user=request.user)
    except:
        account = None
    context['account'] = account
    return render(request, 'account/home.html', context)


def get_otp():
    otp = int(random()*1000000)
    try:
        temp = TempAccount.objects.get(otp=otp)
    except:
        temp = None
    if temp is not None:
        get_otp()
    else:
        return otp


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']
        password2 = request.POST['password2']
        category = request.POST['category']
        if 'terms' in request.POST:
            if password == password2:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'That username is taken')
                    return redirect('register')
                else:
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'That email is already being used ')
                        return redirect('register')
                    else:
                        if len(mobile) != 10 or not str(mobile).isdigit():
                            messages.error(request, 'Mobile no. is incorrect')
                            return redirect('register')
                        else:
                            otp = get_otp()
                            pas = base64.b64encode(password.encode("utf-8"))
                            pas = str(pas)
                            pas = pas[2:len(pas) - 1]
                            ex = datetime.now() + timedelta(seconds=300)
                            temp = TempAccount(username=username, email=email, mobile=mobile,
                                               otp=otp, password=pas, expire=ex, category=category)

                            temp.save()
                            subject = 'Tribalmart verification mail'
                            message = 'Welcome to Tribalmart\nplease enter this otp to verify your email\n' + str(
                                otp) + ''
                            from_email = settings.EMAIL_HOST_USER
                            tolist = [email]
                            send_mail(subject, message, from_email, tolist)
                            return redirect('otp')
            else:
                messages.error(request, 'Password do not match')
                return redirect('register')
        else:
            messages.error(request, 'you have to accept the Terms and Conditions')
            return redirect('register')
    else:
        return render(request, 'account/register.html')


def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        try:
            temp = TempAccount.objects.get(otp=otp)
        except:
            temp = None
        if temp is not None:
            password = base64.b64decode(temp.password).decode("utf-8")
            user = User.objects.create_user(username=temp.username, password=password)
            user.save()
            account = Account(user=user, username=temp.username, email=temp.email, mobile=temp.mobile,
                              category=temp.category)
            account.save()
            temp.delete()
            messages.success(request, 'Your Account has been created Successfully')
            return redirect('login')
        else:
            messages.error(request, 'Invalid otp')
    else:
        return render(request, 'account/otp.html')


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_otp, 'interval', seconds=300)
    scheduler.add_job(check_token, 'interval', hours=20)
    scheduler.start()


def check_otp():
    temp = TempAccount.objects.all()
    for i in temp:
        dt = datetime.now()
        dt = dt.replace(tzinfo=timezone.utc)
        if i.expire < dt:
            i.delete()


def check_token():
    token = Token.objects.all()
    for i in token:
        dt = datetime.now()
        dt = dt.replace(tzinfo=timezone.utc)
        if i.date < dt:
            i.delete()


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        category = request.POST['category']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            account = Account.objects.get(user=user)
            if account.category == category:
                auth.login(request, user)
                return redirect('home')
            else:
                s = "you are not " + str(category)
                messages.error(request, s)
                return redirect('login')
        else:
            messages.error(request, 'Username/Password is incorrect')
            return redirect('login')
    else:
        return render(request, 'account/login.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required
def view_profile(request):
    account = Account.objects.get(user=request.user)
    context = {'account': account}
    return render(request, 'account/view_profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        mobile = request.POST['mobile']
        state = request.POST['state']
        pincode = request.POST['pincode']
        city = request.POST['city']
        area = request.POST['area']
        address = request.POST['address']
        account = Account.objects.get(user=request.user)
        if Account.objects.filter(email=email).exists() and account.email != email:
            messages.error(request, 'That email is already being used ')
            return redirect('edit-account')
        else:
            if Account.objects.filter(mobile=mobile).exists() and account.mobile != mobile:
                messages.error(request, 'That mobile is already being used ')
                return redirect('edit-account')
            else:
                account.firstname = firstname
                account.lastname = lastname
                account.email = email
                account.mobile = mobile
                account.state = state
                account.pincode = pincode
                account.city = city
                account.area = area
                account.address = address
                account.save()
                return redirect('view-profile')
    else:
        account = Account.objects.get(user=request.user)
        context = {'account': account}
        return render(request, 'account/edit_profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        oldpass = request.POST['oldpass']
        newpass = request.POST['newpass']
        newpassconfirm = request.POST['newpassconfirm']
        username = request.user.username
        user = auth.authenticate(username=username, password=oldpass)
        if user is not None:
            if newpass == newpassconfirm:
                user.set_password(newpass)
                user.save()
                return redirect('login')
            else:
                messages.error(request, 'password do not match')
                return redirect('change-password')
        else:
            messages.error(request, 'Wrong password')
            return redirect('change-password')
    else:
        return render(request, 'account/change_password.html')


def get_token(size=20, chars=string.ascii_lowercase + string.digits):
    the_id = "".join(random12.choice(chars) for x in range(size))
    try:
        token = Token.objects.get(token=the_id)
        get_token()
    except:
        return the_id


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        account = Account.objects.get(email=email)
        user = User.objects.get(username=account.username)
        token = Token(token=get_token(), user=user, date=datetime.now() + timedelta(hours=1))
        token.save()
        subject = 'Tribalmart Mail'
        message = 'Please click the below link to reset your password \nhttp://localhost:8000/account/reset/' + str(token.token)
        from_email = settings.EMAIL_HOST_USER
        tolist = [email]
        send_mail(subject, message, from_email, tolist)
        return redirect('login')
    else:
        return render(request, 'account/forgot_password.html')


def reset_password(request, token):
    try:
        token = Token.objects.get(token=token)
    except:
        messages.error(request, 'invalid link')
        return redirect('login')
    user = token.user
    if request.method == 'POST':
        p1 = request.POST['password1']
        p2 = request.POST['password2']
        if p1 == p2:
            user.set_password(p1)
            token.delete()
            user.save()
            return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('reset-password', token)
    else:
        return render(request, 'account/reset_password.html')


def search_product(query_list):
    products = Product.objects.all()
    prod = []
    if len(query_list) == 0:
        return products
    else:
        for i in query_list:
            for j in range(len(products)):
                if (i.lower() in products[j].product_name.lower() or i.lower() in products[j].product_category.lower()) and products[j] not in prod:
                    prod.append(products[j])
        return prod


def search(request):
    context = {}
    if request.method == 'GET':
        query = request.GET.get('q')
        query_list = query.split()
        context['query'] = query
        # lookups = Q(product_name__icontains=query) | Q(product_category__icontains=query)
        # products = Products.objects.filter(lookups).distinct()
        products = search_product(query_list)
        if len(products) == 0:
            context['empty'] = True
        else:
            context['empty'] = False
        context['object_list'] = products
        return render(request, 'account/view.html', context)
    else:
        return render(request, 'account/view.html', context)
