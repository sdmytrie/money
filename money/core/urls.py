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
    path(
        "operation/delete/<int:operation_id>",
        views.operation.operation_delete,
        name="operation_delete",
    ),
    path(
        "third/search",
        views.third.third_get_by_name,
        name="third_get_by_name",
    ),
    path(
        "third/add/<str:motif>",
        views.third.third_add,
        name="third_add",
    ),
    path(
        "category/search",
        views.category.category_get_by_name,
        name="category_get_by_name",
    ),
    path(
        "category/add/<str:motif>",
        views.category.category_add,
        name="category_add",
    ),
]
