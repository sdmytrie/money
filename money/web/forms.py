"""Forms"""

from pprint import pprint

from crispy_forms.bootstrap import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth import authenticate
from django.urls import reverse_lazy
from web.models import Bank


class RegistrationForm(forms.Form):
    """Registration"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "registration-form"
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Sign In"))

    username = forms.CharField(widget=forms.TextInput(), required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError(
                "Sorry, that login was invalid. Please try again."
            )
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        return user


class BankForm(forms.ModelForm):
    """Bank"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.form_id = "bank-form"
        # self.helper.form_method = "post"
        self.helper.attrs = {
            "hx-post": reverse_lazy("create-banks"),
            "hx-target": "#sidebar"
        }
        self.helper.layout = Layout(
            Div(
                Div(
                    "name",
                    css_class="col-8",
                ),
                Div(
                    Submit("submit", "ADD"),
                    css_class="col align-self-top",
                ),
                css_class="row mt-2 d-none",
            ),
        )

    class Meta:
        model = Bank
        fields = ("name",)
        widgets = {"name": forms.TextInput()}
