"""Forms"""

from datetime import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.urls import reverse_lazy


class RegistrationForm(forms.Form):
    """Registration"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "registration-form"
        self.helper.attrs = {
            "hx-post": reverse_lazy("index"),
            "hx-target": "#registration-form",
            "hx-swap": "outerHTML",
        }
        self.helper.add_input(Submit("submit", "Submit"))

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"hx-get": reverse_lazy("index"), "hx-trigger": "keyup"}
        )
    )
    password = forms.CharField(widget=forms.PasswordInput())
