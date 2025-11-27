from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect

from core.forms import OperationForm
from core.models import BankAccount, Operation
from core.views import bank_account


def operation_search(request):
    pass


@login_required
def operation_list(request, bank_account_id):
    bank_account = get_object_or_404(BankAccount, pk=bank_account_id)
    if not bank_account.user == request.user:
        raise PermissionDenied

    if request.method == "POST":
        form = OperationForm(request.POST, user=request.user)
        if form.is_valid():
            date = form.cleaned_data["date"]
            third = form.cleaned_data["third"]
            category = form.cleaned_data["category"]
            value = form.cleaned_data["value"]
            periodicity = form.cleaned_data["periodicity"]
            operation, _ = Operation.objects.get_or_create(
                date=date,
                third=third,
                category=category,
                value=value,
                status="S",
                periodicity=periodicity,
                account=bank_account,
            )

            return redirect("operation_list", bank_account_id=bank_account.pk)
        else:
            context = {"form": form}
            response = render(
                request, "operation/partials/operation_form.html", context
            )
            response["HX-Retarget"] = "#operation-form"
            response["HX-Reswap"] = "outerHTML"
            return response

    operation_list = Operation.objects.filter(account_id=bank_account_id).all()
    balance = 0
    for operation in operation_list:
        balance += operation.value
        operation.balance = balance
    context = {
        "operation_list": operation_list,
        "bank_account": bank_account,
        "form": OperationForm(),
    }
    return render(request, "operation/list.html", context)


@login_required
def operation_add(request):
    context = {}
    return render(request, "operation/add.html", context)


def operation_edit(request):
    pass


@login_required
def operation_delete(request, operation_id):
    operation = Operation.objects.get(pk=operation_id)
    print(operation.__dict__)
    bank_account = operation.account
    operation.delete()
    return redirect("operation_list", bank_account_id=bank_account.pk)
