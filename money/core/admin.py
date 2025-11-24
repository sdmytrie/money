from django.contrib import admin

from core.models import BankAccount, User

admin.site.register(User)
admin.site.register(BankAccount)
