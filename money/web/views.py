"""views"""

from pprint import pprint

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
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
    return render(request, "registration/login.html", {'form': form })


@login_required(redirect_field_name=None)
def index(request):
    """index"""
    context = {"form": BankForm()}
    return render(request, "web/index.html", context)
