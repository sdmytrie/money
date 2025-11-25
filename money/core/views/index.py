from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import BankAccount


@login_required
def index(request):
    bank_account_list = BankAccount.objects.filter(user=request.user).all()
    context = {"bank_account_list": bank_account_list}
    return render(request, "index.html", context)
