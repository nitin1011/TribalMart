from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from account.models import Account
# Create your views here.


def user_list(request):
    if request.user.is_superuser:
        users = User.objects.all()
        context = {'users': users}
        return render(request, 'admindashboard/user_list.html', context)
    else:
        messages.error(request, 'you can not perform this operation')
        return redirect('login')


def user_view(request, pk):
    if request.user.is_superuser:
        account = Account.objects.get(pk=pk)
        context = {'account': account}
        return render(request, 'admindashboard/user_view.html', context)
    else:
        messages.error(request, 'you can not perform this operation')
        return redirect('login')


