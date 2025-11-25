from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Operation


def operation_search(request):
    pass


def operation_list(request, bank_account_id):
    operation_list = Operation.objects.filter(account_id=bank_account_id).all()
    context = {"operation_list": operation_list}
    return render(request, "operation/list.html", context)


def operation_add(request):
    pass


def operation_edit(request):
    pass


def operation_delete(request):
    pass
