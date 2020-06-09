from django.contrib import admin
from .models import Account, TempAccount, Token
# Register your models here.

admin.site.register(Account)
admin.site.register(TempAccount)
admin.site.register(Token)