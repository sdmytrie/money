from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect

from core.forms.category import CategoryForm
from core.models import Category


@login_required()
def category_get_by_name(request):
    motif = request.POST.get("category")
    category_list = Category.objects.filter(
        name__icontains=motif, user=request.user
    ).order_by("name")

    context = {"category_list": category_list, "motif": motif}
    return render(request, "category/partials/category_search_table.html", context)


@login_required()
def category_edit(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if not category.user == request.user:
        raise PermissionDenied

    form = CategoryForm(
        user=request.user,
        initial={
            "name": category.name,
        },
    )
    category_list = Category.objects.filter(user=request.user).order_by("name")

    if request.method == "POST":
        form = CategoryForm(request.POST, user=request.user)
        if form.is_valid():
            category.name = form.cleaned_data["name"]
            category.save()
            return redirect(
                "category_list",
            )
        else:
            context = {
                "category_list": category_list,
                "action": "EDIT",
                "category": category,
                "form": form,
            }
            return render(request, "category/list.html", context)

    context = {
        "category_list": category_list,
        "action": "EDIT",
        "category": category,
        "form": form,
    }
    return render(request, "category/edit.html", context)


@login_required()
def category_list(request):
    category_list = Category.objects.filter(user=request.user).order_by("name")

    if request.method == "POST":
        form = CategoryForm(request.POST, user=request.user)
        if form.is_valid():
            name = form.cleaned_data["name"]
            category, _ = Category.objects.get_or_create(name=name, user=request.user)
            return redirect("category_list")
        else:
            context = {"form": form, "category_list": category_list}
            response = render(request, "category/list.html", context)
            return response
    context = {"action": "ADD", "form": CategoryForm(), "category_list": category_list}
    return render(request, "category/list.html", context)


@login_required
def category_delete(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if not category.user == request.user:
        raise PermissionDenied
    category.delete()
    return redirect("category_list")


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
