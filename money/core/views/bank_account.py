from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect

from core.forms import BankAccountForm
from core.models import BankAccount


def bank_account_search(request):
    pass


@login_required()
def bank_account_edit(request, bank_account_id):
    bank_account = get_object_or_404(BankAccount, pk=bank_account_id)
    if not bank_account.user == request.user:
        raise PermissionDenied

    form = BankAccountForm(
        user=request.user,
        initial={
            "name": bank_account.name,
        },
    )
    bank_account_list = BankAccount.objects.filter(user=request.user).order_by("name")

    if request.method == "POST":
        form = BankAccountForm(request.POST, user=request.user)
        if form.is_valid():
            bank_account.name = form.cleaned_data["name"]
            bank_account.save()
            return redirect(
                "bank_account_list",
            )
        else:
            context = {
                "bank_account_list": bank_account_list,
                "action": "EDIT",
                "bank_account": bank_account,
                "form": form,
            }
            return render(request, "bank_account/list.html", context)

    context = {
        "bank_account_list": bank_account_list,
        "action": "EDIT",
        "bank_account": bank_account,
        "form": form,
    }
    return render(request, "bank_account/edit.html", context)


@login_required()
def bank_account_list(request):
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
    if request.method == "POST":
        form = BankAccountForm(request.POST, user=request.user)
        if form.is_valid():
            name = form.cleaned_data["name"]
            bank_account, _ = BankAccount.objects.get_or_create(
                name=name, user=request.user
            )
            return redirect("bank_account_list")
        else:
            context = {"form": form, "bank_account_list": bank_account_list}
            response = render(request, "bank_account/list.html", context)
            return response
    context = {
        "action": "ADD",
        "form": BankAccountForm(),
        "bank_account_list": bank_account_list,
    }
    return render(request, "bank_account/list.html", context)


@login_required
def bank_account_delete(request, bank_account_id):
    bank_account = get_object_or_404(BankAccount, pk=bank_account_id)
    if not bank_account.user == request.user:
        raise PermissionDenied
    bank_account.delete()
    return redirect("bank_account_list")
