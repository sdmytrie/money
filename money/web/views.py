"""views"""

from pprint import pprint

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from web.forms import BankForm, RegistrationForm
from web.models import Bank


def money_login(request):
    """login to money"""
    form = RegistrationForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return redirect("index")
    return render(request, "registration/login.html", {"form": form})


@login_required(redirect_field_name=None)
def index(request):
    """index"""
    banks = Bank.objects.filter(user=request.user)
    context = {"form": BankForm(), "banks": banks}
    return render(request, "web/index.html", context)


# @login_required(redirect_field_name=None)
# def banks(request):
#     banks = Bank.models.filter(user=request.user)
#     context = {"banks": banks}


@login_required(redirect_field_name=None)
def create_banks(request):
    if request.META.get('HTTP_HX_REQUEST'):
        
        if request.method == "POST":
            form = BankForm(request.POST or None)
            if form.is_valid():
                bank = Bank()
                bank.name = form.cleaned_data["name"]
                bank.user = request.user
                bank.save()
        banks = Bank.objects.filter(user=request.user)
        context = {"form": BankForm(), "banks": banks}
        return render(request, "web/sidebar.html", context)
    else:
        raise Http404
    
