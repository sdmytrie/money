from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "bank-account/search/",
        views.bank_account.bank_account_search,
        name="bank_account_search",
    ),
    path(
        "bank-account/list/",
        views.bank_account.bank_account_list,
        name="bank_account_list",
    ),
    path(
        "operation/list/<int:bank_account_id>",
        views.operation.operation_list,
        name="operation_list",
    ),
]
