from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from web.models import User


class MoneyUserAdmin(UserAdmin):
    pass

admin.site.register(User, MoneyUserAdmin)
