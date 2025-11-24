from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import BankAccount


def bank_account_search(request):
    pass


def bank_account_list(request):
    bank_account_list = BankAccount.objects.filter(user=request.user).all()
    context = {"bank_account_list": bank_account_list}
    return render(request, "bank_account/list.html", context)


def bank_account_add(request):
    pass


def bank_account_edit(request):
    pass


def bank_account_delete(request):
    pass
