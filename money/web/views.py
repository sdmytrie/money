"""views"""

from pprint import pprint

from crispy_forms.utils import render_crispy_form
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template.context_processors import csrf
from web.forms import RegistrationForm


def money_login(request):
    """login to money"""
    if request.method == "GET":
        context = {"form": RegistrationForm()}
        return render(request, "registration/login.html", context)
    elif request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                template = render(request, 'web/index.html')
                template['Hx-Push'] = '/'
                login(request, user)
                # return render(request, "web/index.html")
                return template

        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return HttpResponse(form_html)


# @login_required
def index(request):
    """index"""
    context = {}
    return render(request, "web/index.html", context)
