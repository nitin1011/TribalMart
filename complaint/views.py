from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from account.models import Account
from .models import Complaint
from django.contrib.auth.admin import settings
# Create your views here.


@login_required
def complaint_register(request):
    if request.method == 'POST':
        orderid = request.POST['orderid']
        complaint = request.POST['complaint']
        comp = Complaint(user=request.user, orderid=orderid, complaint=complaint)
        comp.save()
        return redirect('complaint-list')
    else:
        return render(request, 'complaint/complaint_register.html')


@login_required
def complaint_list(request):
    if request.user.account.category == 'customer':
        try:
            complaint = Complaint.objects.filter(user=request.user)
        except:
            complaint = None
    elif request.user.account.category == 'cra' or request.user.is_superuser:
        try:
            complaint = Complaint.objects.all()
        except:
            complaint = None
    else:
        messages.error(request, 'You cannot perform this operation ')
    context = {'complaint': complaint}
    return render(request, 'complaint/complaint_list.html', context)


@login_required
def complaint_view(request, pk):
    complaint = Complaint.objects.get(pk=pk)
    context = {'complaint': complaint}
    return render(request, 'complaint/complaint_view.html', context)


@login_required
def reply(request, pk):
    if request.user.account.category == 'cra':
        if request.method == 'POST':
            message = request.POST['message']
            complaint = Complaint.objects.get(pk=pk)
            subject = 'Tribalmart reply'
            from_email = settings.EMAIL_HOST_USER
            tolist = [complaint.user.account.email]
            send_mail(subject, message, from_email, tolist)
            complaint.reply = message
            complaint.replied = request.user.username
            complaint.status = 'replied'
            complaint.save()
            return redirect('complaint-list')
        else:
            return render(request, 'complaint/reply.html')
    else:
        messages.error(request, 'you are not customer review assistent')
        return redirect('home')
