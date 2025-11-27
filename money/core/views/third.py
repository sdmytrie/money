from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

from core.models import Third


@login_required()
def third_get_by_name(request):
    motif = request.POST.get("third")
    third_list = Third.objects.filter(name__icontains=motif).order_by("name")

    context = {"third_list": third_list, "motif": motif}
    return render(request, "third/partials/third_search_table.html", context)


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
