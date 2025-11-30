from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect

from core.forms.third import ThirdForm
from core.models import Third


@login_required()
def third_get_by_name(request):
    motif = request.POST.get("third")
    third_list = Third.objects.filter(
        name__icontains=motif, user=request.user
    ).order_by("name")

    context = {"third_list": third_list, "motif": motif}
    return render(request, "third/partials/third_search_table.html", context)


@login_required()
def third_edit(request, third_id):
    third = get_object_or_404(Third, pk=third_id)
    if not third.user == request.user:
        raise PermissionDenied

    form = ThirdForm(
        user=request.user,
        initial={
            "name": third.name,
        },
    )
    third_list = Third.objects.filter(user=request.user).order_by("name")

    if request.method == "POST":
        form = ThirdForm(request.POST, user=request.user)
        if form.is_valid():
            third.name = form.cleaned_data["name"]
            third.save()
            return redirect(
                "third_list",
            )
        else:
            context = {
                "third_list": third_list,
                "action": "EDIT",
                "third": third,
                "form": form,
            }
            return render(request, "third/list.html", context)

    context = {"third_list": third_list, "action": "EDIT", "third": third, "form": form}
    return render(request, "third/edit.html", context)


@login_required()
def third_list(request):
    third_list = Third.objects.filter(user=request.user).order_by("name")

    if request.method == "POST":
        form = ThirdForm(request.POST, user=request.user)
        if form.is_valid():
            name = form.cleaned_data["name"]
            third, _ = Third.objects.get_or_create(name=name, user=request.user)
            return redirect("third_list")
        else:
            context = {"form": form, "third_list": third_list}
            response = render(request, "third/list.html", context)
            return response
    context = {"action": "ADD", "form": ThirdForm(), "third_list": third_list}
    return render(request, "third/list.html", context)


@login_required
def third_delete(request, third_id):
    third = get_object_or_404(Third, pk=third_id)
    if not third.user == request.user:
        raise PermissionDenied
    third.delete()
    return redirect("third_list")


@login_required()
def third_add(request, motif):
    if request.htmx:
        third, created = Third.objects.get_or_create(
            name=motif.upper(), user=request.user
        )
        if created:
            response = {
                "views": "third_add",
                "message": f"Third {motif.upper()} added.",
            }
        else:
            response = {
                "views": "third_add",
                "message": f"Third {motif.upper()} exists.",
            }
        return JsonResponse(response)
    else:
        raise PermissionDenied
