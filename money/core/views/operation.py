from copy import deepcopy
from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import QueryDict
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect

from core.forms import OperationForm
from core.models import BankAccount, Operation
from core.views import bank_account


def operation_search(request):
    pass


@login_required
def operation_list(request, bank_account_id, status):
    bank_account = get_object_or_404(BankAccount, pk=bank_account_id)
    if not bank_account.user == request.user:
        raise PermissionDenied

    operation_list = Operation.objects.filter(
        account_id=bank_account, status__in=["S", "A", "R"]
    ).all()
    balance = 0
    default_status_list = ["S", "A"]
    if status == "R":
        default_status_list.append(status)
    for operation in filter(lambda o: o.status in default_status_list, operation_list):
        balance += operation.value
        operation.balance = float(balance)

    if request.method == "POST":
        form = OperationForm(request.POST, user=request.user)
        if form.is_valid():
            date = form.cleaned_data["date"]
            third = form.cleaned_data["third"]
            category = form.cleaned_data["category"]
            value = form.cleaned_data["value"]
            periodicity = form.cleaned_data["periodicity"]
            status = "S"
            if int(periodicity) > 0:
                status = "R"
            operation, _ = Operation.objects.get_or_create(
                date=date,
                third=third,
                category=category,
                value=value,
                status=status,
                periodicity=periodicity,
                account=bank_account,
            )

            return redirect(
                "operation_list", bank_account_id=bank_account.pk, status=status
            )
        else:
            context = {
                "action": "ADD",
                "operation_list": filter(lambda o: o.status == status, operation_list),
                "status": status,
                "bank_account": bank_account,
                "form": form,
            }
            return render(request, "operation/list.html", context)

    context = {
        "action": "ADD",
        "operation_list": filter(lambda o: o.status == status, operation_list),
        "status": status,
        "bank_account": bank_account,
        "form": OperationForm(),
    }
    return render(request, "operation/list.html", context)


@login_required
def operation_edit(request, operation_id):
    operation = get_object_or_404(Operation, pk=operation_id)
    if not operation.account.user == request.user:
        raise PermissionDenied

    form = OperationForm(
        user=request.user,
        initial={
            "date": operation.date,
            "third": operation.third.name,
            "category": operation.category.name,
            "value": operation.value,
            "periodicity": operation.periodicity,
            "account": operation.account,
        },
    )

    operation_list = Operation.objects.filter(
        account_id=operation.account.pk, status__in=["S", "A", "R"]
    ).all()
    balance = 0
    for buffer in filter(lambda o: o.status in ["S", "A"], operation_list):
        balance += buffer.value
        operation.balance = float(balance)

    if request.method == "POST":
        form = OperationForm(request.POST, user=request.user)
        if form.is_valid():
            operation.date = form.cleaned_data["date"]
            operation.third = form.cleaned_data["third"]
            operation.category = form.cleaned_data["category"]
            operation.value = form.cleaned_data["value"]
            operation.periodicity = form.cleaned_data["periodicity"]
            if int(operation.periodicity) > 0:
                operation.status = "R"
            operation.save()
            return redirect(
                "operation_list",
                bank_account_id=operation.account.pk,
                status=operation.status,
            )
        else:
            context = {
                "action": "EDIT",
                "operation_list": operation_list,
                "operation": operation,
                "status": operation.status,
                "bank_account": operation.account,
                "form": form,
            }
            return render(request, "operation/list.html", context)

    context = {
        "form": form,
        "operation": operation,
        "bank_account": operation.account,
    }
    return render(request, "operation/edit.html", context)


@login_required
def operation_delete(request, operation_id, status):
    operation = get_object_or_404(Operation, pk=operation_id)
    bank_account = operation.account
    operation.delete()
    return redirect("operation_list", bank_account_id=bank_account.pk, status=status)


@login_required
def operation_check(request, operation_id, status):
    operation = get_object_or_404(Operation, pk=operation_id)
    if status in ["A", "S"]:
        operation.checked = not operation.checked
        operation.save()
    elif status == "R":
        new_operation = Operation()
        new_operation.date = operation.date
        new_operation.status = "S"
        new_operation.third = operation.third
        new_operation.category = operation.category
        new_operation.account = operation.account
        new_operation.value = operation.value
        new_operation.save()
        operation.date = operation.date + relativedelta(months=operation.periodicity)
        operation.save()
        operation_list = Operation.objects.filter(
            account_id=operation.account.pk, status__in=["S", "A", "R"]
        ).all()
        balance = 0
        for operation in filter(lambda o: o.status in ["S", "A"], operation_list):
            balance += operation.value
            operation.balance = balance
        context = {
            "action": "ADD",
            "operation_list": filter(lambda o: o.status == status, operation_list),
            "status": status,
            "bank_account": operation.account,
            "form": OperationForm(),
        }
        return render(request, "operation/list.html", context)
    response = HttpResponse(status=204)
    response["HX-Trigger"] = "operation-check"
    return response


@login_required
def operation_archive(request, operation_id, status):
    operation = get_object_or_404(Operation, pk=operation_id)
    if status == "S":
        operation.status = "A"
        operation.save()
    balance = 0
    operation_list = Operation.objects.filter(
        account_id=operation.account.pk, status__in=["S", "A", "R"]
    ).all()
    for operation in filter(lambda o: o.status in ["S", "A"], operation_list):
        balance += operation.value
        operation.balance = balance
    context = {
        "action": "ADD",
        "operation_list": filter(lambda o: o.status == status, operation_list),
        "status": status,
        "bank_account": operation.account,
        "form": OperationForm(),
    }
    return render(request, "operation/list.html", context)
