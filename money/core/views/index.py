from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import BankAccount


@login_required
def index(request):
    bank_account_list = BankAccount.objects.filter(user=request.user).all()
    for account in bank_account_list:
        balance = 0
        balance_prev = 0
        for operation in filter(
            lambda o: o.status in ["S", "A"], account.operations.all()
        ):
            balance += operation.value
            operation.balance = balance
        for operation in account.operations.all():
            balance_prev += operation.value
            operation.balance_prev = balance_prev
        account.balance = balance
        account.balance_prev = balance_prev
    context = {"bank_account_list": bank_account_list}
    return render(request, "index.html", context)
