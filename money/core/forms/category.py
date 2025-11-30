from django import forms
from core.models import Category


class CategoryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "required input input-primary", "autocomplete": "off"}
        )
    )

    def clean_name(self):
        name = self.cleaned_data["name"].upper()

        if Category.objects.filter(name=name).exists():
            raise forms.ValidationError(f"{name} already exists.")

        return name
