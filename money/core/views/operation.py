from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render

from core.models import BankAccount, Operation
from core.forms import OperationForm


def operation_search(request):
    pass


@login_required
def operation_list(request, bank_account_id):
    if request.method == "POST":
        form = OperationForm(request.POST, user=request.user)
        if form.is_valid():
            date = form.cleaned_data["date"]
            tier = form.cleaned_data["tier"]
            book, _ = Operation.objects.get_or_create(date=date, tier=tier)

            if not request.user.books.filter(id=book.id).exists():
                request.user.books.add(book)
                return render(request, "partials/book-row.html", {"book": book})
        else:
            context = {"form": form}
            response = render(request, "partials/book-form.html", context)
            response["HX-Retarget"] = "#book-form"
            response["HX-Reswap"] = "outerHTML"
            return response

    bank_account = get_object_or_404(BankAccount, pk=bank_account_id)
    if not bank_account.user == request.user:
        raise PermissionDenied

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


def operation_delete(request):
    pass
