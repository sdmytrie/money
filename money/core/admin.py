from django.contrib import admin

from core.models import BankAccount, Category, Operation, Third, User

admin.site.register(BankAccount)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Operation)
admin.site.register(Third)
