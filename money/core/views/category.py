from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

from core.models import Category


@login_required()
def category_get_by_name(request):
    motif = request.POST.get("category")
    category_list = Category.objects.filter(name__icontains=motif).order_by("name")

    context = {"category_list": category_list, "motif": motif}
    return render(request, "category/partials/category_search_table.html", context)


@login_required()
def category_add(request, motif):
    if request.htmx:
        category, created = Category.objects.get_or_create(
            name=motif.upper(), user=request.user
        )
        if created:
            response = {
                "views": "category_add",
                "message": f"Category {motif.upper()} added.",
            }
        else:
            response = {
                "views": "category_add",
                "message": f"Category {motif.upper()} exists.",
            }
        return JsonResponse(response)
    else:
        raise PermissionDenied
