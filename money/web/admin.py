from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from web.models import Bank, User


class MoneyUserAdmin(UserAdmin):
    pass


class BankAdmin(admin.ModelAdmin):
    list_display = ["name", "user"]
    search_fields = ["name"]
    readonly_fields = [
        "user",
    ]

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ["user"]
        else:
            return []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


admin.site.register(User, MoneyUserAdmin)
admin.site.register(Bank, BankAdmin)
