from django import forms
from core.models import Operation


class OperationForm(forms.Form):
    date = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input input-primary"})
    )

    tier = forms.CharField(
        max_length=128, widget=forms.TextInput(attrs={"class": "input input-primary"})
    )

    # def clean_name(self):
    #    name = self.cleaned_data["name"]
    #    if len(name) < 5 or len(name) > 50:
    #        raise forms.ValidationError(
    #            "Book name must be between 5 and 50 characters long."
    #        )
    #    return name
